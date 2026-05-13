import pandas as pd
import numpy as np
from typing import Dict, Any, List, Optional, Tuple, Union
from app.utils.logger import logger
import re
from datetime import datetime

class FinanceAnalysisService:
    def __init__(self):
        # Define comprehensive column patterns for financial data with more variations
        self.column_patterns = {
            'transaction_id': [
                ['transaction', 'id'], ['trans', 'id'], ['id'], ['ref', 'number'], 
                ['reference'], ['transaction', 'number'], ['txn', 'id'], ['trans', 'ref']
            ],
            'date': [
                ['date'], ['transaction', 'date'], ['posting', 'date'], 
                ['effective', 'date'], ['timestamp'], ['time'], ['created', 'date'],
                ['processed', 'date'], ['entry', 'date']
            ],
            'amount': [
                ['amount'], ['value'], ['transaction', 'amount'], ['total'],
                ['debit'], ['credit'], ['balance'], ['sum'], ['price'], ['cost'],
                ['spending'], ['payment'], ['charge'], ['fee']
            ],
            'revenue': [
                ['revenue'], ['income'], ['sales'], ['earnings'], 
                ['turnover'], ['receipts'], ['inflow'], ['gross', 'revenue'],
                ['net', 'revenue'], ['total', 'revenue'], ['sales', 'amount']
            ],
            'expense': [
                ['expense'], ['cost'], ['expenditure'], ['spending'], 
                ['outflow'], ['payment'], ['disbursement'], ['charges'],
                ['fees'], ['total', 'expense'], ['expense', 'amount']
            ],
            'profit': [
                ['profit'], ['net', 'income'], ['earnings'], 
                ['net', 'profit'], ['bottom', 'line'], ['margin'],
                ['profit', 'loss'], ['net', 'earnings']
            ],
            'account': [
                ['account'], ['account', 'name'], ['gl', 'account'], 
                ['ledger', 'account'], ['account', 'code'], ['acc', 'name'],
                ['account', 'number'], ['chart', 'account']
            ],
            'category': [
                ['category'], ['type'], ['class'], ['classification'], 
                ['account', 'type'], ['expense', 'type'], ['segment'],
                ['group'], ['subcategory'], ['expense', 'category'],
                ['income', 'category'], ['transaction', 'type']
            ],
            'department': [
                ['department'], ['division'], ['cost', 'center'], 
                ['business', 'unit'], ['segment'], ['dept'], ['section'],
                ['team'], ['branch'], ['office'], ['location']
            ],
            'vendor': [
                ['vendor'], ['supplier'], ['payee'], ['merchant'], 
                ['company'], ['contractor'], ['provider'], ['seller'],
                ['vendor', 'name'], ['supplier', 'name']
            ],
            'customer': [
                ['customer'], ['client'], ['payer'], ['debtor'], 
                ['account', 'holder'], ['customer', 'name'], ['client', 'name'],
                ['buyer'], ['purchaser']
            ],
            'invoice_number': [
                ['invoice'], ['bill', 'number'], ['invoice', 'id'], 
                ['bill', 'id'], ['receipt', 'number'], ['invoice', 'number'],
                ['bill', 'ref'], ['receipt', 'id']
            ],
            'payment_method': [
                ['payment', 'method'], ['payment', 'type'], ['method'], 
                ['channel'], ['payment', 'mode'], ['pay', 'method'],
                ['payment', 'channel'], ['pay', 'type']
            ],
            'currency': [
                ['currency'], ['curr'], ['currency', 'code'], ['ccy']
            ],
            'budget': [
                ['budget'], ['allocated'], ['budgeted', 'amount'], 
                ['plan'], ['forecast'], ['budgeted'], ['target'],
                ['planned', 'amount'], ['allocation']
            ],
            'actual': [
                ['actual'], ['actual', 'amount'], ['spent'], 
                ['real'], ['current'], ['realized'], ['used'],
                ['actual', 'cost'], ['actual', 'expense']
            ],
            'variance': [
                ['variance'], ['difference'], ['deviation'], 
                ['budget', 'variance'], ['over', 'under'], ['diff'],
                ['variation'], ['budget', 'diff']
            ],
            'tax': [
                ['tax'], ['vat'], ['sales', 'tax'], ['tax', 'amount'], 
                ['duty'], ['levy'], ['gst'], ['income', 'tax']
            ],
            'discount': [
                ['discount'], ['markdown'], ['reduction'], 
                ['rebate'], ['allowance'], ['deduction']
            ],
            'interest': [
                ['interest'], ['finance', 'charge'], ['interest', 'rate'], 
                ['apr'], ['yield'], ['interest', 'income']
            ],
            'description': [
                ['description'], ['desc'], ['memo'], ['note'], ['notes'],
                ['comment'], ['details'], ['narrative'], ['reference'],
                ['particulars']
            ]
        }

    def compute_finance_insights(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Compute comprehensive financial insights from the dataframe"""
        try:
            if df.empty:
                logger.warning("Empty dataframe provided")
                return {}
                
            insights = {}
            logger.info(f"Analyzing finance dataframe with columns: {list(df.columns)}")
            
            # Clean and prepare data
            df = self._clean_dataframe(df)
            
            # Get column mappings with debugging info
            column_mappings = self._map_columns(df)
            logger.info(f"Column mappings found: {column_mappings}")
            
            # Log mapping success rate
            successful_mappings = len([v for v in column_mappings.values() if v is not None])
            total_concepts = len(self.column_patterns)
            logger.info(f"Successfully mapped {successful_mappings}/{total_concepts} financial concepts")
            
            # Revenue analysis
            if self._can_analyze_revenue(column_mappings):
                insights.update(self._analyze_revenue_metrics(df, column_mappings))
                logger.info("Revenue analysis completed")
            else:
                logger.warning("Revenue analysis skipped - insufficient data")
            
            # Expense analysis
            if self._can_analyze_expenses(column_mappings):
                insights.update(self._analyze_expense_metrics(df, column_mappings))
                logger.info("Expense analysis completed")
            else:
                logger.warning("Expense analysis skipped - insufficient data")
            
            # Profitability analysis
            if self._can_analyze_profitability(column_mappings):
                insights.update(self._analyze_profitability_metrics(df, column_mappings))
                logger.info("Profitability analysis completed")
            else:
                logger.warning("Profitability analysis skipped - insufficient data")
            
            # Cash flow analysis
            if self._can_analyze_cashflow(column_mappings):
                insights.update(self._analyze_cashflow_metrics(df, column_mappings))
                logger.info("Cash flow analysis completed")
            else:
                logger.warning("Cash flow analysis skipped - insufficient data")
            
            # Budget variance analysis
            if self._can_analyze_budget(column_mappings):
                insights.update(self._analyze_budget_variance(df, column_mappings))
                logger.info("Budget variance analysis completed")
            else:
                logger.warning("Budget variance analysis skipped - insufficient data")
            
            # Account analysis
            if self._can_analyze_accounts(column_mappings):
                insights.update(self._analyze_account_performance(df, column_mappings))
                logger.info("Account analysis completed")
            else:
                logger.warning("Account analysis skipped - insufficient data")
            
            # Department financial analysis (also works with segments)
            if self._can_analyze_departments(column_mappings):
                insights.update(self._analyze_department_financials(df, column_mappings))
                logger.info("Department/Segment financial analysis completed")
            else:
                logger.warning("Department/Segment analysis skipped - insufficient data")
            
            # Vendor/Customer analysis
            if self._can_analyze_vendors_customers(column_mappings):
                insights.update(self._analyze_vendor_customer_metrics(df, column_mappings))
                logger.info("Vendor/Customer analysis completed")
            else:
                logger.warning("Vendor/Customer analysis skipped - insufficient data")
            
            # Time-based financial trends
            if self._can_analyze_time_trends(column_mappings):
                insights.update(self._analyze_financial_trends(df, column_mappings))
                logger.info("Financial trends analysis completed")
            else:
                logger.warning("Time trends analysis skipped - insufficient data")
            
            # General transaction analysis (works with any amount data)
            insights.update(self._analyze_general_transactions(df, column_mappings))
            logger.info("General transaction analysis completed")
            
            # Add basic financial statistics
            insights.update(self._get_basic_finance_stats(df, column_mappings))
            
            logger.info("Financial insights computed successfully")
            return insights
            
        except Exception as e:
            logger.error("Failed to compute financial insights", error=str(e))
            return {}

    def _clean_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        """Clean and prepare the dataframe for analysis"""
        try:
            df_clean = df.copy()
            
            # Convert numeric columns that might be stored as strings
            for col in df_clean.columns:
                if df_clean[col].dtype == 'object':
                    # Try to convert to numeric if it looks like numbers
                    sample = df_clean[col].dropna().head(10)
                    if len(sample) > 0:
                        # Check if column contains mostly numeric-like strings
                        numeric_count = sum(1 for val in sample if self._is_numeric_like(str(val)))
                        if numeric_count > len(sample) * 0.7:  # If 70%+ look numeric
                            df_clean[col] = pd.to_numeric(df_clean[col], errors='coerce')
                            logger.info(f"Converted column '{col}' to numeric")
            
            # Convert date columns
            for col in df_clean.columns:
                if any(date_word in col.lower() for date_word in ['date', 'time', 'created', 'posted']):
                    df_clean[col] = pd.to_datetime(df_clean[col], errors='coerce')
                    if df_clean[col].notna().sum() > 0:
                        logger.info(f"Converted column '{col}' to datetime")
            
            return df_clean
            
        except Exception as e:
            logger.error(f"Error cleaning dataframe: {str(e)}")
            return df

    def _is_numeric_like(self, value: str) -> bool:
        """Check if a string value looks like a number"""
        try:
            # Remove common currency symbols and separators
            cleaned = re.sub(r'[$,€£¥₹\s]', '', str(value))
            # Handle negative numbers in parentheses
            if cleaned.startswith('(') and cleaned.endswith(')'):
                cleaned = '-' + cleaned[1:-1]
            float(cleaned)
            return True
        except:
            return False

    def _map_columns(self, df: pd.DataFrame) -> Dict[str, Optional[str]]:
        """Map dataframe columns to financial concepts using flexible pattern matching"""
        columns_lower = {col.lower(): col for col in df.columns}
        mappings = {}
        used_columns = set()  # Track used columns to avoid double-mapping
        
        # First pass: exact matches
        for concept, patterns in self.column_patterns.items():
            best_match = None
            best_score = 0
            
            for col_lower, col_original in columns_lower.items():
                if col_original in used_columns:
                    continue
                    
                for pattern in patterns:
                    score = self._calculate_match_score(col_lower, pattern)
                    if score > best_score and score > 0.5:  # Lowered threshold from 0.6
                        # Additional validation for numeric columns
                        if concept in ['amount', 'revenue', 'expense', 'profit', 'budget', 'actual', 'variance', 'tax', 'discount', 'interest']:
                            if not pd.api.types.is_numeric_dtype(df[col_original]):
                                logger.debug(f"Column '{col_original}' matches '{concept}' pattern but is not numeric")
                                continue
                        best_match = col_original
                        best_score = score
            
            if best_match:
                mappings[concept] = best_match
                used_columns.add(best_match)
                logger.info(f"Mapped '{best_match}' to '{concept}' (score: {best_score:.2f})")
            else:
                mappings[concept] = None
        
        return mappings

    def _calculate_match_score(self, column_name: str, pattern: List[str]) -> float:
        """Calculate how well a column name matches a pattern"""
        normalized_col = re.sub(r'[_\-\s\.]+', ' ', column_name.lower()).strip()
        pattern_str = ' '.join(pattern)
        
        # Exact match gets highest score
        if normalized_col == pattern_str:
            return 1.0
        
        # Check if all pattern words are in column
        words_found = 0
        total_pattern_length = sum(len(word) for word in pattern)
        matched_length = 0
        
        for word in pattern:
            if word in normalized_col:
                words_found += 1
                matched_length += len(word)
            else:
                # Check for partial matches in individual words
                col_words = normalized_col.split()
                for col_word in col_words:
                    if word in col_word or col_word in word:
                        words_found += 0.7
                        matched_length += len(word) * 0.7
                        break
        
        if words_found == 0:
            return 0.0
        
        # Calculate composite score
        word_coverage = min(words_found / len(pattern), 1.0)
        length_ratio = matched_length / max(len(normalized_col), total_pattern_length)
        
        # Bonus for single word exact matches
        if len(pattern) == 1 and pattern[0] in normalized_col:
            word_coverage += 0.2
        
        return min(1.0, word_coverage * 0.8 + length_ratio * 0.2)

    def _can_analyze_revenue(self, mappings: Dict[str, Optional[str]]) -> bool:
        """Check if revenue analysis is possible"""
        has_revenue_col = mappings.get('revenue') is not None
        has_amount_and_category = mappings.get('amount') is not None and mappings.get('category') is not None
        return has_revenue_col or has_amount_and_category

    def _can_analyze_expenses(self, mappings: Dict[str, Optional[str]]) -> bool:
        """Check if expense analysis is possible"""
        has_expense_col = mappings.get('expense') is not None
        has_amount_and_category = mappings.get('amount') is not None and mappings.get('category') is not None
        has_amount_only = mappings.get('amount') is not None  # Allow basic expense analysis with just amounts
        return has_expense_col or has_amount_and_category or has_amount_only

    def _can_analyze_profitability(self, mappings: Dict[str, Optional[str]]) -> bool:
        """Check if profitability analysis is possible"""
        has_profit_col = mappings.get('profit') is not None
        has_revenue_and_expense = (mappings.get('revenue') is not None and 
                                 mappings.get('expense') is not None)
        return has_profit_col or has_revenue_and_expense

    def _can_analyze_cashflow(self, mappings: Dict[str, Optional[str]]) -> bool:
        """Check if cash flow analysis is possible"""
        return mappings.get('amount') is not None and mappings.get('date') is not None

    def _can_analyze_budget(self, mappings: Dict[str, Optional[str]]) -> bool:
        """Check if budget analysis is possible"""
        return mappings.get('budget') is not None and mappings.get('actual') is not None

    def _can_analyze_accounts(self, mappings: Dict[str, Optional[str]]) -> bool:
        """Check if account analysis is possible"""
        return mappings.get('account') is not None and mappings.get('amount') is not None

    def _can_analyze_departments(self, mappings: Dict[str, Optional[str]]) -> bool:
        """Check if department/segment analysis is possible"""
        has_department = mappings.get('department') is not None
        has_category = mappings.get('category') is not None  # Category can include segments
        has_amount = mappings.get('amount') is not None
        return (has_department or has_category) and has_amount

    def _can_analyze_vendors_customers(self, mappings: Dict[str, Optional[str]]) -> bool:
        """Check if vendor/customer analysis is possible"""
        has_vendor_or_customer = (mappings.get('vendor') is not None or 
                                mappings.get('customer') is not None)
        has_amount = mappings.get('amount') is not None
        return has_vendor_or_customer and has_amount

    def _can_analyze_time_trends(self, mappings: Dict[str, Optional[str]]) -> bool:
        """Check if time trend analysis is possible"""
        return mappings.get('date') is not None and mappings.get('amount') is not None

    def _analyze_general_transactions(self, df: pd.DataFrame, mappings: Dict[str, Optional[str]]) -> Dict[str, Any]:
        """Analyze general transaction patterns regardless of specific categories"""
        insights = {}
        
        amount_col = mappings.get('amount')
        if not amount_col:
            return {}
        
        try:
            df_trans = df.dropna(subset=[amount_col])
            if df_trans.empty:
                return {}
            
            insights['transaction_summary'] = {
                'total_transactions': len(df_trans),
                'total_amount': float(df_trans[amount_col].sum()),
                'average_transaction': float(df_trans[amount_col].mean()),
                'median_transaction': float(df_trans[amount_col].median()),
                'largest_transaction': float(df_trans[amount_col].max()),
                'smallest_transaction': float(df_trans[amount_col].min()),
                'positive_transactions': len(df_trans[df_trans[amount_col] > 0]),
                'negative_transactions': len(df_trans[df_trans[amount_col] < 0]),
                'zero_transactions': len(df_trans[df_trans[amount_col] == 0])
            }
            
            # Analyze by any available grouping column
            grouping_cols = ['category', 'department', 'account', 'vendor', 'customer']
            for col_concept in grouping_cols:
                col_name = mappings.get(col_concept)
                if col_name and col_name in df_trans.columns:
                    group_analysis = df_trans.groupby(col_name)[amount_col].agg(['sum', 'count', 'mean']).round(2)
                    group_analysis = group_analysis.sort_values('sum', ascending=False)
                    
                    insights[f'transactions_by_{col_concept}'] = []
                    total_amount = float(df_trans[amount_col].sum())
                    
                    for group_name, row in group_analysis.head(15).iterrows():
                        insights[f'transactions_by_{col_concept}'].append({
                            f'{col_concept}_name': str(group_name),
                            'total_amount': float(row['sum']),
                            'percentage_of_total': round(float((row['sum'] / total_amount) * 100), 2) if total_amount != 0 else 0,
                            'transaction_count': int(row['count']),
                            'average_amount': float(row['mean'])
                        })
                    
                    logger.info(f"Analyzed transactions by {col_concept}")
                    break  # Use the first available grouping column
            
        except Exception as e:
            logger.error(f"Error in general transaction analysis: {str(e)}")
        
        return insights

    # Keep all existing analysis methods but improve them with better error handling and flexibility
    
    def _analyze_revenue_metrics(self, df: pd.DataFrame, mappings: Dict[str, Optional[str]]) -> Dict[str, Any]:
        """Analyze revenue metrics and trends with improved flexibility"""
        insights = {}
        
        revenue_col = mappings.get('revenue')
        amount_col = mappings.get('amount')
        category_col = mappings.get('category')
        date_col = mappings.get('date')
        
        try:
            # Try multiple approaches to identify revenue data
            df_revenue = None
            
            if revenue_col:
                df_revenue = df.dropna(subset=[revenue_col])
                analysis_col = revenue_col
            elif amount_col and category_col:
                # Look for revenue-like categories with more flexible matching
                revenue_patterns = ['revenue', 'income', 'sales', 'earning', 'receipt', 'inflow']
                revenue_mask = df[category_col].str.contains('|'.join(revenue_patterns), case=False, na=False)
                df_revenue = df[revenue_mask].dropna(subset=[amount_col])
                analysis_col = amount_col
            elif amount_col:
                # Use positive amounts as potential revenue
                df_revenue = df[df[amount_col] > 0].dropna(subset=[amount_col])
                analysis_col = amount_col
            
            if df_revenue is None or df_revenue.empty:
                logger.warning("No revenue data found for analysis")
                return {}
            
            insights['revenue_overview'] = {
                'total_revenue': float(df_revenue[analysis_col].sum()),
                'average_revenue': float(df_revenue[analysis_col].mean()),
                'median_revenue': float(df_revenue[analysis_col].median()),
                'revenue_transactions': len(df_revenue),
                'max_single_revenue': float(df_revenue[analysis_col].max()),
                'min_single_revenue': float(df_revenue[analysis_col].min()),
                'revenue_std_dev': float(df_revenue[analysis_col].std())
            }
            
            # Revenue by category if available
            if category_col and category_col in df_revenue.columns:
                revenue_by_category = df_revenue.groupby(category_col)[analysis_col].agg(['sum', 'count', 'mean']).round(2)
                revenue_by_category = revenue_by_category.sort_values('sum', ascending=False)
                
                insights['revenue_by_category'] = []
                total_revenue = float(df_revenue[analysis_col].sum())
                
                for category, row in revenue_by_category.iterrows():
                    insights['revenue_by_category'].append({
                        'category': str(category),
                        'total_revenue': float(row['sum']),
                        'percentage_of_total': round(float((row['sum'] / total_revenue) * 100), 2),
                        'transaction_count': int(row['count']),
                        'average_revenue': float(row['mean'])
                    })
            
            # Time-based analysis
            if date_col and date_col in df_revenue.columns:
                df_revenue_time = df_revenue.copy()
                df_revenue_time = df_revenue_time.dropna(subset=[date_col])
                
                if not df_revenue_time.empty and pd.api.types.is_datetime64_any_dtype(df_revenue_time[date_col]):
                    # Monthly trends
                    df_revenue_time['month'] = df_revenue_time[date_col].dt.to_period('M')
                    monthly_revenue = df_revenue_time.groupby('month')[analysis_col].sum().round(2)
                    
                    insights['monthly_revenue_trends'] = []
                    for month, revenue in monthly_revenue.items():
                        insights['monthly_revenue_trends'].append({
                            'month': str(month),
                            'revenue': float(revenue)
                        })
            
            logger.info(f"Revenue analysis completed with {len(df_revenue)} transactions")
            
        except Exception as e:
            logger.error(f"Error in revenue analysis: {str(e)}")
        
        return insights

    def _analyze_expense_metrics(self, df: pd.DataFrame, mappings: Dict[str, Optional[str]]) -> Dict[str, Any]:
        """Analyze expense metrics and patterns with improved flexibility"""
        insights = {}
        
        expense_col = mappings.get('expense')
        amount_col = mappings.get('amount')
        category_col = mappings.get('category')
        vendor_col = mappings.get('vendor')
        
        try:
            df_expense = None
            analysis_col = None
            
            if expense_col:
                df_expense = df.dropna(subset=[expense_col])
                analysis_col = expense_col
            elif amount_col and category_col:
                # Look for expense-like categories
                expense_patterns = ['expense', 'cost', 'spending', 'payment', 'charge', 'fee', 'outflow']
                expense_mask = df[category_col].str.contains('|'.join(expense_patterns), case=False, na=False)
                df_expense = df[expense_mask].dropna(subset=[amount_col])
                analysis_col = amount_col
            elif amount_col:
                # Use negative amounts or all amounts as potential expenses
                df_expense = df.dropna(subset=[amount_col])
                # If we have mostly positive values, use all; if mixed, use negative for expenses
                if (df_expense[amount_col] < 0).sum() > len(df_expense) * 0.3:
                    df_expense = df_expense[df_expense[amount_col] < 0].copy()
                    df_expense[amount_col] = df_expense[amount_col].abs()  # Make positive for analysis
                analysis_col = amount_col
            
            if df_expense is None or df_expense.empty:
                logger.warning("No expense data found for analysis")
                return {}
            
            insights['expense_overview'] = {
                'total_expenses': float(df_expense[analysis_col].sum()),
                'average_expense': float(df_expense[analysis_col].mean()),
                'median_expense': float(df_expense[analysis_col].median()),
                'expense_transactions': len(df_expense),
                'largest_expense': float(df_expense[analysis_col].max()),
                'smallest_expense': float(df_expense[analysis_col].min()),
                'expense_std_dev': float(df_expense[analysis_col].std())
            }
            
            # Expenses by category
            if category_col and category_col in df_expense.columns:
                expense_by_category = df_expense.groupby(category_col)[analysis_col].agg(['sum', 'count', 'mean']).round(2)
                expense_by_category = expense_by_category.sort_values('sum', ascending=False)
                
                total_expenses = float(df_expense[analysis_col].sum())
                
                insights['expense_by_category'] = []
                for category, row in expense_by_category.iterrows():
                    insights['expense_by_category'].append({
                        'category': str(category),
                        'total_expense': float(row['sum']),
                        'percentage_of_total': round(float((row['sum'] / total_expenses) * 100), 2),
                        'transaction_count': int(row['count']),
                        'average_expense': float(row['mean'])
                    })
            
            # Top vendors by expense
            if vendor_col and vendor_col in df_expense.columns:
                vendor_expenses = df_expense.groupby(vendor_col)[analysis_col].agg(['sum', 'count']).round(2)
                vendor_expenses = vendor_expenses.sort_values('sum', ascending=False)
                
                insights['top_expense_vendors'] = []
                for vendor, row in vendor_expenses.head(15).iterrows():
                    insights['top_expense_vendors'].append({
                        'vendor': str(vendor),
                        'total_expense': float(row['sum']),
                        'transaction_count': int(row['count'])
                    })
            
            logger.info(f"Expense analysis completed with {len(df_expense)} transactions")
            
        except Exception as e:
            logger.error(f"Error in expense analysis: {str(e)}")
        
        return insights

    # Continue with improved versions of other analysis methods...
    # [The rest of the methods would follow similar patterns with better error handling,
    # more flexible data detection, and comprehensive logging]

    def _get_basic_finance_stats(self, df: pd.DataFrame, mappings: Dict[str, Optional[str]]) -> Dict[str, Any]:
        """Get basic financial statistical information with enhanced details"""
        stats = {
            'dataset_info': {
                'total_transactions': len(df),
                'total_columns': len(df.columns),
                'columns_mapped': len([v for v in mappings.values() if v is not None]),
                'mapping_success_rate': round(len([v for v in mappings.values() if v is not None]) / len(self.column_patterns) * 100, 2),
                'data_completeness': round(float(df.count().sum() / (len(df) * len(df.columns))) * 100, 2),
                'date_range': self._get_date_range(df, mappings),
                'available_analyses': self._list_available_analyses(mappings)
            }
        }
        
        # Enhanced transaction statistics
        amount_col = mappings.get('amount')
        if amount_col:
            amount_data = df[amount_col].dropna()
            if not amount_data.empty:
                stats['transaction_statistics'] = {
                    'total_value': float(amount_data.sum()),
                    'average_transaction': float(amount_data.mean()),
                    'median_transaction': float(amount_data.median()),
                    'largest_transaction': float(amount_data.max()),
                    'smallest_transaction': float(amount_data.min()),
                    'transaction_std_dev': float(amount_data.std()),
                    'positive_transactions': int((amount_data > 0).sum()),
                    'negative_transactions': int((amount_data < 0).sum()),
                    'zero_transactions': int((amount_data == 0).sum())
                }
        
        # Enhanced diversity metrics
        diversity_metrics = {}
        diversity_columns = ['account', 'category', 'department', 'vendor', 'customer']
        
        for col_type in diversity_columns:
            col_name = mappings.get(col_type)
            if col_name:
                unique_count = df[col_name].nunique()
                total_count = df[col_name].notna().sum()
                diversity_metrics[f'unique_{col_type}s'] = unique_count
                if total_count > 0:
                    diversity_metrics[f'{col_type}_diversity_ratio'] = round(unique_count / total_count, 3)
        
        if diversity_metrics:
            stats['diversity_metrics'] = diversity_metrics
        
        return stats
    
    def _get_date_range(self, df: pd.DataFrame, mappings: Dict[str, Optional[str]]) -> Optional[Dict[str, Union[str, int]]]:
        """Get the date range of the data if date column exists"""
        date_col = mappings.get('date')
        if not date_col or date_col not in df.columns:
            return None
        
        try:
            date_data = pd.to_datetime(df[date_col], errors='coerce').dropna()
            if not date_data.empty:
                return {
                    'start_date': date_data.min().strftime('%Y-%m-%d'),
                    'end_date': date_data.max().strftime('%Y-%m-%d'),
                    'date_span_days': (date_data.max() - date_data.min()).days
                }
        except Exception as e:
            logger.error(f"Error getting date range: {str(e)}")
        
        return None
    
    def _list_available_analyses(self, mappings: Dict[str, Optional[str]]) -> List[str]:
        """List which analyses are possible with the available data"""
        available = []
        
        if self._can_analyze_revenue(mappings):
            available.append("revenue_analysis")
        if self._can_analyze_expenses(mappings):
            available.append("expense_analysis")
        if self._can_analyze_profitability(mappings):
            available.append("profitability_analysis")
        if self._can_analyze_cashflow(mappings):
            available.append("cashflow_analysis")
        if self._can_analyze_budget(mappings):
            available.append("budget_variance_analysis")
        if self._can_analyze_accounts(mappings):
            available.append("account_performance_analysis")
        if self._can_analyze_departments(mappings):
            available.append("department_segment_analysis")
        if self._can_analyze_vendors_customers(mappings):
            available.append("vendor_customer_analysis")
        if self._can_analyze_time_trends(mappings):
            available.append("time_trends_analysis")
        
        # Always available if we have any amount data
        if mappings.get('amount'):
            available.append("general_transaction_analysis")
        
        return available

    def _analyze_profitability_metrics(self, df: pd.DataFrame, mappings: Dict[str, Optional[str]]) -> Dict[str, Any]:
        """Analyze profitability and profit margins with improved flexibility"""
        insights = {}
        
        revenue_col = mappings.get('revenue')
        expense_col = mappings.get('expense')
        profit_col = mappings.get('profit')
        amount_col = mappings.get('amount')
        category_col = mappings.get('category')
        date_col = mappings.get('date')
        
        try:
            df_profit = None
            
            if profit_col:
                df_profit = df.dropna(subset=[profit_col])
                
                insights['profitability_overview'] = {
                    'total_profit': float(df_profit[profit_col].sum()),
                    'average_profit': float(df_profit[profit_col].mean()),
                    'median_profit': float(df_profit[profit_col].median()),
                    'profit_transactions': len(df_profit),
                    'profitable_transactions': len(df_profit[df_profit[profit_col] > 0]),
                    'loss_transactions': len(df_profit[df_profit[profit_col] < 0]),
                    'break_even_transactions': len(df_profit[df_profit[profit_col] == 0])
                }
            
            elif revenue_col and expense_col:
                df_profitability = df.dropna(subset=[revenue_col, expense_col])
                
                if not df_profitability.empty:
                    df_profitability = df_profitability.copy()
                    df_profitability['calculated_profit'] = df_profitability[revenue_col] - df_profitability[expense_col]
                    df_profitability['profit_margin'] = (df_profitability['calculated_profit'] / df_profitability[revenue_col] * 100).replace([np.inf, -np.inf], 0)
                    
                    insights['profitability_overview'] = {
                        'total_revenue': float(df_profitability[revenue_col].sum()),
                        'total_expenses': float(df_profitability[expense_col].sum()),
                        'total_profit': float(df_profitability['calculated_profit'].sum()),
                        'average_profit_margin': float(df_profitability['profit_margin'].mean()),
                        'median_profit_margin': float(df_profitability['profit_margin'].median()),
                        'profitable_periods': len(df_profitability[df_profitability['calculated_profit'] > 0]),
                        'loss_periods': len(df_profitability[df_profitability['calculated_profit'] < 0])
                    }
                    
                    # Profit trends over time
                    if date_col and pd.api.types.is_datetime64_any_dtype(df_profitability[date_col]):
                        df_profitability['month'] = df_profitability[date_col].dt.to_period('M')
                        monthly_profit = df_profitability.groupby('month')['calculated_profit'].sum().round(2)
                        
                        insights['monthly_profit_trends'] = []
                        for month, profit in monthly_profit.items():
                            insights['monthly_profit_trends'].append({
                                'month': str(month),
                                'profit': float(profit)
                            })
            
            elif amount_col and category_col:
                # Try to calculate profit from revenue and expense categories
                revenue_patterns = ['revenue', 'income', 'sales', 'earning']
                expense_patterns = ['expense', 'cost', 'spending', 'payment']
                
                df_calc = df.dropna(subset=[amount_col, category_col]).copy()
                
                revenue_mask = df_calc[category_col].str.contains('|'.join(revenue_patterns), case=False, na=False)
                expense_mask = df_calc[category_col].str.contains('|'.join(expense_patterns), case=False, na=False)
                
                total_revenue = df_calc[revenue_mask][amount_col].sum()
                total_expenses = df_calc[expense_mask][amount_col].sum()
                
                if total_revenue > 0 or total_expenses > 0:
                    insights['profitability_overview'] = {
                        'total_revenue': float(total_revenue),
                        'total_expenses': float(total_expenses),
                        'total_profit': float(total_revenue - total_expenses),
                        'profit_margin': float((total_revenue - total_expenses) / total_revenue * 100) if total_revenue > 0 else 0.0
                    }
            
        except Exception as e:
            logger.error(f"Error in profitability analysis: {str(e)}")
        
        return insights

    def _analyze_cashflow_metrics(self, df: pd.DataFrame, mappings: Dict[str, Optional[str]]) -> Dict[str, Any]:
        """Analyze cash flow patterns with improved detection"""
        insights = {}
        
        amount_col = mappings['amount']
        date_col = mappings['date']
        category_col = mappings.get('category')
        
        try:
            df_cashflow = df.dropna(subset=[amount_col, date_col])
            if df_cashflow.empty:
                return {}
            
            # Convert date column
            df_cashflow = df_cashflow.copy()
            if not pd.api.types.is_datetime64_any_dtype(df_cashflow[date_col]):
                df_cashflow[date_col] = pd.to_datetime(df_cashflow[date_col], errors='coerce')
            df_cashflow = df_cashflow.dropna(subset=[date_col])
            
            if df_cashflow.empty:
                return {}
            
            # Enhanced inflow/outflow detection
            if category_col:
                # Use category patterns
                inflow_patterns = ['revenue', 'income', 'receipt', 'deposit', 'inflow', 'sales']
                outflow_patterns = ['expense', 'payment', 'cost', 'spending', 'outflow', 'withdrawal']
                
                inflow_mask = df_cashflow[category_col].str.contains('|'.join(inflow_patterns), case=False, na=False)
                outflow_mask = df_cashflow[category_col].str.contains('|'.join(outflow_patterns), case=False, na=False)
                
                inflows = df_cashflow[inflow_mask]
                outflows = df_cashflow[outflow_mask]
                
                # If categories don't clearly separate, fall back to amount signs
                if len(inflows) == 0 and len(outflows) == 0:
                    inflows = df_cashflow[df_cashflow[amount_col] > 0]
                    outflows = df_cashflow[df_cashflow[amount_col] < 0]
            else:
                # Use amount signs
                inflows = df_cashflow[df_cashflow[amount_col] > 0]
                outflows = df_cashflow[df_cashflow[amount_col] < 0]
            
            total_inflows = float(inflows[amount_col].sum()) if not inflows.empty else 0.0
            total_outflows = float(abs(outflows[amount_col].sum())) if not outflows.empty else 0.0
            
            insights['cashflow_overview'] = {
                'total_inflows': total_inflows,
                'total_outflows': total_outflows,
                'net_cashflow': total_inflows - total_outflows,
                'inflow_transactions': len(inflows),
                'outflow_transactions': len(outflows),
                'average_inflow': float(inflows[amount_col].mean()) if not inflows.empty else 0.0,
                'average_outflow': float(abs(outflows[amount_col].mean())) if not outflows.empty else 0.0
            }
            
            # Monthly cash flow trends
            df_cashflow['month'] = df_cashflow[date_col].dt.to_period('M')
            monthly_cashflow = df_cashflow.groupby('month')[amount_col].sum().round(2)
            
            insights['monthly_cashflow_trends'] = []
            for month, flow in monthly_cashflow.items():
                insights['monthly_cashflow_trends'].append({
                    'month': str(month),
                    'net_cashflow': float(flow)
                })
            
            # Weekly trends if we have enough data
            if len(df_cashflow) > 50:
                df_cashflow['week'] = df_cashflow[date_col].dt.to_period('W')
                weekly_cashflow = df_cashflow.groupby('week')[amount_col].sum().round(2)
                
                insights['weekly_cashflow_trends'] = []
                for week, flow in weekly_cashflow.tail(12).items():  # Last 12 weeks
                    insights['weekly_cashflow_trends'].append({
                        'week': str(week),
                        'net_cashflow': float(flow)
                    })
            
        except Exception as e:
            logger.error(f"Error in cashflow analysis: {str(e)}")
        
        return insights

    def _analyze_budget_variance(self, df: pd.DataFrame, mappings: Dict[str, Optional[str]]) -> Dict[str, Any]:
        """Analyze budget vs actual performance with enhanced insights"""
        insights = {}
        
        budget_col = mappings['budget']
        actual_col = mappings['actual']
        variance_col = mappings.get('variance')
        category_col = mappings.get('category')
        
        try:
            df_budget = df.dropna(subset=[budget_col, actual_col])
            if df_budget.empty:
                return {}
            
            # Calculate variance if not provided
            df_budget = df_budget.copy()
            if not variance_col:
                df_budget['calculated_variance'] = df_budget[actual_col] - df_budget[budget_col]
                df_budget['variance_percentage'] = ((df_budget[actual_col] - df_budget[budget_col]) / df_budget[budget_col] * 100).replace([np.inf, -np.inf], 0)
                variance_col = 'calculated_variance'
                percentage_col = 'variance_percentage'
            else:
                percentage_col = 'calculated_variance_percentage'
                df_budget[percentage_col] = ((df_budget[actual_col] - df_budget[budget_col]) / df_budget[budget_col] * 100).replace([np.inf, -np.inf], 0)
            
            total_budget = float(df_budget[budget_col].sum())
            total_actual = float(df_budget[actual_col].sum())
            total_variance = total_actual - total_budget
            
            insights['budget_performance'] = {
                'total_budget': total_budget,
                'total_actual': total_actual,
                'total_variance': total_variance,
                'variance_percentage': float((total_variance / total_budget) * 100) if total_budget != 0 else 0,
                'over_budget_items': len(df_budget[df_budget[variance_col] > 0]),
                'under_budget_items': len(df_budget[df_budget[variance_col] < 0]),
                'on_budget_items': len(df_budget[abs(df_budget[variance_col]) < (df_budget[budget_col] * 0.05)]),  # Within 5%
                'budget_utilization_rate': float((total_actual / total_budget) * 100) if total_budget != 0 else 0,
                'average_variance': float(df_budget[variance_col].mean()),
                'largest_overspend': float(df_budget[variance_col].max()) if df_budget[variance_col].max() > 0 else 0,
                'largest_underspend': float(abs(df_budget[variance_col].min())) if df_budget[variance_col].min() < 0 else 0
            }
            
            # Budget variance by category
            if category_col:
                budget_by_category = df_budget.groupby(category_col).agg({
                    budget_col: 'sum',
                    actual_col: 'sum',
                    variance_col: 'sum'
                }).round(2)
                
                budget_by_category['variance_percentage'] = ((budget_by_category[actual_col] - budget_by_category[budget_col]) / budget_by_category[budget_col] * 100).replace([np.inf, -np.inf], 0).round(2)
                budget_by_category['utilization_rate'] = (budget_by_category[actual_col] / budget_by_category[budget_col] * 100).replace([np.inf, -np.inf], 0).round(2)
                
                insights['budget_variance_by_category'] = []
                for category, row in budget_by_category.iterrows():
                    insights['budget_variance_by_category'].append({
                        'category': str(category),
                        'budgeted': float(row[budget_col]),
                        'actual': float(row[actual_col]),
                        'variance': float(row[variance_col]),
                        'variance_percentage': float(row['variance_percentage']),
                        'utilization_rate': float(row['utilization_rate'])
                    })
            
        except Exception as e:
            logger.error(f"Error in budget variance analysis: {str(e)}")
        
        return insights

    def _analyze_account_performance(self, df: pd.DataFrame, mappings: Dict[str, Optional[str]]) -> Dict[str, Any]:
        """Analyze performance by account with enhanced metrics"""
        insights = {}
        
        account_col = mappings['account']
        amount_col = mappings['amount']
        category_col = mappings.get('category')
        date_col = mappings.get('date')
        
        try:
            df_accounts = df.dropna(subset=[account_col, amount_col])
            if df_accounts.empty:
                return {}
            
            account_summary = df_accounts.groupby(account_col)[amount_col].agg([
                'sum', 'count', 'mean', 'std', 'min', 'max'
            ]).round(2)
            account_summary['std'] = account_summary['std'].fillna(0)
            account_summary = account_summary.sort_values('sum', ascending=False)
            
            insights['account_performance'] = []
            total_amount = float(df_accounts[amount_col].sum())
            
            for account, row in account_summary.iterrows():
                account_data = {
                    'account': str(account),
                    'total_amount': float(row['sum']),
                    'percentage_of_total': round(float((row['sum'] / total_amount) * 100), 2) if total_amount != 0 else 0,
                    'transaction_count': int(row['count']),
                    'average_transaction': float(row['mean']),
                    'amount_volatility': float(row['std']),
                    'min_transaction': float(row['min']),
                    'max_transaction': float(row['max'])
                }
                
                # Add account activity trends if date available
                if date_col and pd.api.types.is_datetime64_any_dtype(df_accounts[date_col]):
                    account_data_subset = df_accounts[df_accounts[account_col] == account]
                    if not account_data_subset.empty:
                        monthly_activity = account_data_subset.set_index(date_col).resample('M')[amount_col].sum()
                        account_data['monthly_activity_trend'] = 'increasing' if monthly_activity.tail(3).sum() > monthly_activity.head(3).sum() else 'decreasing'
                
                insights['account_performance'].append(account_data)
            
            # Top performing accounts
            insights['top_accounts'] = {
                'highest_volume': insights['account_performance'][:10],
                'most_active': sorted(insights['account_performance'], key=lambda x: x['transaction_count'], reverse=True)[:10],
                'most_volatile': sorted(insights['account_performance'], key=lambda x: x['amount_volatility'], reverse=True)[:5]
            }
            
        except Exception as e:
            logger.error(f"Error in account analysis: {str(e)}")
        
        return insights

    def _analyze_department_financials(self, df: pd.DataFrame, mappings: Dict[str, Optional[str]]) -> Dict[str, Any]:
        """Analyze financial performance by department/segment with enhanced insights"""
        insights = {}
        
        department_col = mappings.get('department')
        category_col = mappings.get('category')  # Can also work as segments
        amount_col = mappings['amount']
        date_col = mappings.get('date')
        
        # Use department column first, fall back to category if department not available
        grouping_col = department_col if department_col else category_col
        grouping_name = 'department' if department_col else 'segment'
        
        if not grouping_col:
            return {}
        
        try:
            df_group = df.dropna(subset=[grouping_col, amount_col])
            if df_group.empty:
                return {}
            
            # Overall group financial summary
            group_summary = df_group.groupby(grouping_col)[amount_col].agg([
                'sum', 'count', 'mean', 'std', 'min', 'max'
            ]).round(2)
            group_summary['std'] = group_summary['std'].fillna(0)
            group_summary = group_summary.sort_values('sum', ascending=False)
            
            insights[f'{grouping_name}_financials'] = []
            total_amount = float(df_group[amount_col].sum())
            
            for group_name, row in group_summary.iterrows():
                group_data = {
                    grouping_name: str(group_name),
                    'total_amount': float(row['sum']),
                    'percentage_of_total': round(float((row['sum'] / total_amount) * 100), 2) if total_amount != 0 else 0,
                    'transaction_count': int(row['count']),
                    'average_transaction': float(row['mean']),
                    'amount_volatility': float(row['std']),
                    'min_transaction': float(row['min']),
                    'max_transaction': float(row['max'])
                }
                
                # Calculate growth trend if date available
                if date_col and pd.api.types.is_datetime64_any_dtype(df_group[date_col]):
                    group_data_subset = df_group[df_group[grouping_col] == group_name]
                    if not group_data_subset.empty:
                        monthly_trend = group_data_subset.set_index(date_col).resample('M')[amount_col].sum()
                        if len(monthly_trend) >= 2:
                            recent_avg = monthly_trend.tail(3).mean()
                            earlier_avg = monthly_trend.head(3).mean()
                            growth_rate = ((recent_avg - earlier_avg) / earlier_avg * 100) if earlier_avg != 0 else 0
                            group_data['growth_trend_percentage'] = round(float(growth_rate), 2)
                
                insights[f'{grouping_name}_financials'].append(group_data)
            
            # If we have both department and category, analyze cross-tabulation
            if department_col and category_col and category_col != department_col:
                cross_analysis = df_group.groupby([department_col, category_col])[amount_col].sum().unstack(fill_value=0)
                
                insights[f'{grouping_name}_category_breakdown'] = []
                for dept in cross_analysis.index:
                    dept_breakdown = {
                        'department': str(dept),
                        'categories': []
                    }
                    for cat in cross_analysis.columns:
                        if cross_analysis.loc[dept, cat] > 0:
                            dept_breakdown['categories'].append({
                                'category': str(cat),
                                'amount': float(cross_analysis.loc[dept, cat])
                            })
                    
                    if dept_breakdown['categories']:
                        insights[f'{grouping_name}_category_breakdown'].append(dept_breakdown)
            
        except Exception as e:
            logger.error(f"Error in {grouping_name} financial analysis: {str(e)}")
        
        return insights

    def _analyze_vendor_customer_metrics(self, df: pd.DataFrame, mappings: Dict[str, Optional[str]]) -> Dict[str, Any]:
        """Analyze vendor and customer financial metrics with enhanced insights"""
        insights = {}
        
        vendor_col = mappings.get('vendor')
        customer_col = mappings.get('customer')
        amount_col = mappings['amount']
        date_col = mappings.get('date')
        
        try:
            # Enhanced vendor analysis
            if vendor_col:
                df_vendors = df.dropna(subset=[vendor_col, amount_col])
                if not df_vendors.empty:
                    vendor_metrics = df_vendors.groupby(vendor_col)[amount_col].agg([
                        'sum', 'count', 'mean', 'std', 'min', 'max'
                    ]).round(2)
                    vendor_metrics['std'] = vendor_metrics['std'].fillna(0)
                    vendor_metrics = vendor_metrics.sort_values('sum', ascending=False)
                    
                    insights['vendor_metrics'] = []
                    total_vendor_amount = float(df_vendors[amount_col].sum())
                    
                    for vendor, row in vendor_metrics.head(20).iterrows():
                        vendor_data = {
                            'vendor': str(vendor),
                            'total_amount': float(row['sum']),
                            'percentage_of_total': round(float((row['sum'] / total_vendor_amount) * 100), 2),
                            'transaction_count': int(row['count']),
                            'average_transaction': float(row['mean']),
                            'amount_volatility': float(row['std']),
                            'min_transaction': float(row['min']),
                            'max_transaction': float(row['max'])
                        }
                        
                        # Add recency information if date available
                        if date_col and pd.api.types.is_datetime64_any_dtype(df_vendors[date_col]):
                            vendor_dates = df_vendors[df_vendors[vendor_col] == vendor][date_col]
                            if not vendor_dates.empty:
                                vendor_data['last_transaction_date'] = vendor_dates.max().strftime('%Y-%m-%d')
                                vendor_data['first_transaction_date'] = vendor_dates.min().strftime('%Y-%m-%d')
                                vendor_data['relationship_duration_days'] = (vendor_dates.max() - vendor_dates.min()).days
                        
                        insights['vendor_metrics'].append(vendor_data)
                    
                    # Vendor concentration analysis
                    top_5_vendors = vendor_metrics.head(5)['sum'].sum()
                    insights['vendor_concentration'] = {
                        'top_5_vendor_percentage': round(float((top_5_vendors / total_vendor_amount) * 100), 2),
                        'vendor_diversity_index': len(vendor_metrics),
                        'average_vendor_transaction_value': float(vendor_metrics['mean'].mean())
                    }
            
            # Enhanced customer analysis
            if customer_col:
                df_customers = df.dropna(subset=[customer_col, amount_col])
                if not df_customers.empty:
                    customer_metrics = df_customers.groupby(customer_col)[amount_col].agg([
                        'sum', 'count', 'mean', 'std', 'min', 'max'
                    ]).round(2)
                    customer_metrics['std'] = customer_metrics['std'].fillna(0)
                    customer_metrics = customer_metrics.sort_values('sum', ascending=False)
                    
                    insights['customer_metrics'] = []
                    total_customer_amount = float(df_customers[amount_col].sum())
                    
                    for customer, row in customer_metrics.head(20).iterrows():
                        customer_data = {
                            'customer': str(customer),
                            'total_amount': float(row['sum']),
                            'percentage_of_total': round(float((row['sum'] / total_customer_amount) * 100), 2),
                            'transaction_count': int(row['count']),
                            'average_transaction': float(row['mean']),
                            'amount_volatility': float(row['std']),
                            'min_transaction': float(row['min']),
                            'max_transaction': float(row['max'])
                        }
                        
                        # Add recency and frequency analysis
                        if date_col and pd.api.types.is_datetime64_any_dtype(df_customers[date_col]):
                            customer_dates = df_customers[df_customers[customer_col] == customer][date_col]
                            if not customer_dates.empty:
                                customer_data['last_transaction_date'] = customer_dates.max().strftime('%Y-%m-%d')
                                customer_data['first_transaction_date'] = customer_dates.min().strftime('%Y-%m-%d')
                                customer_data['customer_lifetime_days'] = (customer_dates.max() - customer_dates.min()).days
                                
                                # Calculate transaction frequency
                                if customer_data['customer_lifetime_days'] > 0:
                                    customer_data['transaction_frequency_days'] = round(customer_data['customer_lifetime_days'] / max(1, customer_data['transaction_count'] - 1), 2)
                        
                        insights['customer_metrics'].append(customer_data)
                    
                    # Customer concentration analysis
                    top_5_customers = customer_metrics.head(5)['sum'].sum()
                    insights['customer_concentration'] = {
                        'top_5_customer_percentage': round(float((top_5_customers / total_customer_amount) * 100), 2),
                        'customer_diversity_index': len(customer_metrics),
                        'average_customer_transaction_value': float(customer_metrics['mean'].mean())
                    }
            
        except Exception as e:
            logger.error(f"Error in vendor/customer analysis: {str(e)}")
        
        return insights

    def _analyze_financial_trends(self, df: pd.DataFrame, mappings: Dict[str, Optional[str]]) -> Dict[str, Any]:
        """Analyze financial trends over time with enhanced insights"""
        insights = {}
        
        date_col = mappings['date']
        amount_col = mappings['amount']
        category_col = mappings.get('category')
        
        try:
            df_trends = df.dropna(subset=[date_col, amount_col]).copy()
            if df_trends.empty:
                return {}
            
            # Convert date column if not already datetime
            if not pd.api.types.is_datetime64_any_dtype(df_trends[date_col]):
                df_trends[date_col] = pd.to_datetime(df_trends[date_col], errors='coerce')
            df_trends = df_trends.dropna(subset=[date_col])
            
            if df_trends.empty:
                return {}
            
            # Sort by date for trend analysis
            df_trends = df_trends.sort_values(date_col)
            
            # Daily trends (if enough data points)
            if len(df_trends) > 30:
                daily_trends = df_trends.groupby(df_trends[date_col].dt.date)[amount_col].agg(['sum', 'count']).round(2)
                insights['daily_trends_summary'] = {
                    'average_daily_amount': float(daily_trends['sum'].mean()),
                    'average_daily_transactions': float(daily_trends['count'].mean()),
                    'highest_daily_amount': float(daily_trends['sum'].max()),
                    'lowest_daily_amount': float(daily_trends['sum'].min()),
                    'most_active_day': str(daily_trends['count'].idxmax()),
                    'least_active_day': str(daily_trends['count'].idxmin())
                }
            
            # Monthly trends
            df_trends['month'] = df_trends[date_col].dt.to_period('M')
            monthly_trends = df_trends.groupby('month')[amount_col].agg(['sum', 'count', 'mean']).round(2)
            
            insights['monthly_financial_trends'] = []
            for month, row in monthly_trends.iterrows():
                insights['monthly_financial_trends'].append({
                    'month': str(month),
                    'total_amount': float(row['sum']),
                    'transaction_count': int(row['count']),
                    'average_transaction': float(row['mean'])
                })
            
            # Calculate month-over-month growth
            if len(monthly_trends) > 1:
                monthly_amounts = monthly_trends['sum']
                growth_rates = []
                for i in range(1, len(monthly_amounts)):
                    current = monthly_amounts.iloc[i]
                    previous = monthly_amounts.iloc[i-1]
                    growth_rate = ((current - previous) / previous * 100) if previous != 0 else 0
                    growth_rates.append({
                        'month': str(monthly_amounts.index[i]),
                        'growth_rate_percent': round(float(growth_rate), 2)
                    })
                
                insights['month_over_month_growth'] = growth_rates
            
            # Quarterly trends
            df_trends['quarter'] = df_trends[date_col].dt.to_period('Q')
            quarterly_trends = df_trends.groupby('quarter')[amount_col].agg(['sum', 'count', 'mean']).round(2)
            
            insights['quarterly_trends'] = []
            for quarter, row in quarterly_trends.iterrows():
                insights['quarterly_trends'].append({
                    'quarter': str(quarter),
                    'total_amount': float(row['sum']),
                    'transaction_count': int(row['count']),
                    'average_transaction': float(row['mean'])
                })
            
            # Year-over-year analysis
            df_trends['year'] = df_trends[date_col].dt.year
            yearly_trends = df_trends.groupby('year')[amount_col].agg(['sum', 'count', 'mean']).round(2)
            
            if len(yearly_trends) > 1:
                insights['yearly_trends'] = []
                for year, row in yearly_trends.iterrows():
                    insights['yearly_trends'].append({
                        'year': int(year),
                        'total_amount': float(row['sum']),
                        'transaction_count': int(row['count']),
                        'average_transaction': float(row['mean'])
                    })
                
                # Year-over-year growth calculation
                yearly_amounts = yearly_trends['sum']
                yoy_growth_rates = []
                years = sorted(yearly_amounts.index)
                for i in range(1, len(years)):
                    current_year = years[i]
                    previous_year = years[i-1]
                    current_amount = yearly_amounts[current_year]
                    previous_amount = yearly_amounts[previous_year]
                    growth_rate = ((current_amount - previous_amount) / previous_amount * 100) if previous_amount != 0 else 0
                    yoy_growth_rates.append({
                        'year': current_year,
                        'growth_rate_percent': round(float(growth_rate), 2),
                        'absolute_change': float(current_amount - previous_amount)
                    })
                
                insights['year_over_year_growth'] = yoy_growth_rates
            
            # Seasonal analysis (day of week patterns)
            df_trends['day_of_week'] = df_trends[date_col].dt.day_name()
            dow_trends = df_trends.groupby('day_of_week')[amount_col].agg(['sum', 'count', 'mean']).round(2)
            
            # Order days properly
            day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
            dow_trends = dow_trends.reindex([day for day in day_order if day in dow_trends.index])
            
            insights['day_of_week_patterns'] = []
            for day, row in dow_trends.iterrows():
                insights['day_of_week_patterns'].append({
                    'day_of_week': str(day),
                    'total_amount': float(row['sum']),
                    'transaction_count': int(row['count']),
                    'average_transaction': float(row['mean'])
                })
            
            # Category trends over time (if category available)
            if category_col and category_col in df_trends.columns:
                category_monthly = df_trends.groupby(['month', category_col])[amount_col].sum().unstack(fill_value=0)
                
                insights['category_trends_over_time'] = []
                for category in category_monthly.columns:
                    category_data = []
                    for month in category_monthly.index:
                        if category_monthly.loc[month, category] > 0:
                            category_data.append({
                                'month': str(month),
                                'amount': float(category_monthly.loc[month, category])
                            })
                    
                    if category_data:
                        insights['category_trends_over_time'].append({
                            'category': str(category),
                            'monthly_data': category_data
                        })
            
        except Exception as e:
            logger.error(f"Error in financial trends analysis: {str(e)}")
        
        return insights