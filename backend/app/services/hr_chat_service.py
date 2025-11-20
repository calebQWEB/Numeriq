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

class HRChatService:
    def __init__(self):
        self.client = AsyncTogether(api_key=settings.together_api_key)
        self.spreadsheet_type = "HR"

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

                def is_highest_paid_query(q: str) -> bool:
                    return bool(re.search(r"\b(highest paid|top paid|best paid|highest salary|who (makes|earns) (the )?(most|highest))\b", q, re.I))

                def is_department_query(q: str) -> bool:
                    return bool(re.search(r"\b(which department|what department|department with (most|highest|largest))\b", q, re.I))

                def compute_highest_paid_from_insights() -> Optional[dict]:
                    salary_by_pos = insights.get("salary_by_position", [])
                    if salary_by_pos:
                        try:
                            highest = max(salary_by_pos, key=lambda p: float(p.get("avg_salary", 0)))
                            return {"position": highest.get("position"), "avg_salary": highest.get("avg_salary")}
                        except Exception:
                            pass
                    return None

                def compute_highest_paid_from_raw() -> Optional[dict]:
                    salary_fields = ["salary", "wage", "compensation", "pay", "annual_salary"]
                    position_fields = ["position", "job_title", "role", "title"]
                    
                    position_salaries = {}
                    for row in raw:
                        position = None
                        for field in position_fields:
                            if field in row:
                                position = row[field]
                                break
                        
                        if not position:
                            continue
                        
                        salary = None
                        for field in salary_fields:
                            if field in row:
                                try:
                                    salary = float(row.get(field) or 0)
                                    break
                                except (ValueError, TypeError):
                                    continue
                        
                        if salary:
                            if position not in position_salaries:
                                position_salaries[position] = []
                            position_salaries[position].append(salary)
                    
                    if not position_salaries:
                        return None
                    
                    avg_salaries = {pos: sum(salaries)/len(salaries) for pos, salaries in position_salaries.items()}
                    highest_pos = max(avg_salaries, key=lambda k: avg_salaries[k])
                    return {"position": highest_pos, "avg_salary": avg_salaries[highest_pos]}

                def compute_largest_department_from_insights() -> Optional[dict]:
                    dept_dist = insights.get("department_distribution", [])
                    if dept_dist:
                        try:
                            largest = max(dept_dist, key=lambda d: int(d.get("employee_count", 0)))
                            return {"department": largest.get("department"), "count": largest.get("employee_count")}
                        except Exception:
                            pass
                    return None

                def compute_largest_department_from_raw() -> Optional[dict]:
                    dept_fields = ["department", "dept", "division", "team"]
                    dept_counts = {}
                    
                    for row in raw:
                        dept = None
                        for field in dept_fields:
                            if field in row:
                                dept = row[field]
                                break
                        
                        if dept:
                            dept_counts[dept] = dept_counts.get(dept, 0) + 1
                    
                    if not dept_counts:
                        return None
                    
                    largest_dept = max(dept_counts, key=lambda k: dept_counts[k])
                    return {"department": largest_dept, "count": dept_counts[largest_dept]}

                if is_highest_paid_query(question):
                    result = compute_highest_paid_from_insights() or compute_highest_paid_from_raw()
                    if result:
                        pos = result.get("position")
                        salary = float(result.get("avg_salary") or 0)
                        state["answer"] = f"{pos} is the highest paid position with an average salary of ${salary:,.2f} (computed from the supplied analysis/raw data)."
                        return state
                    else:
                        state["answer"] = "Insufficient data to determine the highest paid position from the provided analysis."
                        return state

                if is_department_query(question):
                    result = compute_largest_department_from_insights() or compute_largest_department_from_raw()
                    if result:
                        dept = result.get("department")
                        count = int(result.get("count") or 0)
                        state["answer"] = f"{dept} is the largest department with {count:,} employees (computed from the supplied analysis/raw data)."
                        return state
                    else:
                        state["answer"] = "Insufficient data to determine department information from the provided analysis."
                        return state

                def build_context(insights: dict, ai_insights: dict, chat_history: list) -> str:
                    parts = []
                    
                    if "workforce_overview" in insights:
                        wo = insights["workforce_overview"]
                        parts.append(f"Total Employees: {int(wo.get('total_employees', 0)):,}")
                        parts.append(f"Active Employees: {int(wo.get('active_employees', 0)):,}")
                    
                    if "compensation_overview" in insights:
                        comp = insights["compensation_overview"]
                        parts.append(f"Average Salary: ${float(comp.get('avg_salary', 0)):,.0f}")
                        parts.append(f"Median Salary: ${float(comp.get('median_salary', 0)):,.0f}")
                        parts.append(f"Total Payroll: ${float(comp.get('total_payroll', 0)):,.0f}")
                    
                    if "salary_by_position" in insights:
                        top_positions = insights["salary_by_position"][:5]
                        parts.append("Top Paid Positions: " + ", ".join([
                            f"{p.get('position')}: ${float(p.get('avg_salary', 0)):,.0f}" 
                            for p in top_positions
                        ]))
                    
                    if "department_distribution" in insights:
                        depts = insights["department_distribution"][:5]
                        parts.append("Department Distribution: " + ", ".join([
                            f"{d.get('department')}: {int(d.get('employee_count', 0)):,} ({float(d.get('percentage', 0)):.1f}%)" 
                            for d in depts
                        ]))
                    
                    if "turnover_metrics" in insights:
                        turnover = insights["turnover_metrics"]
                        parts.append(f"Annual Turnover Rate: {float(turnover.get('annual_turnover_rate', 0)):.1f}%")
                    
                    if "performance_overview" in insights:
                        perf = insights["performance_overview"]
                        parts.append(f"Average Performance Rating: {float(perf.get('avg_performance_rating', 0)):.2f}")
                        parts.append(f"High Performers: {int(perf.get('high_performers', 0)):,}")
                    
                    if "training_overview" in insights:
                        training = insights["training_overview"]
                        parts.append(f"Average Training Hours: {float(training.get('avg_training_hours', 0)):.1f} per employee")
                    
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
                    logger.warning(f"HR context too long ({len(context)} characters); truncating to 7800")
                    context = context[:7800] + "\n\n[TRUNCATED CONTEXT]"

                system_msg = (
                    "You are an accurate HR data analyst. ONLY use facts present in the 'HR Data' text below. "
                    "If the analysis or data does not contain the information requested, respond exactly: "
                    "'Insufficient data to determine <requested item>'. Do NOT invent or extrapolate facts. "
                    "Maintain employee confidentiality and be mindful of privacy considerations."
                )

                prompt = f"""
                    HR Data:
                    {context}

                    Question: {question}

                    Instructions:
                    - Use only information present above. Do not invent any facts.
                    - Provide concise answers and include numbers and names only if present in the data above.
                    - Format salaries as $XX,XXX, percentages as XX.X%, and counts as whole numbers.
                    - If you cannot answer from the data above, reply: "Insufficient data to determine {question}".
                    - Be professional and maintain appropriate confidentiality standards.
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
                logger.info(f"Generated HR answer using {len(list(insights.keys()))} insight keys")
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
            logger.error(f"Failed to process HR chat: {str(e)}")
            raise HTTPException(status_code=500, detail=f"HR chat processing error: {str(e)}")