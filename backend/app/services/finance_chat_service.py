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

class FinanceChatService:
    def __init__(self):
        self.client = AsyncTogether(api_key=settings.together_api_key)
        self.spreadsheet_type = "Finance"

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

                def is_total_revenue_query(q: str) -> bool:
                    return bool(re.search(r"\b(total revenue|total income|total sales|total earnings)\b", q, re.I))

                def is_largest_expense_query(q: str) -> bool:
                    return bool(re.search(r"\b(largest expense|biggest expense|highest expense|most expensive|top expense)\b", q, re.I))

                def is_profit_query(q: str) -> bool:
                    return bool(re.search(r"\b(total profit|net profit|net income|profitability)\b", q, re.I))

                def compute_total_revenue_from_insights() -> Optional[float]:
                    if "revenue_overview" in insights:
                        return float(insights["revenue_overview"].get("total_revenue", 0))
                    if "transaction_summary" in insights:
                        # For finance data, positive amounts might represent revenue
                        return float(insights["transaction_summary"].get("total_amount", 0))
                    return None

                def compute_total_revenue_from_raw() -> Optional[float]:
                    revenue_fields = ["revenue", "income", "sales", "total_price", "amount"]
                    category_fields = ["category", "type", "transaction_type"]
                    
                    total = 0.0
                    for row in raw:
                        # Check if it's a revenue transaction by category
                        is_revenue = False
                        for cat_field in category_fields:
                            if cat_field in row:
                                cat_value = str(row[cat_field] or "").lower()
                                if any(rev_word in cat_value for rev_word in ["revenue", "income", "sales", "earning"]):
                                    is_revenue = True
                                    break
                        
                        # If no category, check revenue fields
                        if not is_revenue:
                            for field in revenue_fields:
                                if field in row:
                                    is_revenue = True
                                    break
                        
                        if is_revenue:
                            for field in revenue_fields:
                                if field in row:
                                    try:
                                        total += float(row.get(field) or 0)
                                        break
                                    except (ValueError, TypeError):
                                        continue
                    
                    return total if total > 0 else None

                def compute_largest_expense_from_insights() -> Optional[dict]:
                    if "expense_by_category" in insights:
                        expenses = insights["expense_by_category"]
                        if expenses:
                            try:
                                largest = max(expenses, key=lambda e: float(e.get("total_expense", 0)))
                                return {"category": largest.get("category"), "amount": largest.get("total_expense")}
                            except Exception:
                                pass
                    if "top_expense_vendors" in insights:
                        vendors = insights["top_expense_vendors"]
                        if vendors:
                            try:
                                largest = max(vendors, key=lambda v: float(v.get("total_expense", 0)))
                                return {"vendor": largest.get("vendor"), "amount": largest.get("total_expense")}
                            except Exception:
                                pass
                    return None

                def compute_largest_expense_from_raw() -> Optional[dict]:
                    expense_fields = ["expense", "cost", "amount", "total_expense"]
                    category_fields = ["category", "vendor", "supplier", "type"]
                    
                    category_totals = {}
                    for row in raw:
                        # Check if it's an expense
                        is_expense = False
                        cat_type = str(row.get("category") or row.get("type") or "").lower()
                        if any(exp_word in cat_type for exp_word in ["expense", "cost", "payment"]):
                            is_expense = True
                        
                        if is_expense:
                            category = None
                            for cat_field in category_fields:
                                if cat_field in row and row[cat_field]:
                                    category = str(row[cat_field])
                                    break
                            
                            if category:
                                amount = 0.0
                                for field in expense_fields:
                                    if field in row:
                                        try:
                                            amount = float(row.get(field) or 0)
                                            break
                                        except (ValueError, TypeError):
                                            continue
                                
                                category_totals[category] = category_totals.get(category, 0.0) + amount
                    
                    if not category_totals:
                        return None
                    
                    largest_cat = max(category_totals, key=lambda k: category_totals[k])
                    return {"category": largest_cat, "amount": category_totals[largest_cat]}

                def compute_profit_from_insights() -> Optional[float]:
                    if "profitability_overview" in insights:
                        return float(insights["profitability_overview"].get("total_profit", 0))
                    return None

                def compute_profit_from_raw() -> Optional[dict]:
                    revenue = compute_total_revenue_from_raw() or 0
                    # Sum all expenses
                    expense_fields = ["expense", "cost"]
                    total_expense = 0.0
                    
                    for row in raw:
                        cat = str(row.get("category") or row.get("type") or "").lower()
                        if any(exp_word in cat for exp_word in ["expense", "cost", "payment"]):
                            for field in expense_fields:
                                if field in row:
                                    try:
                                        total_expense += float(row.get(field) or 0)
                                        break
                                    except (ValueError, TypeError):
                                        continue
                    
                    if revenue > 0 or total_expense > 0:
                        return {"revenue": revenue, "expense": total_expense, "profit": revenue - total_expense}
                    return None

                if is_total_revenue_query(question):
                    revenue = compute_total_revenue_from_insights() or compute_total_revenue_from_raw()
                    if revenue is not None:
                        state["answer"] = f"Total revenue is ${revenue:,.2f} (computed from the supplied analysis/raw data)."
                        return state
                    else:
                        state["answer"] = "Insufficient data to determine total revenue from the provided analysis."
                        return state

                if is_largest_expense_query(question):
                    result = compute_largest_expense_from_insights() or compute_largest_expense_from_raw()
                    if result:
                        name = result.get("category") or result.get("vendor", "Unknown")
                        amount = float(result.get("amount") or 0)
                        state["answer"] = f"{name} is the largest expense category with ${amount:,.2f} (computed from the supplied analysis/raw data)."
                        return state
                    else:
                        state["answer"] = "Insufficient data to determine the largest expense from the provided analysis."
                        return state

                if is_profit_query(question):
                    profit = compute_profit_from_insights()
                    if profit is None:
                        profit_data = compute_profit_from_raw()
                        if profit_data:
                            profit = profit_data["profit"]
                    
                    if profit is not None:
                        state["answer"] = f"Total profit is ${profit:,.2f} (computed from the supplied analysis/raw data)."
                        return state
                    else:
                        state["answer"] = "Insufficient data to determine profit from the provided analysis."
                        return state

                def build_context(insights: dict, ai_insights: dict, chat_history: list) -> str:
                    parts = []
                    
                    if "transaction_summary" in insights:
                        ts = insights["transaction_summary"]
                        parts.append(f"Total Transactions: {int(ts.get('total_transactions', 0)):,}")
                        parts.append(f"Total Amount: ${float(ts.get('total_amount', 0)):,.2f}")
                        parts.append(f"Average Transaction: ${float(ts.get('average_transaction', 0)):,.2f}")
                    
                    if "revenue_overview" in insights:
                        rev = insights["revenue_overview"]
                        parts.append(f"Total Revenue: ${float(rev.get('total_revenue', 0)):,.2f}")
                        parts.append(f"Revenue Transactions: {int(rev.get('revenue_transactions', 0)):,}")
                    
                    if "expense_overview" in insights:
                        exp = insights["expense_overview"]
                        parts.append(f"Total Expenses: ${float(exp.get('total_expenses', 0)):,.2f}")
                        parts.append(f"Expense Transactions: {int(exp.get('expense_transactions', 0)):,}")
                    
                    if "profitability_overview" in insights:
                        profit = insights["profitability_overview"]
                        parts.append(f"Total Profit: ${float(profit.get('total_profit', 0)):,.2f}")
                        if "profit_margin" in profit:
                            parts.append(f"Profit Margin: {float(profit.get('profit_margin', 0)):.2f}%")
                    
                    if "cashflow_overview" in insights:
                        cf = insights["cashflow_overview"]
                        parts.append(f"Net Cash Flow: ${float(cf.get('net_cashflow', 0)):,.2f}")
                        parts.append(f"Total Inflows: ${float(cf.get('total_inflows', 0)):,.2f}")
                        parts.append(f"Total Outflows: ${float(cf.get('total_outflows', 0)):,.2f}")
                    
                    if "expense_by_category" in insights:
                        exp_cats = insights["expense_by_category"][:5]
                        parts.append("Top Expense Categories: " + ", ".join([
                            f"{c.get('category')}: ${float(c.get('total_expense', 0)):,.2f}" 
                            for c in exp_cats
                        ]))
                    
                    if "revenue_by_category" in insights:
                        rev_cats = insights["revenue_by_category"][:5]
                        parts.append("Revenue by Category: " + ", ".join([
                            f"{c.get('category')}: ${float(c.get('total_revenue', 0)):,.2f}" 
                            for c in rev_cats
                        ]))
                    
                    if "budget_performance" in insights:
                        budget = insights["budget_performance"]
                        parts.append(f"Budget Utilization: {float(budget.get('budget_utilization_rate', 0)):.1f}%")
                        parts.append(f"Budget Variance: ${float(budget.get('total_variance', 0)):,.2f}")
                    
                    if "monthly_financial_trends" in insights:
                        trends = insights["monthly_financial_trends"][-3:]
                        parts.append("Recent Monthly Trends: " + ", ".join([
                            f"{t.get('month')}: ${float(t.get('total_amount', 0)):,.2f}" 
                            for t in trends
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
                    logger.warning(f"Finance context too long ({len(context)} characters); truncating to 7800")
                    context = context[:7800] + "\n\n[TRUNCATED CONTEXT]"

                system_msg = (
                    "You are an accurate financial data analyst. ONLY use facts present in the 'Financial Data' text below. "
                    "If the analysis or data does not contain the information requested, respond exactly: "
                    "'Insufficient data to determine <requested item>'. Do NOT invent or extrapolate facts. "
                    "Apply accounting principles and provide business context when appropriate."
                )

                prompt = f"""
                    Financial Data:
                    {context}

                    Question: {question}

                    Instructions:
                    - Use only information present above. Do not invent any facts.
                    - Provide concise answers and include numbers only if present in the data above.
                    - Format currency as $X,XXX.XX, percentages as X.X%, and financial ratios to 2 decimal places.
                    - If you cannot answer from the data above, reply: "Insufficient data to determine {question}".
                    - Focus on actionable financial insights when relevant.
                    """

                messages = [
                    {"role": "system", "content": system_msg},
                    {"role": "user", "content": prompt}
                ]

                response = await self.client.chat.completions.create(
                    model="mistralai/Mixtral-8x7B-Instruct-v0.1",
                    messages=messages,
                    max_tokens=600,
                    temperature=0.1
                )

                if not response.choices or not response.choices[0].message.content:
                    logger.error("Invalid response from API")
                    raise HTTPException(status_code=500, detail="Invalid response from AI model")

                answer = response.choices[0].message.content.strip()
                state["answer"] = answer
                logger.info(f"Generated finance answer using {len(list(insights.keys()))} insight keys")
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
            logger.error(f"Failed to process finance chat: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Finance chat processing error: {str(e)}")