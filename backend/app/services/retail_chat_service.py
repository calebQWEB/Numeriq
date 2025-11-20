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

class RetailChatService:
    def __init__(self):
        self.client = AsyncTogether(api_key=settings.together_api_key)
        self.spreadsheet_type = "Retail"

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

                def is_top_product_query(q: str) -> bool:
                    return bool(re.search(r"\b(top product|best.?selling product|highest revenue product|best product)\b", q, re.I))

                def is_top_category_query(q: str) -> bool:
                    return bool(re.search(r"\b(top category|best.?selling category|highest revenue category|best category)\b", q, re.I))

                def is_total_revenue_query(q: str) -> bool:
                    return bool(re.search(r"\b(total revenue|total sales|overall revenue|revenue total)\b", q, re.I))

                def is_avg_margin_query(q: str) -> bool:
                    return bool(re.search(r"\b(average margin|mean margin|profit margin average)\b", q, re.I))

                def compute_top_product_from_insights() -> Optional[dict]:
                    if "top_performing_products" in insights:
                        products = insights["top_performing_products"]
                        if products:
                            return products[0]
                    if "top_selling_products" in insights:
                        products = insights["top_selling_products"]
                        if products:
                            return products[0]
                    return None

                def compute_top_product_from_raw() -> Optional[dict]:
                    product_fields = ["product_name", "product", "item", "item_name"]
                    qty_fields = ["quantity_sold", "quantity", "qty", "units_sold"]
                    price_fields = ["price", "unit_price", "selling_price"]
                    
                    product_field = None
                    qty_field = None
                    price_field = None
                    
                    for field in product_fields:
                        if field in raw[0] if raw else {}:
                            product_field = field
                            break
                    
                    for field in qty_fields:
                        if field in raw[0] if raw else {}:
                            qty_field = field
                            break
                    
                    for field in price_fields:
                        if field in raw[0] if raw else {}:
                            price_field = field
                            break
                    
                    if not product_field or not qty_field:
                        return None
                    
                    product_totals = {}
                    for row in raw:
                        product = row.get(product_field)
                        if product:
                            try:
                                qty = float(row.get(qty_field, 0))
                                price = float(row.get(price_field, 1)) if price_field else 1
                                revenue = qty * price
                                
                                if product not in product_totals:
                                    product_totals[product] = {'revenue': 0, 'units': 0}
                                product_totals[product]['revenue'] += revenue
                                product_totals[product]['units'] += qty
                            except (ValueError, TypeError):
                                continue
                    
                    if not product_totals:
                        return None
                    
                    top_product = max(product_totals, key=lambda k: product_totals[k]['revenue'])
                    return {
                        'product': top_product,
                        'total_revenue': product_totals[top_product]['revenue'],
                        'units_sold': int(product_totals[top_product]['units'])
                    }

                def compute_top_category_from_insights() -> Optional[dict]:
                    if "category_performance" in insights:
                        categories = insights["category_performance"]
                        if categories:
                            return categories[0]
                    return None

                def compute_top_category_from_raw() -> Optional[dict]:
                    category_fields = ["category", "product_category", "type", "class"]
                    qty_fields = ["quantity_sold", "quantity", "qty", "units_sold"]
                    price_fields = ["price", "unit_price", "selling_price"]
                    
                    category_field = None
                    qty_field = None
                    price_field = None
                    
                    for field in category_fields:
                        if field in raw[0] if raw else {}:
                            category_field = field
                            break
                    
                    for field in qty_fields:
                        if field in raw[0] if raw else {}:
                            qty_field = field
                            break
                    
                    for field in price_fields:
                        if field in raw[0] if raw else {}:
                            price_field = field
                            break
                    
                    if not category_field or not qty_field:
                        return None
                    
                    category_totals = {}
                    for row in raw:
                        category = row.get(category_field)
                        if category:
                            try:
                                qty = float(row.get(qty_field, 0))
                                price = float(row.get(price_field, 1)) if price_field else 1
                                revenue = qty * price
                                category_totals[category] = category_totals.get(category, 0) + revenue
                            except (ValueError, TypeError):
                                continue
                    
                    if not category_totals:
                        return None
                    
                    top_category = max(category_totals, key=lambda k: category_totals[k])
                    return {'category': top_category, 'total_revenue': category_totals[top_category]}

                def compute_total_revenue_from_insights() -> Optional[float]:
                    if "top_performing_products" in insights:
                        return sum(float(p.get('total_revenue', 0)) for p in insights["top_performing_products"])
                    return None

                def compute_total_revenue_from_raw() -> Optional[float]:
                    qty_fields = ["quantity_sold", "quantity", "qty", "units_sold"]
                    price_fields = ["price", "unit_price", "selling_price"]
                    
                    qty_field = None
                    price_field = None
                    
                    for field in qty_fields:
                        if field in raw[0] if raw else {}:
                            qty_field = field
                            break
                    
                    for field in price_fields:
                        if field in raw[0] if raw else {}:
                            price_field = field
                            break
                    
                    if not qty_field or not price_field:
                        return None
                    
                    total_revenue = 0
                    for row in raw:
                        try:
                            qty = float(row.get(qty_field, 0))
                            price = float(row.get(price_field, 0))
                            total_revenue += qty * price
                        except (ValueError, TypeError):
                            continue
                    
                    return total_revenue if total_revenue > 0 else None

                def compute_avg_margin_from_insights() -> Optional[float]:
                    if "margin_analysis" in insights:
                        return float(insights["margin_analysis"].get("avg_margin_percent", 0))
                    return None

                def compute_avg_margin_from_raw() -> Optional[float]:
                    price_fields = ["price", "unit_price", "selling_price"]
                    cost_fields = ["cost", "unit_cost", "cogs"]
                    
                    price_field = None
                    cost_field = None
                    
                    for field in price_fields:
                        if field in raw[0] if raw else {}:
                            price_field = field
                            break
                    
                    for field in cost_fields:
                        if field in raw[0] if raw else {}:
                            cost_field = field
                            break
                    
                    if not price_field or not cost_field:
                        return None
                    
                    margins = []
                    for row in raw:
                        try:
                            price = float(row.get(price_field, 0))
                            cost = float(row.get(cost_field, 0))
                            if price > 0:
                                margin = ((price - cost) / price) * 100
                                margins.append(margin)
                        except (ValueError, TypeError):
                            continue
                    
                    return sum(margins) / len(margins) if margins else None

                if is_top_product_query(question):
                    result = compute_top_product_from_insights() or compute_top_product_from_raw()
                    if result:
                        product = result.get('product')
                        revenue = float(result.get('total_revenue', 0))
                        units = int(result.get('units_sold', 0))
                        state["answer"] = f"{product} is the top-performing product with ${revenue:,.2f} in revenue and {units:,} units sold (computed from the supplied analysis/raw data)."
                        return state
                    else:
                        state["answer"] = "Insufficient data to determine the top product from the provided analysis."
                        return state

                if is_top_category_query(question):
                    result = compute_top_category_from_insights() or compute_top_category_from_raw()
                    if result:
                        category = result.get('category')
                        revenue = float(result.get('total_revenue', 0))
                        state["answer"] = f"{category} is the top-performing category with ${revenue:,.2f} in revenue (computed from the supplied analysis/raw data)."
                        return state
                    else:
                        state["answer"] = "Insufficient data to determine the top category from the provided analysis."
                        return state

                if is_total_revenue_query(question):
                    revenue = compute_total_revenue_from_insights() or compute_total_revenue_from_raw()
                    if revenue is not None:
                        state["answer"] = f"Total revenue: ${revenue:,.2f} (computed from the supplied analysis/raw data)."
                        return state
                    else:
                        state["answer"] = "Insufficient data to determine total revenue from the provided analysis."
                        return state

                if is_avg_margin_query(question):
                    margin = compute_avg_margin_from_insights() or compute_avg_margin_from_raw()
                    if margin is not None:
                        state["answer"] = f"Average profit margin: {margin:.1f}% (computed from the supplied analysis/raw data)."
                        return state
                    else:
                        state["answer"] = "Insufficient data to determine average margin from the provided analysis."
                        return state

                def build_context(insights: dict, ai_insights: dict, chat_history: list) -> str:
                    parts = []
                    
                    if "top_performing_products" in insights:
                        top_prods = insights["top_performing_products"][:5]
                        parts.append("Top Products by Revenue: " + ", ".join([
                            f"{p.get('product')}: ${float(p.get('total_revenue', 0)):,.2f}" 
                            for p in top_prods
                        ]))
                    elif "top_selling_products" in insights:
                        top_prods = insights["top_selling_products"][:5]
                        parts.append("Top Products by Units: " + ", ".join([
                            f"{p.get('product')}: {int(p.get('units_sold', 0)):,} units" 
                            for p in top_prods
                        ]))
                    
                    if "category_performance" in insights:
                        cats = insights["category_performance"][:5]
                        parts.append("Category Performance: " + ", ".join([
                            f"{c.get('category')}: ${float(c.get('total_revenue', 0)):,.2f} ({float(c.get('revenue_share_percent', 0)):.1f}%)" 
                            for c in cats
                        ]))
                    
                    if "brand_performance" in insights:
                        brands = insights["brand_performance"][:3]
                        parts.append("Top Brands: " + ", ".join([
                            f"{b.get('brand')}: ${float(b.get('total_revenue', 0)):,.2f}" 
                            for b in brands
                        ]))
                    
                    if "pricing_metrics" in insights:
                        pricing = insights["pricing_metrics"]
                        parts.append(f"Average Selling Price: ${float(pricing.get('avg_selling_price', 0)):,.2f}")
                        parts.append(f"Price Range: ${float(pricing.get('price_range', {}).get('min', 0)):,.2f} - ${float(pricing.get('price_range', {}).get('max', 0)):,.2f}")
                    
                    if "margin_analysis" in insights:
                        margin = insights["margin_analysis"]
                        parts.append(f"Average Margin: {float(margin.get('avg_margin_percent', 0)):.1f}%")
                    
                    if "inventory_metrics" in insights:
                        inv = insights["inventory_metrics"]
                        parts.append(f"Total Inventory: {float(inv.get('total_inventory_value', 0)):,.0f} units")
                        parts.append(f"Low Stock Products: {int(inv.get('low_stock_products', 0)):,}")
                        parts.append(f"Out of Stock: {int(inv.get('out_of_stock', 0)):,}")
                    
                    if "store_performance" in insights:
                        stores = insights["store_performance"][:3]
                        parts.append("Top Stores: " + ", ".join([
                            f"{s.get('store')}: ${float(s.get('total_revenue', 0)):,.2f}" 
                            for s in stores
                        ]))
                    
                    if "discount_analysis" in insights:
                        discount = insights["discount_analysis"]
                        parts.append(f"Average Discount: {float(discount.get('avg_discount_percent', 0)):.1f}%")
                        parts.append(f"Discount Penetration: {float(discount.get('discount_penetration', 0)):.1f}%")
                    
                    if "seasonal_trends" in insights:
                        seasons = insights["seasonal_trends"]
                        best_season = max(seasons, key=lambda s: float(s.get('total_revenue', 0)))
                        parts.append(f"Best Season: {best_season.get('season')} with ${float(best_season.get('total_revenue', 0)):,.2f}")
                    
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
                    logger.warning(f"Retail context too long ({len(context)} characters); truncating to 7800")
                    context = context[:7800] + "\n\n[TRUNCATED CONTEXT]"

                system_msg = (
                    "You are an accurate retail data analyst. ONLY use facts present in the 'Retail Data' text below. "
                    "If the analysis or data does not contain the information requested, respond exactly: "
                    "'Insufficient data to determine <requested item>'. Do NOT invent or extrapolate facts. "
                    "Focus on product performance, inventory management, pricing strategies, and sales trends."
                )

                prompt = f"""
                    Retail Data:
                    {context}

                    Question: {question}

                    Instructions:
                    - Use only information present above. Do not invent any facts.
                    - Provide concise answers and include numbers only if present in the data above.
                    - Format currency as $X,XXX.XX, percentages as X.X%, and quantities with commas.
                    - If you cannot answer from the data above, reply: "Insufficient data to determine {question}".
                    - Focus on retail metrics like revenue, margins, inventory turnover, and category performance.
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
                logger.info(f"Generated retail answer using {len(list(insights.keys()))} insight keys")
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
            logger.error(f"Failed to process retail chat: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Retail chat processing error: {str(e)}")