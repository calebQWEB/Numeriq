from langgraph.graph import StateGraph, END
from typing import TypedDict, List, Dict, Any, Optional
from app.utils.logger import logger
from fastapi import HTTPException
from together import AsyncTogether
from app.config.settings import settings
import re

class ChatState(TypedDict):
    file_id: str
    user_id: str
    question: str
    analysis_data: Dict
    raw_data: List[Dict[str, Any]]
    chat_history: List[Dict[str, str]]
    answer: str

class OperationsChatService:
    def __init__(self):
        self.client = AsyncTogether(api_key=settings.together_api_key)
        self.spreadsheet_type = "Operations"

    async def process_chat(
        self, 
        file_id: str, 
        user_id: str, 
        question: str, 
        analysis_data: Dict, 
        raw_data: List[Dict[str, Any]],
        chat_history: List[Dict[str, str]]
    ) -> str:
        try:
            workflow = StateGraph(dict)
            
            async def generate_answer(state: ChatState) -> ChatState:
                insights = state.get("analysis_data", {}).get("insights", {})
                ai_insights = state.get("analysis_data", {}).get("ai_insights", {})
                raw = state.get("raw_data", [])
                question = state.get("question", "").strip()
                question = re.sub(r'[\x00-\x1F\x7F]', '', question)

                def is_total_orders_query(q: str) -> bool:
                    return bool(re.search(r"\b(total orders|how many orders|order count|number of orders)\b", q, re.I))

                def is_fulfillment_rate_query(q: str) -> bool:
                    return bool(re.search(r"\b(fulfillment rate|completion rate|on.?time delivery|otd rate)\b", q, re.I))

                def is_lead_time_query(q: str) -> bool:
                    return bool(re.search(r"\b(average lead time|mean lead time|lead time average)\b", q, re.I))

                def is_top_supplier_query(q: str) -> bool:
                    return bool(re.search(r"\b(top supplier|best supplier|largest supplier|highest volume supplier)\b", q, re.I))

                def compute_total_orders_from_insights() -> Optional[int]:
                    if "order_overview" in insights:
                        return int(insights["order_overview"].get("total_orders", 0))
                    return None

                def compute_total_orders_from_raw() -> Optional[int]:
                    order_fields = ["order_id", "order_number", "id"]
                    
                    for field in order_fields:
                        if field in raw[0] if raw else {}:
                            unique_orders = set()
                            for row in raw:
                                order_val = row.get(field)
                                if order_val:
                                    unique_orders.add(str(order_val))
                            return len(unique_orders) if unique_orders else None
                    
                    # If no order ID field, count rows as orders
                    return len(raw) if raw else None

                def compute_fulfillment_rate_from_insights() -> Optional[float]:
                    if "fulfillment_metrics" in insights:
                        return float(insights["fulfillment_metrics"].get("fulfillment_rate_percent", 0))
                    if "delivery_performance" in insights and "on_time_delivery" in insights["delivery_performance"]:
                        return float(insights["delivery_performance"]["on_time_delivery"].get("on_time_delivery_rate_percent", 0))
                    return None

                def compute_fulfillment_rate_from_raw() -> Optional[float]:
                    status_fields = ["status", "order_status", "state"]
                    completed_statuses = ["completed", "delivered", "shipped", "fulfilled", "closed"]
                    
                    for field in status_fields:
                        if field in raw[0] if raw else {}:
                            total = len(raw)
                            completed = sum(1 for row in raw if str(row.get(field, "")).lower() in completed_statuses)
                            if total > 0:
                                return (completed / total) * 100
                    
                    return None

                def compute_avg_lead_time_from_insights() -> Optional[float]:
                    if "lead_time_metrics" in insights:
                        return float(insights["lead_time_metrics"].get("avg_lead_time", 0))
                    return None

                def compute_avg_lead_time_from_raw() -> Optional[float]:
                    lead_time_fields = ["lead_time", "processing_time", "fulfillment_time", "cycle_time"]
                    
                    for field in lead_time_fields:
                        if field in raw[0] if raw else {}:
                            lead_times = []
                            for row in raw:
                                try:
                                    lt = float(row.get(field, 0))
                                    if lt > 0:
                                        lead_times.append(lt)
                                except (ValueError, TypeError):
                                    continue
                            
                            if lead_times:
                                return sum(lead_times) / len(lead_times)
                    
                    return None

                def compute_top_supplier_from_insights() -> Optional[dict]:
                    if "supplier_performance" in insights:
                        suppliers = insights["supplier_performance"]
                        if suppliers:
                            try:
                                top = max(suppliers, key=lambda s: float(s.get("total_quantity", 0)))
                                return {"supplier": top.get("supplier"), "quantity": top.get("total_quantity")}
                            except Exception:
                                pass
                    return None

                def compute_top_supplier_from_raw() -> Optional[dict]:
                    supplier_fields = ["supplier", "vendor", "provider"]
                    quantity_fields = ["quantity", "qty", "amount", "volume"]
                    
                    supplier_totals = {}
                    supplier_field = None
                    quantity_field = None
                    
                    # Find available fields
                    for field in supplier_fields:
                        if field in raw[0] if raw else {}:
                            supplier_field = field
                            break
                    
                    for field in quantity_fields:
                        if field in raw[0] if raw else {}:
                            quantity_field = field
                            break
                    
                    if not supplier_field or not quantity_field:
                        return None
                    
                    for row in raw:
                        supplier = row.get(supplier_field)
                        if supplier:
                            try:
                                qty = float(row.get(quantity_field, 0))
                                supplier_totals[supplier] = supplier_totals.get(supplier, 0.0) + qty
                            except (ValueError, TypeError):
                                continue
                    
                    if not supplier_totals:
                        return None
                    
                    top_supplier = max(supplier_totals, key=lambda k: supplier_totals[k])
                    return {"supplier": top_supplier, "quantity": supplier_totals[top_supplier]}

                if is_total_orders_query(question):
                    total = compute_total_orders_from_insights() or compute_total_orders_from_raw()
                    if total is not None:
                        state["answer"] = f"Total orders: {total:,} (computed from the supplied analysis/raw data)."
                        return state
                    else:
                        state["answer"] = "Insufficient data to determine total orders from the provided analysis."
                        return state

                if is_fulfillment_rate_query(question):
                    rate = compute_fulfillment_rate_from_insights() or compute_fulfillment_rate_from_raw()
                    if rate is not None:
                        state["answer"] = f"Fulfillment rate: {rate:.1f}% (computed from the supplied analysis/raw data)."
                        return state
                    else:
                        state["answer"] = "Insufficient data to determine fulfillment rate from the provided analysis."
                        return state

                if is_lead_time_query(question):
                    lead_time = compute_avg_lead_time_from_insights() or compute_avg_lead_time_from_raw()
                    if lead_time is not None:
                        state["answer"] = f"Average lead time: {lead_time:.1f} days (computed from the supplied analysis/raw data)."
                        return state
                    else:
                        state["answer"] = "Insufficient data to determine average lead time from the provided analysis."
                        return state

                if is_top_supplier_query(question):
                    result = compute_top_supplier_from_insights() or compute_top_supplier_from_raw()
                    if result:
                        supplier = result.get("supplier")
                        quantity = float(result.get("quantity", 0))
                        state["answer"] = f"{supplier} is the top supplier with {quantity:,.0f} units supplied (computed from the supplied analysis/raw data)."
                        return state
                    else:
                        state["answer"] = "Insufficient data to determine top supplier from the provided analysis."
                        return state

                def build_context(insights: dict, ai_insights: dict, chat_history: list) -> str:
                    parts = []
                    
                    if "order_overview" in insights:
                        oo = insights["order_overview"]
                        parts.append(f"Total Orders: {int(oo.get('total_orders', 0)):,}")
                        parts.append(f"Total Quantity Ordered: {float(oo.get('total_quantity_ordered', 0)):,.0f}")
                        parts.append(f"Average Order Quantity: {float(oo.get('average_order_quantity', 0)):,.1f}")
                    
                    if "fulfillment_metrics" in insights:
                        fm = insights["fulfillment_metrics"]
                        parts.append(f"Fulfillment Rate: {float(fm.get('fulfillment_rate_percent', 0)):.1f}%")
                        parts.append(f"Completed Orders: {int(fm.get('completed_orders', 0)):,}")
                        parts.append(f"Pending Orders: {int(fm.get('pending_orders', 0)):,}")
                    
                    if "inventory_overview" in insights:
                        inv = insights["inventory_overview"]
                        parts.append(f"Total Inventory: {float(inv.get('total_inventory_units', 0)):,.0f} units")
                        parts.append(f"Low Inventory Items: {int(inv.get('low_inventory_items', 0)):,}")
                    
                    if "lead_time_metrics" in insights:
                        lt = insights["lead_time_metrics"]
                        parts.append(f"Average Lead Time: {float(lt.get('avg_lead_time', 0)):.1f} days")
                        parts.append(f"Lead Time Consistency Score: {float(lt.get('lead_time_consistency_score', 0)):.1f}%")
                    
                    if "supplier_performance" in insights:
                        suppliers = insights["supplier_performance"][:3]
                        parts.append("Top Suppliers: " + ", ".join([
                            f"{s.get('supplier')}: {float(s.get('total_quantity', 0)):,.0f} units" 
                            for s in suppliers if s.get('total_quantity')
                        ]))
                    
                    if "delivery_performance" in insights and "on_time_delivery" in insights["delivery_performance"]:
                        otd = insights["delivery_performance"]["on_time_delivery"]
                        parts.append(f"On-Time Delivery Rate: {float(otd.get('on_time_delivery_rate_percent', 0)):.1f}%")
                    
                    if "quality_metrics" in insights:
                        qm = insights["quality_metrics"]
                        if "defect_analysis" in qm:
                            parts.append(f"Average Defect Rate: {float(qm['defect_analysis'].get('avg_defect_rate', 0)):.2f}%")
                        if "quality_score_analysis" in qm:
                            parts.append(f"Average Quality Score: {float(qm['quality_score_analysis'].get('avg_quality_score', 0)):.2f}")
                    
                    if "production_efficiency" in insights:
                        pe = insights["production_efficiency"]
                        if "utilization" in pe:
                            parts.append(f"Average Utilization: {float(pe['utilization'].get('avg_utilization_percent', 0)):.1f}%")
                        if "productivity" in pe:
                            parts.append(f"Average Productivity: {float(pe['productivity'].get('avg_productivity', 0)):.2f}")
                    
                    if "cost_overview" in insights:
                        cost = insights["cost_overview"]
                        parts.append(f"Total Operational Costs: ${float(cost.get('total_operational_costs', 0)):,.2f}")
                    
                    if "regional_operations" in insights:
                        ro = insights["regional_operations"]
                        if "volume_by_region" in ro:
                            top_regions = ro["volume_by_region"][:3]
                            parts.append("Top Regions by Volume: " + ", ".join([
                                f"{r.get('region')}: {float(r.get('total_quantity', 0)):,.0f}" 
                                for r in top_regions
                            ]))
                    
                    if "trends" in ai_insights:
                        parts.append("AI trends: " + "; ".join(ai_insights.get("trends", [])[:3]))
                    
                    if chat_history:
                        recent = chat_history[-3:]
                        parts.append("Recent conversation: " + " || ".join([
                            f"Q:{x.get('question')} A:{x.get('answer')[:80]}" 
                            for x in recent
                        ]))
                    
                    return "\n".join(parts)

                context = build_context(insights, ai_insights, state.get("chat_history", []))

                if len(context) > 8000:
                    logger.warning(f"Operations context too long ({len(context)} characters); truncating to 7800")
                    context = context[:7800] + "\n\n[TRUNCATED CONTEXT]"

                system_msg = (
                    "You are an accurate operations data analyst. ONLY use facts present in the 'Operations Data' text below. "
                    "If the analysis or data does not contain the information requested, respond exactly: "
                    "'Insufficient data to determine <requested item>'. Do NOT invent or extrapolate facts. "
                    "Focus on operational efficiency, supply chain performance, and logistics metrics."
                )

                prompt = f"""
                    Operations Data:
                    {context}

                    Question: {question}

                    Instructions:
                    - Use only information present above. Do not invent any facts.
                    - Provide concise answers and include numbers only if present in the data above.
                    - Format quantities with commas, percentages as X.X%, and metrics appropriately.
                    - If you cannot answer from the data above, reply: "Insufficient data to determine {question}".
                    - Focus on operational KPIs like fulfillment rates, lead times, inventory levels, and quality metrics.
                    """

                messages = [
                    {"role": "system", "content": system_msg},
                    {"role": "user", "content": prompt}
                ]

                response = await self.client.chat.completions.create(
                    model="mistralai/Mixtral-8x7B-Instruct-v0.1",
                    messages=messages,
                    max_tokens=500,
                    temperature=0.1
                )

                if not response.choices or not response.choices[0].message.content:
                    logger.error("Invalid response from API")
                    raise HTTPException(status_code=500, detail="Invalid response from AI model")

                answer = response.choices[0].message.content.strip()
                state["answer"] = answer
                logger.info(f"Generated operations answer using {len(list(insights.keys()))} insight keys")
                return state

            workflow.add_node("generate_answer", generate_answer)
            workflow.set_entry_point("generate_answer")
            workflow.add_edge("generate_answer", END)

            graph = workflow.compile()
            initial_state = {
                "file_id": file_id,
                "user_id": user_id,
                "question": question,
                "analysis_data": analysis_data,
                "raw_data": raw_data,
                "chat_history": chat_history,
                "answer": ""
            }

            result = await graph.ainvoke(initial_state)
            return result["answer"]

        except Exception as e:
            logger.error(f"Failed to process operations chat: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Operations chat processing error: {str(e)}")