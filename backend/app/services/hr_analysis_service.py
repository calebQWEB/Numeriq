import pandas as pd
import numpy as np
from typing import Dict, Any, List, Optional, Tuple
from app.utils.logger import logger
import re
from datetime import datetime

class HRAnalysisService:
    def __init__(self):
        # Define comprehensive column patterns for HR data
        self.column_patterns = {
            'employee_id': [
                ['employee', 'id'], ['emp', 'id'], ['staff', 'id'], 
                ['worker', 'id'], ['id'], ['emp', 'number']
            ],
            'employee_name': [
                ['name'], ['employee', 'name'], ['full', 'name'], 
                ['first', 'name'], ['last', 'name'], ['staff', 'name']
            ],
            'department': [
                ['department'], ['dept'], ['division'], ['team'], 
                ['unit'], ['section'], ['group']
            ],
            'position': [
                ['position'], ['job', 'title'], ['role'], ['title'], 
                ['designation'], ['job', 'role'], ['function']
            ],
            'salary': [
                ['salary'], ['wage'], ['pay'], ['compensation'], 
                ['annual', 'salary'], ['base', 'pay'], ['income']
            ],
            'hire_date': [
                ['hire', 'date'], ['start', 'date'], ['join', 'date'], 
                ['employment', 'date'], ['onboard', 'date']
            ],
            'termination_date': [
                ['termination', 'date'], ['end', 'date'], ['exit', 'date'], 
                ['separation', 'date'], ['last', 'day']
            ],
            'employment_status': [
                ['status'], ['employment', 'status'], ['active'], 
                ['current'], ['employee', 'status']
            ],
            'manager': [
                ['manager'], ['supervisor'], ['boss'], ['lead'], 
                ['manager', 'name'], ['reports', 'to']
            ],
            'performance_rating': [
                ['rating'], ['performance'], ['score'], ['evaluation'], 
                ['review', 'rating'], ['performance', 'score']
            ],
            'training_hours': [
                ['training'], ['education'], ['learning'], ['development'], 
                ['training', 'hours'], ['course', 'hours']
            ],
            'location': [
                ['location'], ['office'], ['site'], ['branch'], 
                ['workplace'], ['city'], ['region']
            ],
            'age': [
                ['age'], ['years', 'old'], ['birth', 'year']
            ],
            'gender': [
                ['gender'], ['sex'], ['male', 'female']
            ],
            'tenure': [
                ['tenure'], ['years', 'service'], ['experience'], 
                ['time', 'company'], ['seniority']
            ],
            'overtime_hours': [
                ['overtime'], ['extra', 'hours'], ['ot'], 
                ['additional', 'hours'], ['overtime', 'hours']
            ],
            'sick_days': [
                ['sick'], ['sick', 'days'], ['sick', 'leave'], 
                ['medical', 'days'], ['illness', 'days']
            ],
            'vacation_days': [
                ['vacation'], ['pto'], ['holiday'], ['leave'], 
                ['vacation', 'days'], ['paid', 'time', 'off']
            ]
        }

    def compute_hr_insights(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Compute comprehensive HR insights from the dataframe"""
        try:
            if df.empty:
                logger.warning("Empty dataframe provided")
                return {}
                
            insights = {}
            logger.info(f"Analyzing HR dataframe with columns: {list(df.columns)}")
            
            # Get column mappings
            column_mappings = self._map_columns(df)
            logger.info(f"Column mappings found: {column_mappings}")
            
            # Workforce composition analysis
            insights.update(self._analyze_workforce_composition(df, column_mappings))
            logger.info("Workforce composition analysis completed")
            
            # Department analysis
            if self._can_analyze_departments(column_mappings):
                insights.update(self._analyze_department_metrics(df, column_mappings))
                logger.info("Department analysis completed")
            
            # Compensation analysis
            if self._can_analyze_compensation(column_mappings):
                insights.update(self._analyze_compensation_metrics(df, column_mappings))
                logger.info("Compensation analysis completed")
            
            # Performance analysis
            if self._can_analyze_performance(column_mappings):
                insights.update(self._analyze_performance_metrics(df, column_mappings))
                logger.info("Performance analysis completed")
            
            # Turnover and retention analysis
            if self._can_analyze_turnover(column_mappings):
                insights.update(self._analyze_turnover_metrics(df, column_mappings))
                logger.info("Turnover analysis completed")
            
            # Training and development analysis
            if self._can_analyze_training(column_mappings):
                insights.update(self._analyze_training_metrics(df, column_mappings))
                logger.info("Training analysis completed")
            
            # Demographics analysis
            insights.update(self._analyze_demographics(df, column_mappings))
            logger.info("Demographics analysis completed")
            
            # Attendance and leave analysis
            if self._can_analyze_attendance(column_mappings):
                insights.update(self._analyze_attendance_metrics(df, column_mappings))
                logger.info("Attendance analysis completed")
            
            # Add basic HR statistics
            insights.update(self._get_basic_hr_stats(df, column_mappings))
            
            logger.info("HR insights computed successfully")
            return insights
            
        except Exception as e:
            logger.error("Failed to compute HR insights", error=str(e))
            return {}

    def _map_columns(self, df: pd.DataFrame) -> Dict[str, Optional[str]]:
        """Map dataframe columns to HR concepts using flexible pattern matching"""
        columns_lower = {col.lower(): col for col in df.columns}
        mappings = {}
        
        for concept, patterns in self.column_patterns.items():
            best_match = None
            best_score = 0
            
            for col_lower, col_original in columns_lower.items():
                for pattern in patterns:
                    score = self._calculate_match_score(col_lower, pattern)
                    if score > best_score and score > 0.6:
                        # Additional validation for numeric columns
                        if concept in ['salary', 'performance_rating', 'training_hours', 'age', 'tenure', 'overtime_hours', 'sick_days', 'vacation_days'] and not pd.api.types.is_numeric_dtype(df[col_original]):
                            continue
                        best_match = col_original
                        best_score = score
            
            mappings[concept] = best_match
        
        return mappings

    def _calculate_match_score(self, column_name: str, pattern: List[str]) -> float:
        """Calculate how well a column name matches a pattern"""
        normalized_col = re.sub(r'[_\-\s]+', ' ', column_name.lower()).strip()
        
        words_found = 0
        total_pattern_length = sum(len(word) for word in pattern)
        matched_length = 0
        
        for word in pattern:
            if word in normalized_col:
                words_found += 1
                matched_length += len(word)
            elif any(word in part for part in normalized_col.split()):
                words_found += 0.5
                matched_length += len(word) * 0.5
        
        if words_found == 0:
            return 0.0
        
        word_coverage = words_found / len(pattern)
        length_ratio = matched_length / max(len(normalized_col), total_pattern_length)
        exact_match_bonus = 1.0 if ' '.join(pattern) == normalized_col else 0.0
        
        return min(1.0, word_coverage * 0.7 + length_ratio * 0.2 + exact_match_bonus * 0.1)

    def _can_analyze_departments(self, mappings: Dict[str, Optional[str]]) -> bool:
        return mappings.get('department') is not None

    def _can_analyze_compensation(self, mappings: Dict[str, Optional[str]]) -> bool:
        return mappings.get('salary') is not None

    def _can_analyze_performance(self, mappings: Dict[str, Optional[str]]) -> bool:
        return mappings.get('performance_rating') is not None

    def _can_analyze_turnover(self, mappings: Dict[str, Optional[str]]) -> bool:
        return mappings.get('hire_date') is not None or mappings.get('termination_date') is not None

    def _can_analyze_training(self, mappings: Dict[str, Optional[str]]) -> bool:
        return mappings.get('training_hours') is not None

    def _can_analyze_attendance(self, mappings: Dict[str, Optional[str]]) -> bool:
        return mappings.get('sick_days') is not None or mappings.get('vacation_days') is not None or mappings.get('overtime_hours') is not None

    def _analyze_workforce_composition(self, df: pd.DataFrame, mappings: Dict[str, Optional[str]]) -> Dict[str, Any]:
        """Analyze overall workforce composition"""
        insights = {}
        
        try:
            insights['workforce_overview'] = {
                'total_employees': len(df),
                'active_employees': len(df) if not mappings.get('employment_status') else len(df[df[mappings['employment_status']].isin(['Active', 'Current', 'Employed', True])]) if mappings.get('employment_status') else len(df)
            }
            
            # Department distribution
            if mappings.get('department'):
                dept_counts = df[mappings['department']].value_counts()
                insights['department_distribution'] = [
                    {'department': str(dept), 'employee_count': int(count), 'percentage': round(float(count/len(df) * 100), 2)}
                    for dept, count in dept_counts.items()
                ]
            
            # Position distribution
            if mappings.get('position'):
                position_counts = df[mappings['position']].value_counts()
                insights['position_distribution'] = [
                    {'position': str(pos), 'employee_count': int(count)}
                    for pos, count in position_counts.head(10).items()
                ]
            
            # Location distribution
            if mappings.get('location'):
                location_counts = df[mappings['location']].value_counts()
                insights['location_distribution'] = [
                    {'location': str(loc), 'employee_count': int(count)}
                    for loc, count in location_counts.items()
                ]
            
        except Exception as e:
            logger.error(f"Error in workforce composition analysis: {str(e)}")
        
        return insights

    def _analyze_department_metrics(self, df: pd.DataFrame, mappings: Dict[str, Optional[str]]) -> Dict[str, Any]:
        """Analyze department-specific metrics"""
        insights = {}
        
        dept_col = mappings['department']
        salary_col = mappings.get('salary')
        performance_col = mappings.get('performance_rating')
        
        try:
            dept_analysis = {}
            
            if salary_col:
                dept_salary = df.dropna(subset=[dept_col, salary_col]).groupby(dept_col)[salary_col].agg(['mean', 'median', 'count', 'std']).round(2)
                dept_salary['std'] = dept_salary['std'].fillna(0)
                
                dept_analysis['salary_by_department'] = []
                for dept, row in dept_salary.iterrows():
                    dept_analysis['salary_by_department'].append({
                        'department': str(dept),
                        'avg_salary': float(row['mean']),
                        'median_salary': float(row['median']),
                        'employee_count': int(row['count']),
                        'salary_std_dev': float(row['std'])
                    })
            
            if performance_col:
                dept_performance = df.dropna(subset=[dept_col, performance_col]).groupby(dept_col)[performance_col].agg(['mean', 'count']).round(2)
                
                dept_analysis['performance_by_department'] = []
                for dept, row in dept_performance.iterrows():
                    dept_analysis['performance_by_department'].append({
                        'department': str(dept),
                        'avg_performance_rating': float(row['mean']),
                        'employees_rated': int(row['count'])
                    })
            
            insights['department_metrics'] = dept_analysis
            
        except Exception as e:
            logger.error(f"Error in department analysis: {str(e)}")
        
        return insights

    def _analyze_compensation_metrics(self, df: pd.DataFrame, mappings: Dict[str, Optional[str]]) -> Dict[str, Any]:
        """Analyze compensation and salary metrics"""
        insights = {}
        
        salary_col = mappings['salary']
        position_col = mappings.get('position')
        tenure_col = mappings.get('tenure')
        
        try:
            df_clean = df.dropna(subset=[salary_col])
            
            if df_clean.empty:
                return {}
            
            insights['compensation_overview'] = {
                'avg_salary': float(df_clean[salary_col].mean()),
                'median_salary': float(df_clean[salary_col].median()),
                'salary_range': {
                    'min': float(df_clean[salary_col].min()),
                    'max': float(df_clean[salary_col].max())
                },
                'salary_std_dev': float(df_clean[salary_col].std()),
                'total_payroll': float(df_clean[salary_col].sum())
            }
            
            # Salary by position
            if position_col:
                position_salary = df_clean.dropna(subset=[position_col]).groupby(position_col)[salary_col].agg(['mean', 'median', 'count']).round(2)
                position_salary = position_salary.sort_values('mean', ascending=False)
                
                insights['salary_by_position'] = []
                for position, row in position_salary.head(15).iterrows():
                    insights['salary_by_position'].append({
                        'position': str(position),
                        'avg_salary': float(row['mean']),
                        'median_salary': float(row['median']),
                        'employee_count': int(row['count'])
                    })
            
            # Salary distribution analysis
            salary_data = df_clean[salary_col]
            insights['salary_distribution'] = {
                'quartiles': {
                    'q1': float(salary_data.quantile(0.25)),
                    'q2': float(salary_data.quantile(0.5)),
                    'q3': float(salary_data.quantile(0.75))
                },
                'percentiles': {
                    'p10': float(salary_data.quantile(0.1)),
                    'p90': float(salary_data.quantile(0.9))
                }
            }
            
        except Exception as e:
            logger.error(f"Error in compensation analysis: {str(e)}")
        
        return insights

    def _analyze_performance_metrics(self, df: pd.DataFrame, mappings: Dict[str, Optional[str]]) -> Dict[str, Any]:
        """Analyze employee performance metrics"""
        insights = {}
        
        performance_col = mappings['performance_rating']
        dept_col = mappings.get('department')
        position_col = mappings.get('position')
        
        try:
            df_clean = df.dropna(subset=[performance_col])
            
            if df_clean.empty:
                return {}
            
            insights['performance_overview'] = {
                'avg_performance_rating': float(df_clean[performance_col].mean()),
                'median_performance_rating': float(df_clean[performance_col].median()),
                'performance_std_dev': float(df_clean[performance_col].std()),
                'high_performers': len(df_clean[df_clean[performance_col] >= df_clean[performance_col].quantile(0.8)]),
                'low_performers': len(df_clean[df_clean[performance_col] <= df_clean[performance_col].quantile(0.2)])
            }
            
            # Performance distribution
            performance_bins = pd.cut(df_clean[performance_col], bins=5, labels=['Poor', 'Below Average', 'Average', 'Good', 'Excellent'])
            performance_dist = performance_bins.value_counts()
            
            insights['performance_distribution'] = [
                {'category': str(cat), 'employee_count': int(count)}
                for cat, count in performance_dist.items()
            ]
            
        except Exception as e:
            logger.error(f"Error in performance analysis: {str(e)}")
        
        return insights

    def _analyze_turnover_metrics(self, df: pd.DataFrame, mappings: Dict[str, Optional[str]]) -> Dict[str, Any]:
        """Analyze employee turnover and retention metrics"""
        insights = {}
        
        hire_date_col = mappings.get('hire_date')
        term_date_col = mappings.get('termination_date')
        dept_col = mappings.get('department')
        
        try:
            if hire_date_col:
                df_dates = df.dropna(subset=[hire_date_col]).copy()
                
                # Convert hire dates
                date_formats = ['%Y-%m-%d', '%m/%d/%Y', '%d/%m/%Y', '%Y-%m-%d %H:%M:%S']
                for fmt in date_formats:
                    try:
                        df_dates[hire_date_col] = pd.to_datetime(df_dates[hire_date_col], format=fmt)
                        break
                    except:
                        continue
                else:
                    df_dates[hire_date_col] = pd.to_datetime(df_dates[hire_date_col], errors='coerce')
                
                df_dates = df_dates.dropna(subset=[hire_date_col])
                
                if not df_dates.empty:
                    current_date = datetime.now()
                    df_dates['tenure_years'] = (current_date - df_dates[hire_date_col]).dt.days / 365.25
                    
                    insights['tenure_metrics'] = {
                        'avg_tenure_years': float(df_dates['tenure_years'].mean()),
                        'median_tenure_years': float(df_dates['tenure_years'].median()),
                        'new_hires_last_year': len(df_dates[df_dates[hire_date_col] >= (current_date - pd.DateOffset(years=1))]),
                        'long_tenure_employees': len(df_dates[df_dates['tenure_years'] >= 5])
                    }
                    
                    # Hiring trends by month
                    df_dates['hire_month'] = df_dates[hire_date_col].dt.to_period('M')
                    hiring_trends = df_dates.groupby('hire_month').size()
                    
                    insights['hiring_trends'] = [
                        {'month': str(month), 'hires': int(count)}
                        for month, count in hiring_trends.tail(12).items()
                    ]
            
            # Termination analysis
            if term_date_col:
                df_terms = df.dropna(subset=[term_date_col]).copy()
                
                if not df_terms.empty:
                    current_date = datetime.now()
                    recent_terms = len(df_terms[pd.to_datetime(df_terms[term_date_col], errors='coerce') >= (current_date - pd.DateOffset(years=1))])
                    
                    insights['turnover_metrics'] = {
                        'total_terminations': len(df_terms),
                        'terminations_last_year': recent_terms,
                        'annual_turnover_rate': round(float((recent_terms / len(df)) * 100), 2) if len(df) > 0 else 0
                    }
            
        except Exception as e:
            logger.error(f"Error in turnover analysis: {str(e)}")
        
        return insights

    def _analyze_training_metrics(self, df: pd.DataFrame, mappings: Dict[str, Optional[str]]) -> Dict[str, Any]:
        """Analyze training and development metrics"""
        insights = {}
        
        training_col = mappings['training_hours']
        dept_col = mappings.get('department')
        position_col = mappings.get('position')
        
        try:
            df_clean = df.dropna(subset=[training_col])
            
            if df_clean.empty:
                return {}
            
            insights['training_overview'] = {
                'avg_training_hours': float(df_clean[training_col].mean()),
                'median_training_hours': float(df_clean[training_col].median()),
                'total_training_hours': float(df_clean[training_col].sum()),
                'employees_with_training': len(df_clean[df_clean[training_col] > 0]),
                'avg_training_per_employee': float(df_clean[training_col].sum() / len(df_clean))
            }
            
            # Training by department
            if dept_col:
                dept_training = df_clean.dropna(subset=[dept_col]).groupby(dept_col)[training_col].agg(['mean', 'sum', 'count']).round(2)
                
                insights['training_by_department'] = []
                for dept, row in dept_training.iterrows():
                    insights['training_by_department'].append({
                        'department': str(dept),
                        'avg_training_hours': float(row['mean']),
                        'total_training_hours': float(row['sum']),
                        'employees_trained': int(row['count'])
                    })
            
        except Exception as e:
            logger.error(f"Error in training analysis: {str(e)}")
        
        return insights

    def _analyze_demographics(self, df: pd.DataFrame, mappings: Dict[str, Optional[str]]) -> Dict[str, Any]:
        """Analyze workforce demographics"""
        insights = {}
        
        age_col = mappings.get('age')
        gender_col = mappings.get('gender')
        
        try:
            demographics = {}
            
            # Age analysis
            if age_col:
                df_age = df.dropna(subset=[age_col])
                if not df_age.empty:
                    demographics['age_metrics'] = {
                        'avg_age': float(df_age[age_col].mean()),
                        'median_age': float(df_age[age_col].median()),
                        'age_range': {
                            'min': float(df_age[age_col].min()),
                            'max': float(df_age[age_col].max())
                        }
                    }
                    
                    # Age groups
                    age_bins = pd.cut(df_age[age_col], bins=[0, 25, 35, 45, 55, 100], labels=['Under 25', '25-34', '35-44', '45-54', '55+'])
                    age_dist = age_bins.value_counts()
                    
                    demographics['age_distribution'] = [
                        {'age_group': str(group), 'employee_count': int(count)}
                        for group, count in age_dist.items()
                    ]
            
            # Gender analysis
            if gender_col:
                gender_dist = df[gender_col].value_counts()
                demographics['gender_distribution'] = [
                    {'gender': str(gender), 'employee_count': int(count), 'percentage': round(float(count/len(df) * 100), 2)}
                    for gender, count in gender_dist.items()
                ]
            
            insights['demographics'] = demographics
            
        except Exception as e:
            logger.error(f"Error in demographics analysis: {str(e)}")
        
        return insights

    def _analyze_attendance_metrics(self, df: pd.DataFrame, mappings: Dict[str, Optional[str]]) -> Dict[str, Any]:
        """Analyze attendance and leave metrics"""
        insights = {}
        
        sick_days_col = mappings.get('sick_days')
        vacation_days_col = mappings.get('vacation_days')
        overtime_col = mappings.get('overtime_hours')
        
        try:
            attendance_metrics = {}
            
            # Sick days analysis
            if sick_days_col:
                df_sick = df.dropna(subset=[sick_days_col])
                if not df_sick.empty:
                    attendance_metrics['sick_leave'] = {
                        'avg_sick_days': float(df_sick[sick_days_col].mean()),
                        'median_sick_days': float(df_sick[sick_days_col].median()),
                        'total_sick_days': float(df_sick[sick_days_col].sum()),
                        'employees_with_sick_leave': len(df_sick[df_sick[sick_days_col] > 0])
                    }
            
            # Vacation analysis
            if vacation_days_col:
                df_vacation = df.dropna(subset=[vacation_days_col])
                if not df_vacation.empty:
                    attendance_metrics['vacation'] = {
                        'avg_vacation_days': float(df_vacation[vacation_days_col].mean()),
                        'median_vacation_days': float(df_vacation[vacation_days_col].median()),
                        'total_vacation_days': float(df_vacation[vacation_days_col].sum())
                    }
            
            # Overtime analysis
            if overtime_col:
                df_overtime = df.dropna(subset=[overtime_col])
                if not df_overtime.empty:
                    attendance_metrics['overtime'] = {
                        'avg_overtime_hours': float(df_overtime[overtime_col].mean()),
                        'total_overtime_hours': float(df_overtime[overtime_col].sum()),
                        'employees_with_overtime': len(df_overtime[df_overtime[overtime_col] > 0])
                    }
            
            insights['attendance_metrics'] = attendance_metrics
            
        except Exception as e:
            logger.error(f"Error in attendance analysis: {str(e)}")
        
        return insights

    def _get_basic_hr_stats(self, df: pd.DataFrame, mappings: Dict[str, Optional[str]]) -> Dict[str, Any]:
        """Get basic HR statistical information"""
        stats = {
            'dataset_info': {
                'total_records': len(df),
                'total_columns': len(df.columns),
                'columns_mapped': len([v for v in mappings.values() if v is not None]),
                'data_completeness': round(float(df.count().sum() / (len(df) * len(df.columns))) * 100, 2)
            }
        }
        
        # Employee diversity metrics
        if mappings.get('department'):
            stats['diversity_metrics'] = {
                'unique_departments': df[mappings['department']].nunique()
            }
        
        if mappings.get('position'):
            stats['diversity_metrics'] = stats.get('diversity_metrics', {})
            stats['diversity_metrics']['unique_positions'] = df[mappings['position']].nunique()
        
        if mappings.get('location'):
            stats['diversity_metrics'] = stats.get('diversity_metrics', {})
            stats['diversity_metrics']['unique_locations'] = df[mappings['location']].nunique()
        
        return stats