from langgraph.graph import StateGraph, END
from typing import TypedDict, Dict, Any, Literal, List
from app.utils.logger import logger
from fastapi import HTTPException
from together import AsyncTogether
from app.config.settings import settings
import json
import time
import asyncio
import math

class GraphState(TypedDict):
    json_data: Dict[str, Any]
    description: str
    spreadsheet_type: Literal['Finance', 'HR', 'Operations', 'Sales', 'Retail', 'Unknown']
    insights: Dict[str, Any]

class LangGraphService:
    def __init__(self):
        self.client = AsyncTogether(api_key=settings.together_api_key)
        self.types = ['Finance', 'HR', 'Operations', 'Sales', 'Retail']

    def _smart_sample_data(self, json_data: Dict[str, Any], max_rows: int = 100) -> Dict[str, Any]:
        """Smart sampling with statistical distribution and column prioritization"""
        if not isinstance(json_data, list):
            return {"sampled_data": json_data, "metadata": {"strategy": "no_sampling_needed"}}
        if not json_data:
            return {"sampled_data": [], "metadata": {"strategy": "empty_data"}}
        
        total_rows = len(json_data)
        if total_rows <= max_rows:
            return {"sampled_data": json_data, "metadata": {"strategy": "full_data", "total_rows": total_rows}}
        
        # Step 1: Column prioritization
        priority_data = self._prioritize_columns(json_data)
        filtered_data = priority_data["priority_data"]
        
        # Step 2: Statistical sampling - take from beginning, middle, end + some random
        beginning_size = max_rows // 4
        middle_size = max_rows // 4  
        end_size = max_rows // 4
        random_size = max_rows - beginning_size - middle_size - end_size
        
        # Beginning sample
        beginning = filtered_data[:beginning_size]
        
        # Middle sample
        middle_start = total_rows // 2 - middle_size // 2
        middle_end = middle_start + middle_size
        middle = filtered_data[middle_start:middle_end]
        
        # End sample
        end = filtered_data[-end_size:]
        
        # Random sample from remaining data
        import random
        remaining_indices = list(range(beginning_size, middle_start)) + list(range(middle_end, total_rows - end_size))
        if remaining_indices and random_size > 0:
            random_indices = random.sample(remaining_indices, min(random_size, len(remaining_indices)))
            random_sample = [filtered_data[i] for i in random_indices]
        else:
            random_sample = []
        
        sampled_data = beginning + middle + end + random_sample
        
        metadata = {
            "strategy": "smart_sampling",
            "total_rows": total_rows,
            "sampled_rows": len(sampled_data),
            "sampling_sections": ["beginning", "middle", "end", "random"],
            "column_info": priority_data["column_info"]
        }
        
        return {"sampled_data": sampled_data, "metadata": metadata}

    def _prioritize_columns(self, json_data: list) -> dict:
        """Rank columns by importance and filter to most relevant ones"""
        if not json_data:
            return {"priority_data": [], "column_info": {"strategy": "empty_data"}}
        
        # Get all columns from first row
        columns = list(json_data[0].keys()) if json_data else []
        if not columns:
            return {"priority_data": json_data, "column_info": {"strategy": "no_columns"}}
        
        # Analyze column importance using sample
        sample_size = min(100, len(json_data))
        sample_data = json_data[:sample_size]
        column_scores = self._rank_columns_by_importance(columns, sample_data)
        
        # Determine how many columns to keep (keep at least 3, at most 10)
        total_cols = len(columns)
        if total_cols <= 5:
            priority_cols = columns  # Keep all if few columns
        elif total_cols <= 15:
            priority_cols = column_scores[:8]  # Keep top 8
        else:
            priority_cols = column_scores[:10]  # Keep top 10 for very wide data
        
        # Filter data to priority columns only
        filtered_data = []
        for row in json_data:
            filtered_row = {col: row.get(col) for col in priority_cols if col in row}
            filtered_data.append(filtered_row)
        
        column_info = {
            "strategy": "column_prioritization",
            "total_columns": total_cols,
            "priority_columns": priority_cols,
            "kept_columns": len(priority_cols),
            "dropped_columns": total_cols - len(priority_cols)
        }
        
        return {"priority_data": filtered_data, "column_info": column_info}

    def _rank_columns_by_importance(self, columns: list, sample_data: list) -> list:
        """Rank columns by data variety, completeness, and likely business importance"""
        scores = {}
        
        for col in columns:
            # Extract values for this column
            values = [row.get(col) for row in sample_data if row.get(col) is not None]
            
            if not values:
                scores[col] = 0
                continue
            
            # Metrics for importance
            non_null_ratio = len(values) / len(sample_data)
            unique_values = len(set(str(v) for v in values))
            unique_ratio = unique_values / len(values) if values else 0
            
            # Business importance heuristics (higher score = more important)
            business_score = 1.0
            col_lower = col.lower()
            
            # High importance indicators
            if any(keyword in col_lower for keyword in ['id', 'name', 'date', 'time', 'amount', 'price', 'revenue', 'cost', 'profit', 'sales', 'customer']):
                business_score *= 2.0
            if any(keyword in col_lower for keyword in ['total', 'sum', 'avg', 'mean', 'count', 'quantity']):
                business_score *= 1.5
            
            # Penalize columns that are likely less important
            if any(keyword in col_lower for keyword in ['unnamed', 'index', 'row', 'column']):
                business_score *= 0.3
            if col_lower.startswith('unnamed'):
                business_score *= 0.1
            
            # Combined score: completeness * diversity * business relevance
            final_score = non_null_ratio * (unique_ratio + 0.1) * business_score
            scores[col] = final_score
        
        # Sort by score (highest first)
        return sorted(columns, key=lambda x: scores.get(x, 0), reverse=True)

    def _truncate_text(self, text: str, max_chars: int = 500) -> str:
        if len(text) <= max_chars:
            return text
        truncated = text[:max_chars].rsplit('\n', 1)[0] if '\n' in text[:max_chars] else text[:max_chars]
        return truncated + "\n... (truncated)"

    async def _call_llm_with_retry(self, prompt: str, max_tokens: int = 300, retries: int = 2) -> str:
        for attempt in range(retries):
            try:
                response = await self.client.chat.completions.create(
                    model="mistralai/Mixtral-8x7B-Instruct-v0.1",
                    messages=[{"role": "user", "content": prompt}],
                    response_format={"type": "json_object"},
                    max_tokens=max_tokens,
                    temperature=0.2
                )
                return response.choices[0].message.content.strip()
            except Exception as e:
                logger.warning(f"LLM call failed (attempt {attempt+1})", error=str(e))
                if attempt == retries - 1:
                    raise
                await asyncio.sleep(2 ** attempt)  # Exponential backoff

    # ---------- New helper methods for chunking & aggregation ----------
    def _estimate_tokens_from_text(self, text: str) -> int:
        """
        Rough token estimate: assume ~4 characters per token (conservative).
        You can adjust this heuristic if you have a tokenizer available.
        """
        if not text:
            return 0
        return max(1, math.ceil(len(text) / 4))

    def _chunk_json_data_by_tokens(self, json_data: List[Dict[str, Any]], max_input_tokens: int = 8000) -> List[List[Dict[str, Any]]]:
        """
        Split a list of rows (dicts) into chunks such that each chunk's JSON string
        representation is estimated to be under `max_input_tokens`.
        Default max_input_tokens is conservative (8k).
        """
        if not isinstance(json_data, list):
            return [json_data]
        if not json_data:
            return []

        chunks: List[List[Dict[str, Any]]] = []
        current_chunk: List[Dict[str, Any]] = []
        current_chars = 0
        max_chars = max_input_tokens * 4  # reverse heuristic to characters

        for row in json_data:
            row_text = json.dumps(row, ensure_ascii=False)
            row_len = len(row_text) + 2  # small padding
            if current_chars + row_len > max_chars and current_chunk:
                chunks.append(current_chunk)
                current_chunk = [row]
                current_chars = row_len
            else:
                current_chunk.append(row)
                current_chars += row_len

        if current_chunk:
            chunks.append(current_chunk)

        return chunks

    async def _merge_partials(self, partials: List[Any], domain: str, kind: str, description: str, max_tokens: int = 400) -> List[str]:
        """
        Merge a list of partial results (strings or JSON arrays) into a final concise list (2-3 items).
        `domain` e.g., 'finance', 'hr'. `kind` e.g., 'trends', 'anomalies', 'predictions'.
        """
        try:
            # Prepare a concise summarization prompt
            partials_text = json.dumps(partials, ensure_ascii=False)
            prompt = f"""
            You are an expert {domain} analyst. Given multiple partial {kind} results (JSON array or text) from different chunks of data,
            synthesize them into the top 2-3 {kind}. Keep entries short, include quantitative elements if present.
            
            Description: {self._truncate_text(description, max_chars=800)}
            Partials: {partials_text}
            
            Return JSON: {{"{kind}": ["Item 1", "Item 2"]}}
            """
            content = await self._call_llm_with_retry(prompt, max_tokens=max_tokens)
            parsed = json.loads(content)
            result = parsed.get(kind, [])
            if not isinstance(result, list):
                # fallback: try to coerce
                return [str(result)]
            return result
        except Exception as e:
            logger.error("Merging partials failed", error=str(e))
            # As fallback, return unique non-empty strings from partials
            flat = []
            for p in partials:
                if isinstance(p, list):
                    flat.extend([str(x) for x in p if x])
                else:
                    flat.append(str(p))
            # dedupe and short list
            seen = []
            for item in flat:
                if item not in seen and item.strip():
                    seen.append(item)
                if len(seen) >= 3:
                    break
            return seen or [f"Error merging {kind}"]

    async def _process_chunks_collect_and_merge(self, chunks: List[List[Dict[str, Any]]], domain: str, kind: str, prompt_template: str, description: str, per_chunk_max_tokens: int = 300, merge_max_tokens: int = 400) -> List[str]:
        """
        Generic helper:
        - runs prompt_template for each chunk (where template contains {data} and {description})
        - expects JSON with key `kind` in each chunk response
        - collects partials and merges them using _merge_partials
        """
        partials = []
        for chunk in chunks:
            try:
                data_text = json.dumps(chunk, ensure_ascii=False)
                prompt = prompt_template.format(data=data_text, description=self._truncate_text(description, max_chars=1000))
                content = await self._call_llm_with_retry(prompt, max_tokens=per_chunk_max_tokens)
                try:
                    parsed = json.loads(content)
                    partial = parsed.get(kind, [])
                    partials.append(partial)
                except Exception:
                    # if parsing failed, store raw content as a fallback
                    partials.append(content)
            except Exception as e:
                logger.warning("Chunk LLM call failed; continuing to next chunk", error=str(e))
                # continue with other chunks

        # Merge partials into final concise list
        merged = await self._merge_partials(partials, domain, kind, description, max_tokens=merge_max_tokens)
        return merged

    # ---------- End new helpers ----------

    async def generate_insights(self, json_data: Dict[str, Any], description: str) -> Dict[str, Any]:
        try:
            # Use smart sampling first
            sampling_result = self._smart_sample_data(json_data, max_rows=150)
            sampled_data = sampling_result["sampled_data"]
            sampling_metadata = sampling_result["metadata"]
            
            truncated_description = self._truncate_text(description)
            sampled_json = json.dumps(sampled_data)

            logger.info("Starting insight generation with smart sampling", 
                       json_length=len(sampled_json),
                       sampling_strategy=sampling_metadata.get("strategy"),
                       total_rows=sampling_metadata.get("total_rows", 0),
                       sampled_rows=sampling_metadata.get("sampled_rows", 0),
                       column_info=sampling_metadata.get("column_info", {}))

            workflow = StateGraph(GraphState)

            # Classification node
            async def classify_spreadsheet(state: GraphState) -> GraphState:
                try:
                    # Use sampled data for classification
                    sample_for_classification = state['json_data'][:5] if isinstance(state['json_data'], list) else list(state['json_data'].values())[:5]
                    
                    prompt = f"""
                    Classify the spreadsheet as one of: {', '.join(self.types)}.
                    Use description and sample data. If unclear, use 'Unknown'.
                    
                    Description: {state['description']}
                    Sample Data (JSON): {json.dumps(sample_for_classification)}
                    
                    Return: {{"type": "Finance"}}  # Example; must be exact match
                    """
                    content = await self._call_llm_with_retry(prompt, max_tokens=50)
                    parsed = json.loads(content)
                    state_type = parsed.get('type', 'Unknown')
                    if state_type not in self.types + ['Unknown']:
                        state_type = 'Unknown'
                    state['spreadsheet_type'] = state_type
                    logger.info("Classified type", type=state_type)
                except Exception as e:
                    logger.error("Classification failed", error=str(e))
                    state['spreadsheet_type'] = 'Unknown'
                return state

            # ---------- Domain-specific nodes (now using chunking + merge) ----------
            # Finance-specific nodes
            async def analyze_finance_trends(state: GraphState) -> GraphState:
                # Chunk data conservatively to avoid context overflow
                chunks = self._chunk_json_data_by_tokens(state['json_data'], max_input_tokens=8000)
                prompt_template = """
                Analyze financial data for 2-3 key trends, e.g., revenue growth, expense patterns, ROI, cash flow changes.
                Include quantitative metrics where possible (e.g., 'Revenue grew 12% YoY').
                Data: {data}
                Description: {description}
                Return: {{"trends": ["Trend 1 with metric", "Trend 2"]}}
                """
                merged = await self._process_chunks_collect_and_merge(chunks, domain="finance", kind="trends", prompt_template=prompt_template, description=state['description'])
                state['insights']['trends'] = merged
                return state

            async def analyze_finance_anomalies(state: GraphState) -> GraphState:
                chunks = self._chunk_json_data_by_tokens(state['json_data'], max_input_tokens=8000)
                prompt_template = """
                Detect 1-2 financial anomalies, e.g., unusual expense spikes, budget overruns, irregular cash flows.
                Explain potential causes.
                Data: {data}
                Description: {description}
                Return: {{"anomalies": ["Anomaly 1 explanation", "Anomaly 2"]}}
                """
                merged = await self._process_chunks_collect_and_merge(chunks, domain="finance", kind="anomalies", prompt_template=prompt_template, description=state['description'])
                state['insights']['anomalies'] = merged
                return state

            async def generate_finance_predictions(state: GraphState) -> GraphState:
                chunks = self._chunk_json_data_by_tokens(state['json_data'], max_input_tokens=8000)
                prompt_template = """
                Generate 1-2 financial predictions/recommendations, e.g., forecast revenue, suggest cost cuts, risk assessments.
                Data: {data}
                Description: {description}
                Return: {{"predictions": ["Prediction 1", "Prediction 2"]}}
                """
                merged = await self._process_chunks_collect_and_merge(chunks, domain="finance", kind="predictions", prompt_template=prompt_template, description=state['description'])
                state['insights']['predictions'] = merged
                return state
            
            # HR-specific nodes
            async def analyze_hr_trends(state: GraphState) -> GraphState:
                chunks = self._chunk_json_data_by_tokens(state['json_data'], max_input_tokens=8000)
                prompt_template = """
                Analyze HR data for 2-3 key trends, e.g., employee turnover rates, hiring patterns, salary progression, 
                performance ratings distribution, training completion rates, diversity metrics.
                Include quantitative insights where possible.
                Data: {data}
                Description: {description}
                Return: {{"trends": ["HR trend 1 with metric", "HR trend 2"]}}
                """
                merged = await self._process_chunks_collect_and_merge(chunks, domain="hr", kind="trends", prompt_template=prompt_template, description=state['description'])
                state['insights']['trends'] = merged
                return state

            async def analyze_hr_anomalies(state: GraphState) -> GraphState:
                chunks = self._chunk_json_data_by_tokens(state['json_data'], max_input_tokens=8000)
                prompt_template = """
                Detect 1-2 HR anomalies, e.g., sudden turnover spikes in specific departments, unusual hiring patterns,
                salary disparities, performance rating inconsistencies.
                Data: {data}
                Description: {description}
                Return: {{"anomalies": ["HR anomaly 1 explanation", "HR anomaly 2"]}}
                """
                merged = await self._process_chunks_collect_and_merge(chunks, domain="hr", kind="anomalies", prompt_template=prompt_template, description=state['description'])
                state['insights']['anomalies'] = merged
                return state

            async def generate_hr_predictions(state: GraphState) -> GraphState:
                chunks = self._chunk_json_data_by_tokens(state['json_data'], max_input_tokens=8000)
                prompt_template = """
                Generate 1-2 HR predictions/recommendations, e.g., forecast hiring needs, retention strategies.
                Data: {data}
                Description: {description}
                Return: {{"predictions": ["HR prediction 1", "HR prediction 2"]}}
                """
                merged = await self._process_chunks_collect_and_merge(chunks, domain="hr", kind="predictions", prompt_template=prompt_template, description=state['description'])
                state['insights']['predictions'] = merged
                return state

            # Operations-specific nodes
            async def analyze_operations_trends(state: GraphState) -> GraphState:
                chunks = self._chunk_json_data_by_tokens(state['json_data'], max_input_tokens=8000)
                prompt_template = """
                Analyze operations data for 2-3 key trends, e.g., production efficiency, supply chain performance, downtime.
                Data: {data}
                Description: {description}
                Return: {{"trends": ["Operations trend 1 with metric", "Operations trend 2"]}}
                """
                merged = await self._process_chunks_collect_and_merge(chunks, domain="operations", kind="trends", prompt_template=prompt_template, description=state['description'])
                state['insights']['trends'] = merged
                return state

            async def analyze_operations_anomalies(state: GraphState) -> GraphState:
                chunks = self._chunk_json_data_by_tokens(state['json_data'], max_input_tokens=8000)
                prompt_template = """
                Detect 1-2 operations anomalies, e.g., unexpected equipment failures, supply chain disruptions.
                Data: {data}
                Description: {description}
                Return: {{"anomalies": ["Operations anomaly 1 explanation", "Operations anomaly 2"]}}
                """
                merged = await self._process_chunks_collect_and_merge(chunks, domain="operations", kind="anomalies", prompt_template=prompt_template, description=state['description'])
                state['insights']['anomalies'] = merged
                return state

            async def generate_operations_predictions(state: GraphState) -> GraphState:
                chunks = self._chunk_json_data_by_tokens(state['json_data'], max_input_tokens=8000)
                prompt_template = """
                Generate 1-2 operations predictions/recommendations, e.g., maintenance scheduling, capacity forecasts.
                Data: {data}
                Description: {description}
                Return: {{"predictions": ["Operations prediction 1", "Operations prediction 2"]}}
                """
                merged = await self._process_chunks_collect_and_merge(chunks, domain="operations", kind="predictions", prompt_template=prompt_template, description=state['description'])
                state['insights']['predictions'] = merged
                return state

            # Sales-specific nodes
            async def analyze_sales_trends(state: GraphState) -> GraphState:
                chunks = self._chunk_json_data_by_tokens(state['json_data'], max_input_tokens=8000)
                prompt_template = """
                Analyze sales data for 2-3 key trends, e.g., revenue growth, conversion rates, product performance.
                Data: {data}
                Description: {description}
                Return: {{"trends": ["Sales trend 1 with metric", "Sales trend 2"]}}
                """
                merged = await self._process_chunks_collect_and_merge(chunks, domain="sales", kind="trends", prompt_template=prompt_template, description=state['description'])
                state['insights']['trends'] = merged
                return state

            async def analyze_sales_anomalies(state: GraphState) -> GraphState:
                chunks = self._chunk_json_data_by_tokens(state['json_data'], max_input_tokens=8000)
                prompt_template = """
                Detect 1-2 sales anomalies, e.g., sudden drops in specific products/regions, unusual customer behavior.
                Data: {data}
                Description: {description}
                Return: {{"anomalies": ["Sales anomaly 1 explanation", "Sales anomaly 2"]}}
                """
                merged = await self._process_chunks_collect_and_merge(chunks, domain="sales", kind="anomalies", prompt_template=prompt_template, description=state['description'])
                state['insights']['anomalies'] = merged
                return state

            async def generate_sales_predictions(state: GraphState) -> GraphState:
                chunks = self._chunk_json_data_by_tokens(state['json_data'], max_input_tokens=8000)
                prompt_template = """
                Generate 1-2 sales predictions/recommendations, e.g., forecast revenue, pricing recommendations.
                Data: {data}
                Description: {description}
                Return: {{"predictions": ["Sales prediction 1", "Sales prediction 2"]}}
                """
                merged = await self._process_chunks_collect_and_merge(chunks, domain="sales", kind="predictions", prompt_template=prompt_template, description=state['description'])
                state['insights']['predictions'] = merged
                return state

            # Retail-specific nodes
            async def analyze_retail_trends(state: GraphState) -> GraphState:
                chunks = self._chunk_json_data_by_tokens(state['json_data'], max_input_tokens=8000)
                prompt_template = """
                Analyze retail data for 2-3 key trends, e.g., inventory turnover, customer footfall, product performance.
                Data: {data}
                Description: {description}
                Return: {{"trends": ["Retail trend 1 with metric", "Retail trend 2"]}}
                """
                merged = await self._process_chunks_collect_and_merge(chunks, domain="retail", kind="trends", prompt_template=prompt_template, description=state['description'])
                state['insights']['trends'] = merged
                return state

            async def analyze_retail_anomalies(state: GraphState) -> GraphState:
                chunks = self._chunk_json_data_by_tokens(state['json_data'], max_input_tokens=8000)
                prompt_template = """
                Detect 1-2 retail anomalies, e.g., stockouts, slow-moving inventory, unusual customer patterns.
                Data: {data}
                Description: {description}
                Return: {{"anomalies": ["Retail anomaly 1 explanation", "Retail anomaly 2"]}}
                """
                merged = await self._process_chunks_collect_and_merge(chunks, domain="retail", kind="anomalies", prompt_template=prompt_template, description=state['description'])
                state['insights']['anomalies'] = merged
                return state

            async def generate_retail_predictions(state: GraphState) -> GraphState:
                chunks = self._chunk_json_data_by_tokens(state['json_data'], max_input_tokens=8000)
                prompt_template = """
                Generate 1-2 retail predictions/recommendations, e.g., inventory optimization, demand forecasting.
                Data: {data}
                Description: {description}
                Return: {{"predictions": ["Retail prediction 1", "Retail prediction 2"]}}
                """
                merged = await self._process_chunks_collect_and_merge(chunks, domain="retail", kind="predictions", prompt_template=prompt_template, description=state['description'])
                state['insights']['predictions'] = merged
                return state

            # Generic fallback nodes
            async def analyze_generic_trends(state: GraphState) -> GraphState:
                chunks = self._chunk_json_data_by_tokens(state['json_data'], max_input_tokens=8000)
                prompt_template = """
                Identify 2-3 key trends in the data. Look for patterns, growth/decline, changes over time,
                distributions, or notable characteristics in the dataset.
                Data: {data}
                Description: {description}
                Return: {{"trends": ["Generic trend 1", "Generic trend 2"]}}
                """
                merged = await self._process_chunks_collect_and_merge(chunks, domain="generic", kind="trends", prompt_template=prompt_template, description=state['description'])
                state['insights']['trends'] = merged
                return state

            async def analyze_generic_anomalies(state: GraphState) -> GraphState:
                chunks = self._chunk_json_data_by_tokens(state['json_data'], max_input_tokens=8000)
                prompt_template = """
                Detect 1-2 anomalies or outliers in the data.
                Data: {data}
                Description: {description}
                Return: {{"anomalies": ["Generic anomaly 1", "Generic anomaly 2"]}}
                """
                merged = await self._process_chunks_collect_and_merge(chunks, domain="generic", kind="anomalies", prompt_template=prompt_template, description=state['description'])
                state['insights']['anomalies'] = merged
                return state

            async def generate_generic_predictions(state: GraphState) -> GraphState:
                chunks = self._chunk_json_data_by_tokens(state['json_data'], max_input_tokens=8000)
                prompt_template = """
                Generate 1-2 predictions or recommendations based on the data patterns.
                Data: {data}
                Description: {description}
                Return: {{"predictions": ["Generic prediction 1", "Generic prediction 2"]}}
                """
                merged = await self._process_chunks_collect_and_merge(chunks, domain="generic", kind="predictions", prompt_template=prompt_template, description=state['description'])
                state['insights']['predictions'] = merged
                return state

            # Add nodes to workflow
            workflow.add_node("classify", classify_spreadsheet)
            
            # Finance nodes
            workflow.add_node("analyze_finance_trends", analyze_finance_trends)
            workflow.add_node("analyze_finance_anomalies", analyze_finance_anomalies)
            workflow.add_node("generate_finance_predictions", generate_finance_predictions)

            # HR nodes
            workflow.add_node("analyze_hr_trends", analyze_hr_trends)
            workflow.add_node("analyze_hr_anomalies", analyze_hr_anomalies)
            workflow.add_node("generate_hr_predictions", generate_hr_predictions)

            # Operations nodes
            workflow.add_node("analyze_operations_trends", analyze_operations_trends)
            workflow.add_node("analyze_operations_anomalies", analyze_operations_anomalies)
            workflow.add_node("generate_operations_predictions", generate_operations_predictions)

            # Sales nodes
            workflow.add_node("analyze_sales_trends", analyze_sales_trends)
            workflow.add_node("analyze_sales_anomalies", analyze_sales_anomalies)
            workflow.add_node("generate_sales_predictions", generate_sales_predictions)

            # Retail nodes
            workflow.add_node("analyze_retail_trends", analyze_retail_trends)
            workflow.add_node("analyze_retail_anomalies", analyze_retail_anomalies)
            workflow.add_node("generate_retail_predictions", generate_retail_predictions)

            # Generic fallback nodes
            workflow.add_node("analyze_generic_trends", analyze_generic_trends)
            workflow.add_node("analyze_generic_anomalies", analyze_generic_anomalies)
            workflow.add_node("generate_generic_predictions", generate_generic_predictions)

            # Conditional routing based on type
            def route_after_classify(state: GraphState):
                spreadsheet_type = state['spreadsheet_type'].lower()
                if spreadsheet_type == 'finance':
                    return "analyze_finance_trends"
                elif spreadsheet_type == 'hr':
                    return "analyze_hr_trends"
                elif spreadsheet_type == 'operations':
                    return "analyze_operations_trends"
                elif spreadsheet_type == 'sales':
                    return "analyze_sales_trends"
                elif spreadsheet_type == 'retail':
                    return "analyze_retail_trends"
                else:  # Unknown or any other type
                    return "analyze_generic_trends"

            # Set up the workflow structure
            workflow.set_entry_point("classify")
            workflow.add_conditional_edges("classify", route_after_classify)

            # Chain edges for each domain (trends -> anomalies -> predictions -> END)
            
            # Finance chain
            workflow.add_edge("analyze_finance_trends", "analyze_finance_anomalies")
            workflow.add_edge("analyze_finance_anomalies", "generate_finance_predictions")
            workflow.add_edge("generate_finance_predictions", END)

            # HR chain
            workflow.add_edge("analyze_hr_trends", "analyze_hr_anomalies")
            workflow.add_edge("analyze_hr_anomalies", "generate_hr_predictions")
            workflow.add_edge("generate_hr_predictions", END)

            # Operations chain
            workflow.add_edge("analyze_operations_trends", "analyze_operations_anomalies")
            workflow.add_edge("analyze_operations_anomalies", "generate_operations_predictions")
            workflow.add_edge("generate_operations_predictions", END)

            # Sales chain
            workflow.add_edge("analyze_sales_trends", "analyze_sales_anomalies")
            workflow.add_edge("analyze_sales_anomalies", "generate_sales_predictions")
            workflow.add_edge("generate_sales_predictions", END)

            # Retail chain
            workflow.add_edge("analyze_retail_trends", "analyze_retail_anomalies")
            workflow.add_edge("analyze_retail_anomalies", "generate_retail_predictions")
            workflow.add_edge("generate_retail_predictions", END)

            # Generic chain
            workflow.add_edge("analyze_generic_trends", "analyze_generic_anomalies")
            workflow.add_edge("analyze_generic_anomalies", "generate_generic_predictions")
            workflow.add_edge("generate_generic_predictions", END)

            # Compile and execute the workflow
            graph = workflow.compile()
            initial_state = GraphState(
                json_data=sampled_data,
                description=truncated_description,
                spreadsheet_type='Unknown',
                insights={}
            )
            
            result = await graph.ainvoke(initial_state)
            logger.info("Insight generation completed", 
                       classified_type=result.get("spreadsheet_type", "Unknown"),
                       insights_keys=list(result.get("insights", {}).keys()),
                       sampling_metadata=sampling_metadata)
            
            # Add sampling metadata to the final insights for transparency
            final_insights = result.get("insights", {
                "trends": ["Error generating insights"],
                "anomalies": ["Error generating insights"],
                "predictions": ["Error generating predictions"]
            })
            
            # Include sampling information in the response
            final_insights["_metadata"] = {
                "sampling_applied": sampling_metadata.get("strategy") not in ["no_sampling_needed", "full_data"],
                "total_rows_analyzed": sampling_metadata.get("total_rows", 0),
                "sampled_rows_used": sampling_metadata.get("sampled_rows", 0),
                "columns_prioritized": sampling_metadata.get("column_info", {}).get("kept_columns", 0),
                "sampling_strategy": sampling_metadata.get("strategy", "unknown")
            }
            
            return final_insights
            
        except Exception as e:
            logger.error("Insight generation failed", error=str(e))
            return {
                "trends": ["Error analyzing trends"],
                "anomalies": ["Error analyzing anomalies"],
                "predictions": ["Error generating predictions"]
            }
