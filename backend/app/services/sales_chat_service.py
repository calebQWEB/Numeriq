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

class SalesChatService:
    def __init__(self):
        self.client = AsyncTogether(api_key=settings.together_api_key)
        self.spreadsheet_type = "Sales"

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

                def is_best_query(q: str) -> bool:
                    return bool(re.search(r"\b(best|top|highest|top performer|who (is|was) (the )?(best|top|highest))\b", q, re.I))

                def compute_best_from_insights() -> Optional[dict]:
                    tsr = insights.get("top_sales_reps")
                    if not tsr:
                        return None
                    best = tsr.get("best_performer")
                    if best:
                        return best
                    all_reps = tsr.get("all_reps") or []
                    if all_reps:
                        try:
                            return max(all_reps, key=lambda r: float(r.get("total_sales", 0)))
                        except Exception:
                            return None
                    return None

                def compute_best_from_raw() -> Optional[dict]:
                    totals = {}
                    # Define possible field names for sales rep
                    rep_fields = ["sales_rep", "salesperson", "rep", "sold_by"]
                    
                    for row in raw:
                        # Find the first field that exists in the row
                        rep = None
                        for field in rep_fields:
                            if field in row:
                                rep = row[field]
                                break
                        
                        # Skip if no rep field found or if rep value is empty/None
                        if not rep:
                            logger.debug(f"No valid sales rep found in row: {row}")
                            continue
                        
                        # Calculate price
                        price = None
                        try:
                            if "total_price" in row:
                                price = float(row.get("total_price") or 0)
                            elif "amount" in row:
                                price = float(row.get("amount") or 0)
                            elif "price" in row:
                                price = float(row.get("price") or 0)
                            else:
                                up = float(row.get("unit_price") or 0)
                                qty = float(row.get("quantity") or 1)
                                price = up * qty
                        except (ValueError, TypeError) as e:
                            logger.debug(f"Error calculating price for row: {e}")
                            price = 0.0
                        
                        totals[rep] = totals.get(rep, 0.0) + price
                    
                    if not totals:
                        return None
                    
                    best_name = max(totals, key=lambda k: totals[k])
                    return {"name": best_name, "total_sales": totals[best_name]}

                if is_best_query(question):
                    best = compute_best_from_insights() or compute_best_from_raw()
                    if best:
                        name = best.get("name")
                        total = float(best.get("total_sales") or 0)
                        state["answer"] = f"{name} is the top sales performer with ${total:,.2f} in sales (as computed from the supplied analysis/raw data)."
                        return state
                    else:
                        state["answer"] = "Insufficient data to determine the best performing sales representative from the provided analysis."
                        return state

                def build_context(insights: dict, ai_insights: dict, chat_history: list) -> str:
                    parts = []
                    if "sales_metrics" in insights:
                        m = insights["sales_metrics"]
                        parts.append(f"Total Revenue: ${float(m.get('total_revenue', 0)):,.2f}")
                        parts.append(f"Total Transactions: {int(m.get('total_transactions', 0)):,}")
                        parts.append(f"Average Transaction: ${float(m.get('average_transaction', 0)):,.2f}")
                    bp = compute_best_from_insights()
                    if bp:
                        parts.append(f"Best Performer: {bp.get('name')} — ${float(bp.get('total_sales', 0)):,.2f}")
                    if "revenue_by_category" in insights:
                        cats = insights["revenue_by_category"][:6]
                        parts.append("Revenue by Category: " + ", ".join([f"{c.get('category')}: ${float(c.get('revenue', 0)):,.2f}" for c in cats]))
                    tsr = insights.get("top_sales_reps", {})
                    all_reps = tsr.get("all_reps", [])[:5]
                    if all_reps:
                        parts.append("Top reps (sample): " + "; ".join([f"{r.get('name')}: ${float(r.get('total_sales', 0)):,.2f}" for r in all_reps]))
                    if "trends" in ai_insights:
                        parts.append("AI trends: " + "; ".join(ai_insights.get("trends", [])[:3]))
                    if chat_history:
                        recent = chat_history[-3:]
                        parts.append("Recent conversation: " + " || ".join([f"Q:{x.get('question')} A:{x.get('answer')[:80]}" for x in recent]))
                    return "\n".join(parts)

                context = build_context(insights, ai_insights, state.get("chat_history", []))

                if len(context) > 8000:
                    logger.warning(f"Context too long ({len(context)} characters); truncating to 7800")
                    context = context[:7800] + "\n\n[TRUNCATED CONTEXT]"

                system_msg = (
                    "You are an accurate sales data analyst. ONLY use facts present in the 'Sales Data' text below. "
                    "If the analysis or data does not contain the information requested, respond exactly: "
                    "'Insufficient data to determine <requested item>'. Do NOT invent or extrapolate facts."
                )

                prompt = f"""
                    Sales Data:
                    {context}

                    Question: {question}

                    Instructions:
                    - Use only information present above. Do not invent any facts.
                    - Provide concise answers and include numbers and names only if present in the data above.
                    - If you cannot answer from the data above, reply: "Insufficient data to determine {question}".
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
                logger.info(f"Generated sales answer using {len(list(insights.keys()))} insight keys")
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
            logger.error(f"Failed to process sales chat: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Sales chat processing error: {str(e)}")