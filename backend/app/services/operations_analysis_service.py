import pandas as pd
import numpy as np
from typing import Dict, Any, List, Optional, Tuple
from app.utils.logger import logger
import re
from datetime import datetime

class OperationsAnalysisService:
    def __init__(self):
        # Define comprehensive column patterns for operations data
        self.column_patterns = {
            'order_id': [
                ['order', 'id'], ['order', 'number'], ['id'], ['ref'], 
                ['reference'], ['order', 'ref'], ['transaction', 'id']
            ],
            'product_id': [
                ['product', 'id'], ['item', 'id'], ['sku'], ['product', 'code'], 
                ['item', 'code'], ['part', 'number']
            ],
            'product_name': [
                ['product'], ['item'], ['product', 'name'], ['item', 'name'], 
                ['description'], ['title']
            ],
            'quantity': [
                ['quantity'], ['qty'], ['amount'], ['count'], ['units'], 
                ['volume'], ['pieces']
            ],
            'order_date': [
                ['order', 'date'], ['date'], ['created', 'date'], 
                ['timestamp'], ['order', 'time']
            ],
            'delivery_date': [
                ['delivery', 'date'], ['shipped', 'date'], ['fulfillment', 'date'], 
                ['completed', 'date'], ['sent', 'date']
            ],
            'lead_time': [
                ['lead', 'time'], ['processing', 'time'], ['fulfillment', 'time'], 
                ['cycle', 'time'], ['turnaround']
            ],
            'status': [
                ['status'], ['order', 'status'], ['state'], ['stage'], 
                ['progress'], ['condition']
            ],
            'priority': [
                ['priority'], ['urgency'], ['importance'], ['rush'], 
                ['priority', 'level']
            ],
            'supplier': [
                ['supplier'], ['vendor'], ['provider'], ['manufacturer'], 
                ['source'], ['partner']
            ],
            'warehouse': [
                ['warehouse'], ['location'], ['facility'], ['depot'], 
                ['distribution', 'center'], ['storage']
            ],
            'customer': [
                ['customer'], ['client'], ['buyer'], ['account'], 
                ['customer', 'name'], ['client', 'name']
            ],
            'region': [
                ['region'], ['area'], ['territory'], ['zone'], ['market'], 
                ['district'], ['location'], ['geography']
            ],
            'defect_rate': [
                ['defect'], ['defective'], ['reject'], ['failure'], 
                ['defect', 'rate'], ['quality', 'issue']
            ],
            'on_time_delivery': [
                ['on', 'time'], ['otd'], ['delivery', 'performance'], 
                ['punctual'], ['timely']
            ],
            'cost': [
                ['cost'], ['price'], ['expense'], ['unit', 'cost'], 
                ['total', 'cost'], ['amount']
            ],
            'capacity': [
                ['capacity'], ['throughput'], ['output'], ['production', 'capacity'], 
                ['maximum'], ['limit']
            ],
            'utilization': [
                ['utilization'], ['usage'], ['efficiency'], ['utilization', 'rate'], 
                ['capacity', 'used']
            ],
            'downtime': [
                ['downtime'], ['outage'], ['stoppage'], ['idle', 'time'], 
                ['maintenance', 'time'], ['breakdown']
            ],
            'productivity': [
                ['productivity'], ['output', 'per', 'hour'], ['efficiency'], 
                ['performance'], ['rate']
            ],
            'backlog': [
                ['backlog'], ['pending'], ['queue'], ['waiting'], 
                ['outstanding'], ['open', 'orders']
            ],
            'inventory_level': [
                ['inventory'], ['stock'], ['on', 'hand'], ['available'], 
                ['stock', 'level'], ['inventory', 'count']
            ],
            'reorder_point': [
                ['reorder'], ['minimum', 'stock'], ['safety', 'stock'], 
                ['threshold'], ['trigger', 'point']
            ],
            'cycle_count': [
                ['cycle', 'count'], ['inventory', 'count'], ['stock', 'count'], 
                ['physical', 'count'], ['audit']
            ],
            'shipment_weight': [
                ['weight'], ['mass'], ['kg'], ['pounds'], ['lbs'], 
                ['shipment', 'weight']
            ],
            'processing_time': [
                ['processing'], ['handle', 'time'], ['work', 'time'], 
                ['operation', 'time'], ['duration']
            ],
            'quality_score': [
                ['quality'], ['score'], ['rating'], ['grade'], 
                ['quality', 'rating'], ['performance', 'score']
            ],
            'error_rate': [
                ['error'], ['mistake'], ['accuracy'], ['error', 'rate'], 
                ['failure', 'rate'], ['reject', 'rate']
            ]
        }

    def compute_operations_insights(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Compute comprehensive operations insights from the dataframe"""
        try:
            if df.empty:
                logger.warning("Empty dataframe provided")
                return {}
                
            insights = {}
            logger.info(f"Analyzing operations dataframe with columns: {list(df.columns)}")
            
            # Get column mappings
            column_mappings = self._map_columns(df)
            logger.info(f"Column mappings found: {column_mappings}")
            
            # Order fulfillment analysis
            if self._can_analyze_orders(column_mappings):
                insights.update(self._analyze_order_fulfillment(df, column_mappings))
                logger.info("Order fulfillment analysis completed")
            
            # Inventory management analysis
            if self._can_analyze_inventory(column_mappings):
                insights.update(self._analyze_inventory_management(df, column_mappings))
                logger.info("Inventory analysis completed")
            
            # Supply chain performance
            if self._can_analyze_supply_chain(column_mappings):
                insights.update(self._analyze_supply_chain_performance(df, column_mappings))
                logger.info("Supply chain analysis completed")
            
            # Quality metrics analysis
            if self._can_analyze_quality(column_mappings):
                insights.update(self._analyze_quality_metrics(df, column_mappings))
                logger.info("Quality analysis completed")
            
            # Production efficiency analysis
            if self._can_analyze_production(column_mappings):
                insights.update(self._analyze_production_efficiency(df, column_mappings))
                logger.info("Production efficiency analysis completed")
            
            # Delivery performance analysis
            if self._can_analyze_delivery(column_mappings):
                insights.update(self._analyze_delivery_performance(df, column_mappings))
                logger.info("Delivery performance analysis completed")
            
            # Regional operations analysis
            if self._can_analyze_regions(column_mappings):
                insights.update(self._analyze_regional_operations(df, column_mappings))
                logger.info("Regional operations analysis completed")
            
            # Cost analysis
            if self._can_analyze_costs(column_mappings):
                insights.update(self._analyze_operational_costs(df, column_mappings))
                logger.info("Cost analysis completed")
            
            # Time-based operational trends
            if self._can_analyze_time_trends(column_mappings):
                insights.update(self._analyze_operational_trends(df, column_mappings))
                logger.info("Operational trends analysis completed")
            
            # Add basic operations statistics
            insights.update(self._get_basic_operations_stats(df, column_mappings))
            
            logger.info("Operations insights computed successfully")
            return insights
            
        except Exception as e:
            logger.error("Failed to compute operations insights", error=str(e))
            return {}

    def _map_columns(self, df: pd.DataFrame) -> Dict[str, Optional[str]]:
        """Map dataframe columns to operations concepts using flexible pattern matching"""
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
                        numeric_concepts = ['quantity', 'lead_time', 'defect_rate', 'cost', 'capacity', 
                                          'utilization', 'downtime', 'productivity', 'inventory_level', 
                                          'shipment_weight', 'processing_time', 'quality_score', 'error_rate']
                        if concept in numeric_concepts and not pd.api.types.is_numeric_dtype(df[col_original]):
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

    def _can_analyze_orders(self, mappings: Dict[str, Optional[str]]) -> bool:
        return mappings.get('order_id') is not None and mappings.get('quantity') is not None

    def _can_analyze_inventory(self, mappings: Dict[str, Optional[str]]) -> bool:
        return mappings.get('inventory_level') is not None or mappings.get('product_name') is not None

    def _can_analyze_supply_chain(self, mappings: Dict[str, Optional[str]]) -> bool:
        return mappings.get('supplier') is not None or mappings.get('lead_time') is not None

    def _can_analyze_quality(self, mappings: Dict[str, Optional[str]]) -> bool:
        return mappings.get('defect_rate') is not None or mappings.get('quality_score') is not None or mappings.get('error_rate') is not None

    def _can_analyze_production(self, mappings: Dict[str, Optional[str]]) -> bool:
        return mappings.get('productivity') is not None or mappings.get('utilization') is not None or mappings.get('capacity') is not None

    def _can_analyze_delivery(self, mappings: Dict[str, Optional[str]]) -> bool:
        return mappings.get('delivery_date') is not None or mappings.get('on_time_delivery') is not None

    def _can_analyze_regions(self, mappings: Dict[str, Optional[str]]) -> bool:
        return mappings.get('region') is not None and (mappings.get('quantity') is not None or mappings.get('cost') is not None)

    def _can_analyze_costs(self, mappings: Dict[str, Optional[str]]) -> bool:
        return mappings.get('cost') is not None

    def _can_analyze_time_trends(self, mappings: Dict[str, Optional[str]]) -> bool:
        return mappings.get('order_date') is not None and mappings.get('quantity') is not None

    def _analyze_order_fulfillment(self, df: pd.DataFrame, mappings: Dict[str, Optional[str]]) -> Dict[str, Any]:
        """Analyze order fulfillment metrics"""
        insights = {}
        
        order_id_col = mappings.get('order_id')
        quantity_col = mappings['quantity']
        status_col = mappings.get('status')
        priority_col = mappings.get('priority')
        
        try:
            df_orders = df.dropna(subset=[col for col in [order_id_col, quantity_col] if col is not None])
            
            if df_orders.empty:
                return {}
            
            insights['order_overview'] = {
                'total_orders': df_orders[order_id_col].nunique() if order_id_col else len(df_orders),
                'total_quantity_ordered': float(df_orders[quantity_col].sum()),
                'average_order_quantity': float(df_orders[quantity_col].mean()),
                'median_order_quantity': float(df_orders[quantity_col].median()),
                'largest_order': float(df_orders[quantity_col].max()),
                'smallest_order': float(df_orders[quantity_col].min())
            }
            
            # Order status analysis
            if status_col:
                status_counts = df_orders[status_col].value_counts()
                total_orders = len(df_orders)
                
                insights['order_status_breakdown'] = []
                for status, count in status_counts.items():
                    insights['order_status_breakdown'].append({
                        'status': str(status),
                        'order_count': int(count),
                        'percentage': round(float((count / total_orders) * 100), 2)
                    })
                
                # Calculate fulfillment rate
                completed_statuses = ['completed', 'delivered', 'shipped', 'fulfilled', 'closed']
                completed_orders = len(df_orders[df_orders[status_col].str.lower().isin(completed_statuses)])
                insights['fulfillment_metrics'] = {
                    'fulfillment_rate_percent': round(float((completed_orders / total_orders) * 100), 2),
                    'completed_orders': completed_orders,
                    'pending_orders': total_orders - completed_orders
                }
            
            # Priority analysis
            if priority_col:
                priority_analysis = df_orders.groupby(priority_col)[quantity_col].agg(['sum', 'count', 'mean']).round(2)
                
                insights['priority_analysis'] = []
                for priority, row in priority_analysis.iterrows():
                    insights['priority_analysis'].append({
                        'priority': str(priority),
                        'total_quantity': float(row['sum']),
                        'order_count': int(row['count']),
                        'avg_quantity_per_order': float(row['mean'])
                    })
            
        except Exception as e:
            logger.error(f"Error in order fulfillment analysis: {str(e)}")
        
        return insights

    def _analyze_inventory_management(self, df: pd.DataFrame, mappings: Dict[str, Optional[str]]) -> Dict[str, Any]:
        """Analyze inventory management metrics"""
        insights = {}
        
        inventory_col = mappings.get('inventory_level')
        product_col = mappings.get('product_name')
        reorder_col = mappings.get('reorder_point')
        
        try:
            if inventory_col:
                df_inventory = df.dropna(subset=[inventory_col])
                
                if not df_inventory.empty:
                    insights['inventory_overview'] = {
                        'total_inventory_units': float(df_inventory[inventory_col].sum()),
                        'average_inventory_per_item': float(df_inventory[inventory_col].mean()),
                        'median_inventory': float(df_inventory[inventory_col].median()),
                        'inventory_items': len(df_inventory),
                        'zero_inventory_items': len(df_inventory[df_inventory[inventory_col] == 0]),
                        'low_inventory_items': len(df_inventory[df_inventory[inventory_col] <= df_inventory[inventory_col].quantile(0.1)])
                    }
                    
                    # Inventory distribution analysis
                    inventory_bins = pd.qcut(df_inventory[inventory_col], q=5, labels=['Very Low', 'Low', 'Medium', 'High', 'Very High'], duplicates='drop')
                    inventory_dist = inventory_bins.value_counts()
                    
                    insights['inventory_distribution'] = []
                    for level, count in inventory_dist.items():
                        insights['inventory_distribution'].append({
                            'level': str(level),
                            'item_count': int(count)
                        })
                    
                    # Reorder analysis
                    if reorder_col and reorder_col in df_inventory.columns:
                        df_reorder = df_inventory.dropna(subset=[reorder_col])
                        items_below_reorder = df_reorder[df_reorder[inventory_col] <= df_reorder[reorder_col]]
                        
                        insights['reorder_analysis'] = {
                            'items_below_reorder_point': len(items_below_reorder),
                            'percentage_below_reorder': round(float((len(items_below_reorder) / len(df_reorder)) * 100), 2),
                            'avg_reorder_point': float(df_reorder[reorder_col].mean())
                        }
            
            # Product inventory analysis
            if product_col and inventory_col:
                product_inventory = df.dropna(subset=[product_col, inventory_col]).groupby(product_col)[inventory_col].agg(['sum', 'mean']).round(2)
                product_inventory = product_inventory.sort_values('sum', ascending=True)
                
                insights['product_inventory_alerts'] = {
                    'lowest_stock_products': []
                }
                
                for product, row in product_inventory.head(10).iterrows():
                    insights['product_inventory_alerts']['lowest_stock_products'].append({
                        'product': str(product),
                        'total_inventory': float(row['sum']),
                        'avg_inventory': float(row['mean'])
                    })
            
        except Exception as e:
            logger.error(f"Error in inventory management analysis: {str(e)}")
        
        return insights

    def _analyze_supply_chain_performance(self, df: pd.DataFrame, mappings: Dict[str, Optional[str]]) -> Dict[str, Any]:
        """Analyze supply chain performance metrics"""
        insights = {}
        
        supplier_col = mappings.get('supplier')
        lead_time_col = mappings.get('lead_time')
        quantity_col = mappings.get('quantity')
        cost_col = mappings.get('cost')
        
        try:
            # Supplier performance analysis
            if supplier_col:
                df_suppliers = df.dropna(subset=[supplier_col])
                
                if not df_suppliers.empty:
                    supplier_metrics = {}
                    
                    if quantity_col:
                        supplier_qty = df_suppliers.dropna(subset=[quantity_col]).groupby(supplier_col)[quantity_col].agg(['sum', 'count', 'mean']).round(2)
                        supplier_metrics['quantity'] = supplier_qty
                    
                    if lead_time_col:
                        supplier_lead = df_suppliers.dropna(subset=[lead_time_col]).groupby(supplier_col)[lead_time_col].agg(['mean', 'std']).round(2)
                        supplier_lead['std'] = supplier_lead['std'].fillna(0)
                        supplier_metrics['lead_time'] = supplier_lead
                    
                    if cost_col:
                        supplier_cost = df_suppliers.dropna(subset=[cost_col]).groupby(supplier_col)[cost_col].agg(['sum', 'mean']).round(2)
                        supplier_metrics['cost'] = supplier_cost
                    
                    # Combine supplier metrics
                    insights['supplier_performance'] = []
                    suppliers = set()
                    for metric_type in supplier_metrics.values():
                        suppliers.update(metric_type.index)
                    
                    for supplier in suppliers:
                        supplier_data = {'supplier': str(supplier)}
                        
                        if 'quantity' in supplier_metrics and supplier in supplier_metrics['quantity'].index:
                            row = supplier_metrics['quantity'].loc[supplier]
                            supplier_data.update({
                                'total_quantity': float(row['sum']),
                                'order_count': int(row['count']),
                                'avg_quantity_per_order': float(row['mean'])
                            })
                        
                        if 'lead_time' in supplier_metrics and supplier in supplier_metrics['lead_time'].index:
                            row = supplier_metrics['lead_time'].loc[supplier]
                            supplier_data.update({
                                'avg_lead_time': float(row['mean']),
                                'lead_time_consistency': float(row['std'])
                            })
                        
                        if 'cost' in supplier_metrics and supplier in supplier_metrics['cost'].index:
                            row = supplier_metrics['cost'].loc[supplier]
                            supplier_data.update({
                                'total_cost': float(row['sum']),
                                'avg_cost': float(row['mean'])
                            })
                        
                        insights['supplier_performance'].append(supplier_data)
            
            # Lead time analysis
            if lead_time_col:
                df_lead_time = df.dropna(subset=[lead_time_col])
                
                if not df_lead_time.empty:
                    insights['lead_time_metrics'] = {
                        'avg_lead_time': float(df_lead_time[lead_time_col].mean()),
                        'median_lead_time': float(df_lead_time[lead_time_col].median()),
                        'lead_time_std_dev': float(df_lead_time[lead_time_col].std()),
                        'min_lead_time': float(df_lead_time[lead_time_col].min()),
                        'max_lead_time': float(df_lead_time[lead_time_col].max()),
                        'lead_time_consistency_score': round(100 - (float(df_lead_time[lead_time_col].std()) / float(df_lead_time[lead_time_col].mean()) * 100), 2)
                    }
            
        except Exception as e:
            logger.error(f"Error in supply chain analysis: {str(e)}")
        
        return insights

    def _analyze_quality_metrics(self, df: pd.DataFrame, mappings: Dict[str, Optional[str]]) -> Dict[str, Any]:
        """Analyze quality control metrics"""
        insights = {}
        
        defect_col = mappings.get('defect_rate')
        quality_col = mappings.get('quality_score')
        error_col = mappings.get('error_rate')
        product_col = mappings.get('product_name')
        
        try:
            quality_metrics = {}
            
            # Defect rate analysis
            if defect_col:
                df_defects = df.dropna(subset=[defect_col])
                if not df_defects.empty:
                    quality_metrics['defect_analysis'] = {
                        'avg_defect_rate': float(df_defects[defect_col].mean()),
                        'median_defect_rate': float(df_defects[defect_col].median()),
                        'total_defects': float(df_defects[defect_col].sum()),
                        'highest_defect_rate': float(df_defects[defect_col].max()),
                        'zero_defect_items': len(df_defects[df_defects[defect_col] == 0])
                    }
            
            # Quality score analysis
            if quality_col:
                df_quality = df.dropna(subset=[quality_col])
                if not df_quality.empty:
                    quality_metrics['quality_score_analysis'] = {
                        'avg_quality_score': float(df_quality[quality_col].mean()),
                        'median_quality_score': float(df_quality[quality_col].median()),
                        'quality_std_dev': float(df_quality[quality_col].std()),
                        'high_quality_items': len(df_quality[df_quality[quality_col] >= df_quality[quality_col].quantile(0.8)]),
                        'low_quality_items': len(df_quality[df_quality[quality_col] <= df_quality[quality_col].quantile(0.2)])
                    }
            
            # Error rate analysis
            if error_col:
                df_errors = df.dropna(subset=[error_col])
                if not df_errors.empty:
                    quality_metrics['error_analysis'] = {
                        'avg_error_rate': float(df_errors[error_col].mean()),
                        'total_errors': float(df_errors[error_col].sum()),
                        'error_free_items': len(df_errors[df_errors[error_col] == 0])
                    }
            
            # Quality by product
            if product_col and (defect_col or quality_col):
                quality_by_product = []
                
                if defect_col:
                    product_defects = df.dropna(subset=[product_col, defect_col]).groupby(product_col)[defect_col].mean().round(4)
                    product_defects = product_defects.sort_values(ascending=False)
                    
                    quality_by_product = [
                        {'product': str(product), 'avg_defect_rate': float(rate)}
                        for product, rate in product_defects.head(10).items()
                    ]
                
                if quality_by_product:
                    quality_metrics['product_quality_issues'] = quality_by_product
            
            insights['quality_metrics'] = quality_metrics
            
        except Exception as e:
            logger.error(f"Error in quality analysis: {str(e)}")
        
        return insights

    def _analyze_production_efficiency(self, df: pd.DataFrame, mappings: Dict[str, Optional[str]]) -> Dict[str, Any]:
        """Analyze production efficiency metrics"""
        insights = {}
        
        productivity_col = mappings.get('productivity')
        utilization_col = mappings.get('utilization')
        capacity_col = mappings.get('capacity')
        downtime_col = mappings.get('downtime')
        
        try:
            production_metrics = {}
            
            # Productivity analysis
            if productivity_col:
                df_prod = df.dropna(subset=[productivity_col])
                if not df_prod.empty:
                    production_metrics['productivity'] = {
                        'avg_productivity': float(df_prod[productivity_col].mean()),
                        'median_productivity': float(df_prod[productivity_col].median()),
                        'productivity_std_dev': float(df_prod[productivity_col].std()),
                        'max_productivity': float(df_prod[productivity_col].max()),
                        'min_productivity': float(df_prod[productivity_col].min())
                    }
            
            # Utilization analysis
            if utilization_col:
                df_util = df.dropna(subset=[utilization_col])
                if not df_util.empty:
                    production_metrics['utilization'] = {
                        'avg_utilization_percent': float(df_util[utilization_col].mean()),
                        'median_utilization_percent': float(df_util[utilization_col].median()),
                        'high_utilization_periods': len(df_util[df_util[utilization_col] >= 90]),
                        'low_utilization_periods': len(df_util[df_util[utilization_col] <= 50]),
                        'optimal_utilization_periods': len(df_util[(df_util[utilization_col] >= 75) & (df_util[utilization_col] < 90)])
                    }
            
            # Capacity analysis
            if capacity_col:
                df_capacity = df.dropna(subset=[capacity_col])
                if not df_capacity.empty:
                    production_metrics['capacity'] = {
                        'total_capacity': float(df_capacity[capacity_col].sum()),
                        'avg_capacity': float(df_capacity[capacity_col].mean()),
                        'capacity_variance': float(df_capacity[capacity_col].std())
                    }
            
            # Downtime analysis
            if downtime_col:
                df_downtime = df.dropna(subset=[downtime_col])
                if not df_downtime.empty:
                    production_metrics['downtime'] = {
                        'total_downtime': float(df_downtime[downtime_col].sum()),
                        'avg_downtime': float(df_downtime[downtime_col].mean()),
                        'median_downtime': float(df_downtime[downtime_col].median()),
                        'zero_downtime_periods': len(df_downtime[df_downtime[downtime_col] == 0])
                    }
            
            insights['production_efficiency'] = production_metrics
            
        except Exception as e:
            logger.error(f"Error in production efficiency analysis: {str(e)}")
        
        return insights

    def _analyze_delivery_performance(self, df: pd.DataFrame, mappings: Dict[str, Optional[str]]) -> Dict[str, Any]:
        """Analyze delivery performance metrics"""
        insights = {}
        
        order_date_col = mappings.get('order_date')
        delivery_date_col = mappings.get('delivery_date')
        on_time_col = mappings.get('on_time_delivery')
        
        try:
            delivery_metrics = {}
            
            # On-time delivery analysis
            if on_time_col:
                df_otd = df.dropna(subset=[on_time_col])
                if not df_otd.empty:
                    # Assume on-time delivery is boolean or percentage
                    if df_otd[on_time_col].dtype == 'bool' or df_otd[on_time_col].isin([0, 1]).all():
                        on_time_rate = float(df_otd[on_time_col].mean() * 100)
                    else:
                        on_time_rate = float(df_otd[on_time_col].mean())
                    
                    delivery_metrics['on_time_delivery'] = {
                        'on_time_delivery_rate_percent': on_time_rate,
                        'total_deliveries': len(df_otd),
                        'on_time_deliveries': len(df_otd[df_otd[on_time_col] == 1]) if df_otd[on_time_col].isin([0, 1]).all() else int(len(df_otd) * on_time_rate / 100)
                    }
            
            # Delivery time analysis
            if order_date_col and delivery_date_col:
                df_delivery = df.dropna(subset=[order_date_col, delivery_date_col]).copy()
                
                if not df_delivery.empty:
                    # Convert dates
                    for date_col in [order_date_col, delivery_date_col]:
                        df_delivery[date_col] = pd.to_datetime(df_delivery[date_col], errors='coerce')
                    
                    df_delivery = df_delivery.dropna(subset=[order_date_col, delivery_date_col])
                    
                    if not df_delivery.empty:
                        df_delivery['delivery_time_days'] = (df_delivery[delivery_date_col] - df_delivery[order_date_col]).dt.days
                        
                        delivery_metrics['delivery_time_analysis'] = {
                            'avg_delivery_time_days': float(df_delivery['delivery_time_days'].mean()),
                            'median_delivery_time_days': float(df_delivery['delivery_time_days'].median()),
                            'fastest_delivery_days': float(df_delivery['delivery_time_days'].min()),
                            'slowest_delivery_days': float(df_delivery['delivery_time_days'].max()),
                            'delivery_time_std_dev': float(df_delivery['delivery_time_days'].std())
                        }
                        
                        # Delivery time distribution
                        delivery_bins = pd.cut(df_delivery['delivery_time_days'], bins=5, labels=['Very Fast', 'Fast', 'Average', 'Slow', 'Very Slow'])
                        delivery_dist = delivery_bins.value_counts()
                        
                        delivery_metrics['delivery_time_distribution'] = []
                        for category, count in delivery_dist.items():
                            delivery_metrics['delivery_time_distribution'].append({
                                'category': str(category),
                                'delivery_count': int(count)
                            })
            
            insights['delivery_performance'] = delivery_metrics
            
        except Exception as e:
            logger.error(f"Error in delivery performance analysis: {str(e)}")
        
        return insights

    def _analyze_regional_operations(self, df: pd.DataFrame, mappings: Dict[str, Optional[str]]) -> Dict[str, Any]:
        """Analyze regional operations performance"""
        insights = {}
        
        region_col = mappings['region']
        quantity_col = mappings.get('quantity')
        cost_col = mappings.get('cost')
        
        try:
            df_regional = df.dropna(subset=[region_col])
            
            if df_regional.empty:
                return {}
            
            regional_metrics = {}
            
            # Regional volume analysis
            if quantity_col:
                df_qty = df_regional.dropna(subset=[quantity_col])
                if not df_qty.empty:
                    regional_qty = df_qty.groupby(region_col)[quantity_col].agg(['sum', 'count', 'mean']).round(2)
                    regional_qty = regional_qty.sort_values('sum', ascending=False)
                    
                    total_quantity = float(df_qty[quantity_col].sum())
                    
                    regional_metrics['volume_by_region'] = []
                    for region, row in regional_qty.iterrows():
                        regional_metrics['volume_by_region'].append({
                            'region': str(region),
                            'total_quantity': float(row['sum']),
                            'percentage_of_total': round(float((row['sum'] / total_quantity) * 100), 2),
                            'order_count': int(row['count']),
                            'avg_quantity_per_order': float(row['mean'])
                        })
            
            # Regional cost analysis
            if cost_col:
                df_cost = df_regional.dropna(subset=[cost_col])
                if not df_cost.empty:
                    regional_cost = df_cost.groupby(region_col)[cost_col].agg(['sum', 'mean', 'std']).round(2)
                    regional_cost['std'] = regional_cost['std'].fillna(0)
                    regional_cost = regional_cost.sort_values('sum', ascending=False)
                    
                    regional_metrics['cost_by_region'] = []
                    for region, row in regional_cost.iterrows():
                        regional_metrics['cost_by_region'].append({
                            'region': str(region),
                            'total_cost': float(row['sum']),
                            'avg_cost': float(row['mean']),
                            'cost_variability': float(row['std'])
                        })
            
            insights['regional_operations'] = regional_metrics
            
        except Exception as e:
            logger.error(f"Error in regional operations analysis: {str(e)}")
        
        return insights

    def _analyze_operational_costs(self, df: pd.DataFrame, mappings: Dict[str, Optional[str]]) -> Dict[str, Any]:
        """Analyze operational cost metrics"""
        insights = {}
        
        cost_col = mappings['cost']
        product_col = mappings.get('product_name')
        supplier_col = mappings.get('supplier')
        warehouse_col = mappings.get('warehouse')
        
        try:
            df_cost = df.dropna(subset=[cost_col])
            
            if df_cost.empty:
                return {}
            
            insights['cost_overview'] = {
                'total_operational_costs': float(df_cost[cost_col].sum()),
                'average_cost': float(df_cost[cost_col].mean()),
                'median_cost': float(df_cost[cost_col].median()),
                'highest_cost': float(df_cost[cost_col].max()),
                'lowest_cost': float(df_cost[cost_col].min()),
                'cost_std_dev': float(df_cost[cost_col].std())
            }
            
            # Cost by product
            if product_col:
                product_costs = df_cost.dropna(subset=[product_col]).groupby(product_col)[cost_col].agg(['sum', 'count', 'mean']).round(2)
                product_costs = product_costs.sort_values('sum', ascending=False)
                
                insights['cost_by_product'] = []
                for product, row in product_costs.head(15).iterrows():
                    insights['cost_by_product'].append({
                        'product': str(product),
                        'total_cost': float(row['sum']),
                        'transaction_count': int(row['count']),
                        'avg_cost_per_transaction': float(row['mean'])
                    })
            
            # Cost by supplier
            if supplier_col:
                supplier_costs = df_cost.dropna(subset=[supplier_col]).groupby(supplier_col)[cost_col].agg(['sum', 'count', 'mean']).round(2)
                supplier_costs = supplier_costs.sort_values('sum', ascending=False)
                
                insights['cost_by_supplier'] = []
                for supplier, row in supplier_costs.head(10).iterrows():
                    insights['cost_by_supplier'].append({
                        'supplier': str(supplier),
                        'total_cost': float(row['sum']),
                        'transaction_count': int(row['count']),
                        'avg_cost_per_transaction': float(row['mean'])
                    })
            
            # Cost by warehouse/location
            if warehouse_col:
                warehouse_costs = df_cost.dropna(subset=[warehouse_col]).groupby(warehouse_col)[cost_col].agg(['sum', 'count', 'mean']).round(2)
                warehouse_costs = warehouse_costs.sort_values('sum', ascending=False)
                
                insights['cost_by_warehouse'] = []
                for warehouse, row in warehouse_costs.iterrows():
                    insights['cost_by_warehouse'].append({
                        'warehouse': str(warehouse),
                        'total_cost': float(row['sum']),
                        'transaction_count': int(row['count']),
                        'avg_cost_per_transaction': float(row['mean'])
                    })
            
        except Exception as e:
            logger.error(f"Error in operational cost analysis: {str(e)}")
        
        return insights

    def _analyze_operational_trends(self, df: pd.DataFrame, mappings: Dict[str, Optional[str]]) -> Dict[str, Any]:
        """Analyze operational trends over time"""
        insights = {}
        
        order_date_col = mappings['order_date']
        quantity_col = mappings['quantity']
        cost_col = mappings.get('cost')
        status_col = mappings.get('status')
        
        try:
            df_trends = df.dropna(subset=[order_date_col, quantity_col]).copy()
            if df_trends.empty:
                return {}
            
            # Convert date column
            df_trends[order_date_col] = pd.to_datetime(df_trends[order_date_col], errors='coerce')
            df_trends = df_trends.dropna(subset=[order_date_col])
            
            if df_trends.empty:
                return {}
            
            # Monthly operational trends
            df_trends['month'] = df_trends[order_date_col].dt.to_period('M')
            monthly_trends = df_trends.groupby('month').agg({
                quantity_col: ['sum', 'count', 'mean'],
                cost_col: ['sum', 'mean'] if cost_col else []
            }).round(2)
            
            monthly_trends.columns = ['_'.join(col).strip() for col in monthly_trends.columns]
            
            insights['monthly_operational_trends'] = []
            for month, row in monthly_trends.iterrows():
                trend_data = {
                    'month': str(month),
                    'total_quantity': float(row[f'{quantity_col}_sum']),
                    'order_count': int(row[f'{quantity_col}_count']),
                    'avg_quantity_per_order': float(row[f'{quantity_col}_mean'])
                }
                
                if cost_col:
                    trend_data.update({
                        'total_cost': float(row[f'{cost_col}_sum']),
                        'avg_cost': float(row[f'{cost_col}_mean'])
                    })
                
                insights['monthly_operational_trends'].append(trend_data)
            
            # Weekly patterns
            df_trends['day_of_week'] = df_trends[order_date_col].dt.day_name()
            daily_patterns = df_trends.groupby('day_of_week')[quantity_col].agg(['sum', 'count']).round(2)
            
            insights['weekly_patterns'] = []
            for day, row in daily_patterns.iterrows():
                insights['weekly_patterns'].append({
                    'day': day,
                    'total_quantity': float(row['sum']),
                    'order_count': int(row['count'])
                })
            
            # Seasonal analysis
            df_trends['season'] = df_trends[order_date_col].dt.month.map({
                12: 'Winter', 1: 'Winter', 2: 'Winter',
                3: 'Spring', 4: 'Spring', 5: 'Spring',
                6: 'Summer', 7: 'Summer', 8: 'Summer',
                9: 'Fall', 10: 'Fall', 11: 'Fall'
            })
            
            seasonal_trends = df_trends.groupby('season')[quantity_col].agg(['sum', 'count']).round(2)
            
            insights['seasonal_trends'] = []
            for season, row in seasonal_trends.iterrows():
                insights['seasonal_trends'].append({
                    'season': season,
                    'total_quantity': float(row['sum']),
                    'order_count': int(row['count'])
                })
            
            # Growth rate calculation
            if len(monthly_trends) > 1:
                quantity_values = [row[f'{quantity_col}_sum'] for _, row in monthly_trends.iterrows()]
                if len(quantity_values) >= 2:
                    recent_growth = ((quantity_values[-1] - quantity_values[-2]) / quantity_values[-2]) * 100
                    insights['growth_metrics'] = {
                        'monthly_quantity_growth_percent': round(float(recent_growth), 2),
                        'trend_direction': 'increasing' if recent_growth > 0 else 'decreasing'
                    }
            
        except Exception as e:
            logger.error(f"Error in operational trends analysis: {str(e)}")
        
        return insights

    def _get_basic_operations_stats(self, df: pd.DataFrame, mappings: Dict[str, Optional[str]]) -> Dict[str, Any]:
        """Get basic operations statistical information"""
        stats = {
            'dataset_info': {
                'total_records': len(df),
                'total_columns': len(df.columns),
                'columns_mapped': len([v for v in mappings.values() if v is not None]),
                'data_completeness': round(float(df.count().sum() / (len(df) * len(df.columns))) * 100, 2)
            }
        }
        
        # Operations diversity metrics
        diversity_metrics = {}
        
        if mappings.get('product_name'):
            diversity_metrics['unique_products'] = df[mappings['product_name']].nunique()
        
        if mappings.get('supplier'):
            diversity_metrics['unique_suppliers'] = df[mappings['supplier']].nunique()
        
        if mappings.get('warehouse'):
            diversity_metrics['unique_warehouses'] = df[mappings['warehouse']].nunique()
        
        if mappings.get('customer'):
            diversity_metrics['unique_customers'] = df[mappings['customer']].nunique()
        
        if mappings.get('region'):
            diversity_metrics['unique_regions'] = df[mappings['region']].nunique()
        
        if diversity_metrics:
            stats['diversity_metrics'] = diversity_metrics
        
        # Operational volume metrics
        if mappings.get('quantity'):
            quantity_data = df[mappings['quantity']].dropna()
            if not quantity_data.empty:
                stats['volume_statistics'] = {
                    'total_volume': float(quantity_data.sum()),
                    'avg_volume_per_record': float(quantity_data.mean()),
                    'median_volume': float(quantity_data.median()),
                    'volume_std_dev': float(quantity_data.std()),
                    'max_single_volume': float(quantity_data.max()),
                    'min_single_volume': float(quantity_data.min())
                }
        
        # Order metrics
        if mappings.get('order_id'):
            stats['order_statistics'] = {
                'unique_orders': df[mappings['order_id']].nunique(),
                'avg_items_per_order': round(len(df) / df[mappings['order_id']].nunique(), 2)
            }
        
        return stats