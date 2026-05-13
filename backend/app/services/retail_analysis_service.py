import pandas as pd
import numpy as np
from typing import Dict, Any, List, Optional, Tuple
from app.utils.logger import logger
import re

class RetailAnalysisService:
    def __init__(self):
        # Define comprehensive column patterns for retail data
        self.column_patterns = {
            'product_id': [
                ['product', 'id'], ['sku'], ['item', 'code'], ['product', 'code'],
                ['barcode'], ['upc'], ['item', 'id'], ['sku', 'code']
            ],
            'product_name': [
                ['product'], ['item'], ['product', 'name'], ['item', 'name'],
                ['merchandise'], ['goods'], ['article']
            ],
            'category': [
                ['category'], ['product', 'category'], ['item', 'category'],
                ['type'], ['class'], ['group'], ['department'], ['section']
            ],
            'brand': [
                ['brand'], ['manufacturer'], ['supplier'], ['vendor'],
                ['make'], ['label']
            ],
            'price': [
                ['price'], ['unit', 'price'], ['cost', 'price'], ['retail', 'price'],
                ['selling', 'price'], ['list', 'price'], ['msrp']
            ],
            'cost': [
                ['cost'], ['unit', 'cost'], ['wholesale', 'cost'], ['purchase', 'cost'],
                ['buy', 'price'], ['supplier', 'cost'], ['cogs']
            ],
            'quantity_sold': [
                ['quantity'], ['qty'], ['units', 'sold'], ['sold'],
                ['sales', 'qty'], ['volume'], ['count']
            ],
            'inventory_level': [
                ['inventory'], ['stock'], ['on', 'hand'], ['available'],
                ['in', 'stock'], ['current', 'stock'], ['stock', 'level']
            ],
            'date': [
                ['date'], ['sale', 'date'], ['transaction', 'date'],
                ['order', 'date'], ['timestamp'], ['time']
            ],
            'store': [
                ['store'], ['location'], ['branch'], ['outlet'],
                ['shop'], ['store', 'id'], ['location', 'id']
            ],
            'discount': [
                ['discount'], ['markdown'], ['promotion'], ['sale', 'discount'],
                ['price', 'reduction'], ['rebate'], ['coupon']
            ],
            'margin': [
                ['margin'], ['profit', 'margin'], ['gross', 'margin'],
                ['markup'], ['profit'], ['gross', 'profit']
            ]
        }

    def compute_retail_insights(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Compute comprehensive retail business insights from the dataframe"""
        try:
            if df.empty:
                logger.warning("Empty dataframe provided")
                return {}
                
            insights = {}
            logger.info(f"Analyzing retail dataframe with columns: {list(df.columns)}")
            
            # Get column mappings
            column_mappings = self._map_columns(df)
            logger.info(f"Column mappings found: {column_mappings}")
            
            # Product performance analysis
            if self._can_analyze_products(column_mappings):
                insights.update(self._analyze_product_performance(df, column_mappings))
                logger.info("Product performance analysis completed")
            
            # Category analysis
            if self._can_analyze_categories(column_mappings):
                insights.update(self._analyze_category_performance(df, column_mappings))
                logger.info("Category analysis completed")
            
            # Brand analysis
            if self._can_analyze_brands(column_mappings):
                insights.update(self._analyze_brand_performance(df, column_mappings))
                logger.info("Brand analysis completed")
            
            # Inventory analysis
            if self._can_analyze_inventory(column_mappings):
                insights.update(self._analyze_inventory_metrics(df, column_mappings))
                logger.info("Inventory analysis completed")
            
            # Pricing and margin analysis
            if self._can_analyze_pricing(column_mappings):
                insights.update(self._analyze_pricing_strategy(df, column_mappings))
                logger.info("Pricing analysis completed")
            
            # Store performance analysis
            if self._can_analyze_stores(column_mappings):
                insights.update(self._analyze_store_performance(df, column_mappings))
                logger.info("Store performance analysis completed")
            
            # Seasonal and time-based analysis
            if self._can_analyze_time(column_mappings):
                insights.update(self._analyze_seasonal_trends(df, column_mappings))
                logger.info("Seasonal analysis completed")
            
            # Add basic retail statistics
            insights.update(self._get_basic_retail_stats(df, column_mappings))
            
            logger.info("Retail insights computed successfully")
            return insights
            
        except Exception as e:
            logger.error("Failed to compute retail insights", error=str(e))
            return {}

    def _map_columns(self, df: pd.DataFrame) -> Dict[str, Optional[str]]:
        """Map dataframe columns to retail concepts using flexible pattern matching"""
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
                        if concept in ['price', 'cost', 'quantity_sold', 'inventory_level', 'discount', 'margin'] and not pd.api.types.is_numeric_dtype(df[col_original]):
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

    def _can_analyze_products(self, mappings: Dict[str, Optional[str]]) -> bool:
        return mappings.get('product_name') is not None and mappings.get('quantity_sold') is not None

    def _can_analyze_categories(self, mappings: Dict[str, Optional[str]]) -> bool:
        return mappings.get('category') is not None and mappings.get('quantity_sold') is not None

    def _can_analyze_brands(self, mappings: Dict[str, Optional[str]]) -> bool:
        return mappings.get('brand') is not None and mappings.get('quantity_sold') is not None

    def _can_analyze_inventory(self, mappings: Dict[str, Optional[str]]) -> bool:
        return mappings.get('inventory_level') is not None or (mappings.get('quantity_sold') is not None and mappings.get('product_name') is not None)

    def _can_analyze_pricing(self, mappings: Dict[str, Optional[str]]) -> bool:
        return mappings.get('price') is not None or mappings.get('cost') is not None

    def _can_analyze_stores(self, mappings: Dict[str, Optional[str]]) -> bool:
        return mappings.get('store') is not None and mappings.get('quantity_sold') is not None

    def _can_analyze_time(self, mappings: Dict[str, Optional[str]]) -> bool:
        return mappings.get('date') is not None and mappings.get('quantity_sold') is not None

    def _analyze_product_performance(self, df: pd.DataFrame, mappings: Dict[str, Optional[str]]) -> Dict[str, Any]:
        """Analyze individual product performance"""
        insights = {}
        
        product_col = mappings['product_name']
        qty_col = mappings['quantity_sold']
        price_col = mappings.get('price')
        
        try:
            df_clean = df.dropna(subset=[col for col in [product_col, qty_col] if col is not None])
            
            if df_clean.empty:
                return {}
            
            # Calculate revenue if price available
            if price_col:
                df_clean = df_clean.dropna(subset=[price_col])
                df_clean['revenue'] = df_clean[qty_col] * df_clean[price_col]
                
                product_metrics = df_clean.groupby(product_col).agg({
                    qty_col: ['sum', 'count'],
                    'revenue': ['sum', 'mean'],
                    price_col: 'mean'
                }).round(2)
                
                product_metrics.columns = ['_'.join(col).strip() for col in product_metrics.columns]
                product_metrics = product_metrics.sort_values('revenue_sum', ascending=False)
                
                insights['top_performing_products'] = []
                for product, row in product_metrics.head(10).iterrows():
                    insights['top_performing_products'].append({
                        'product': str(product),
                        'total_revenue': float(row['revenue_sum']),
                        'units_sold': int(row[f'{qty_col}_sum']),
                        'transactions': int(row[f'{qty_col}_count']),
                        'avg_revenue_per_transaction': float(row['revenue_mean']),
                        'avg_price': float(row[f'{price_col}_mean'])
                    })
            else:
                product_metrics = df_clean.groupby(product_col)[qty_col].agg(['sum', 'count', 'mean']).round(2)
                product_metrics = product_metrics.sort_values('sum', ascending=False)
                
                insights['top_selling_products'] = []
                for product, row in product_metrics.head(10).iterrows():
                    insights['top_selling_products'].append({
                        'product': str(product),
                        'units_sold': int(row['sum']),
                        'transactions': int(row['count']),
                        'avg_units_per_transaction': float(row['mean'])
                    })
            
        except Exception as e:
            logger.error(f"Error in product performance analysis: {str(e)}")
        
        return insights

    def _analyze_category_performance(self, df: pd.DataFrame, mappings: Dict[str, Optional[str]]) -> Dict[str, Any]:
        """Analyze category performance"""
        insights = {}
        
        category_col = mappings['category']
        qty_col = mappings['quantity_sold']
        price_col = mappings.get('price')
        
        try:
            df_clean = df.dropna(subset=[category_col, qty_col])
            
            if price_col:
                df_clean = df_clean.dropna(subset=[price_col])
                df_clean['revenue'] = df_clean[qty_col] * df_clean[price_col]
                
                category_analysis = df_clean.groupby(category_col).agg({
                    qty_col: 'sum',
                    'revenue': 'sum',
                    price_col: 'mean'
                }).round(2)
                
                total_revenue = df_clean['revenue'].sum()
                total_units = df_clean[qty_col].sum()
                
                insights['category_performance'] = []
                for category, row in category_analysis.sort_values('revenue', ascending=False).iterrows():
                    insights['category_performance'].append({
                        'category': str(category),
                        'total_revenue': float(row['revenue']),
                        'units_sold': int(row[qty_col]),
                        'revenue_share_percent': round(float((row['revenue'] / total_revenue) * 100), 2),
                        'units_share_percent': round(float((row[qty_col] / total_units) * 100), 2),
                        'avg_price': float(row[price_col])
                    })
            
        except Exception as e:
            logger.error(f"Error in category analysis: {str(e)}")
        
        return insights

    def _analyze_brand_performance(self, df: pd.DataFrame, mappings: Dict[str, Optional[str]]) -> Dict[str, Any]:
        """Analyze brand performance"""
        insights = {}
        
        brand_col = mappings['brand']
        qty_col = mappings['quantity_sold']
        price_col = mappings.get('price')
        
        try:
            df_clean = df.dropna(subset=[brand_col, qty_col])
            
            if price_col and not df_clean.empty:
                df_clean = df_clean.dropna(subset=[price_col])
                df_clean['revenue'] = df_clean[qty_col] * df_clean[price_col]
                
                brand_analysis = df_clean.groupby(brand_col).agg({
                    qty_col: 'sum',
                    'revenue': 'sum',
                    price_col: ['mean', 'std']
                }).round(2)
                
                brand_analysis.columns = ['_'.join(col).strip() for col in brand_analysis.columns]
                brand_analysis[f'{price_col}_std'] = brand_analysis[f'{price_col}_std'].fillna(0)
                
                insights['brand_performance'] = []
                for brand, row in brand_analysis.sort_values('revenue_sum', ascending=False).iterrows():
                    insights['brand_performance'].append({
                        'brand': str(brand),
                        'total_revenue': float(row['revenue_sum']),
                        'units_sold': int(row[f'{qty_col}_sum']),
                        'avg_price': float(row[f'{price_col}_mean']),
                        'price_consistency': float(row[f'{price_col}_std'])
                    })
            
        except Exception as e:
            logger.error(f"Error in brand analysis: {str(e)}")
        
        return insights

    def _analyze_inventory_metrics(self, df: pd.DataFrame, mappings: Dict[str, Optional[str]]) -> Dict[str, Any]:
        """Analyze inventory levels and turnover"""
        insights = {}
        
        inventory_col = mappings.get('inventory_level')
        product_col = mappings.get('product_name')
        qty_sold_col = mappings.get('quantity_sold')
        
        try:
            if inventory_col:
                df_clean = df.dropna(subset=[inventory_col])
                
                if not df_clean.empty:
                    insights['inventory_metrics'] = {
                        'total_inventory_value': float(df_clean[inventory_col].sum()),
                        'avg_inventory_per_product': float(df_clean[inventory_col].mean()),
                        'low_stock_products': len(df_clean[df_clean[inventory_col] <= df_clean[inventory_col].quantile(0.1)]),
                        'overstock_products': len(df_clean[df_clean[inventory_col] >= df_clean[inventory_col].quantile(0.9)]),
                        'out_of_stock': len(df_clean[df_clean[inventory_col] == 0])
                    }
                    
                    if product_col:
                        stock_analysis = df_clean.groupby(product_col)[inventory_col].sum().sort_values(ascending=True)
                        
                        insights['inventory_alerts'] = {
                            'low_stock_items': [
                                {'product': str(product), 'stock_level': int(stock)}
                                for product, stock in stock_analysis.head(10).items()
                            ],
                            'high_stock_items': [
                                {'product': str(product), 'stock_level': int(stock)}
                                for product, stock in stock_analysis.tail(10).items()
                            ]
                        }
            
        except Exception as e:
            logger.error(f"Error in inventory analysis: {str(e)}")
        
        return insights

    def _analyze_pricing_strategy(self, df: pd.DataFrame, mappings: Dict[str, Optional[str]]) -> Dict[str, Any]:
        """Analyze pricing and margin strategies"""
        insights = {}
        
        price_col = mappings.get('price')
        cost_col = mappings.get('cost')
        margin_col = mappings.get('margin')
        discount_col = mappings.get('discount')
        
        try:
            if price_col:
                df_clean = df.dropna(subset=[price_col])
                
                if not df_clean.empty:
                    insights['pricing_metrics'] = {
                        'avg_selling_price': float(df_clean[price_col].mean()),
                        'median_price': float(df_clean[price_col].median()),
                        'price_range': {
                            'min': float(df_clean[price_col].min()),
                            'max': float(df_clean[price_col].max())
                        },
                        'price_std_dev': float(df_clean[price_col].std())
                    }
                    
                    # Calculate margins if cost is available
                    if cost_col:
                        df_margins = df_clean.dropna(subset=[cost_col])
                        if not df_margins.empty:
                            df_margins['calculated_margin'] = ((df_margins[price_col] - df_margins[cost_col]) / df_margins[price_col] * 100)
                            
                            insights['margin_analysis'] = {
                                'avg_margin_percent': float(df_margins['calculated_margin'].mean()),
                                'median_margin_percent': float(df_margins['calculated_margin'].median()),
                                'margin_range': {
                                    'min': float(df_margins['calculated_margin'].min()),
                                    'max': float(df_margins['calculated_margin'].max())
                                }
                            }
                    
                    # Discount analysis
                    if discount_col:
                        df_discounts = df_clean.dropna(subset=[discount_col])
                        if not df_discounts.empty:
                            insights['discount_analysis'] = {
                                'avg_discount_percent': float(df_discounts[discount_col].mean()),
                                'total_discount_transactions': len(df_discounts[df_discounts[discount_col] > 0]),
                                'discount_penetration': float((len(df_discounts[df_discounts[discount_col] > 0]) / len(df_discounts)) * 100)
                            }
            
        except Exception as e:
            logger.error(f"Error in pricing analysis: {str(e)}")
        
        return insights

    def _analyze_store_performance(self, df: pd.DataFrame, mappings: Dict[str, Optional[str]]) -> Dict[str, Any]:
        """Analyze performance across different stores"""
        insights = {}
        
        store_col = mappings['store']
        qty_col = mappings['quantity_sold']
        price_col = mappings.get('price')
        
        try:
            df_clean = df.dropna(subset=[store_col, qty_col])
            
            if price_col and not df_clean.empty:
                df_clean = df_clean.dropna(subset=[price_col])
                df_clean['revenue'] = df_clean[qty_col] * df_clean[price_col]
                
                store_performance = df_clean.groupby(store_col).agg({
                    'revenue': ['sum', 'mean'],
                    qty_col: ['sum', 'count']
                }).round(2)
                
                store_performance.columns = ['_'.join(col).strip() for col in store_performance.columns]
                store_performance = store_performance.sort_values('revenue_sum', ascending=False)
                
                insights['store_performance'] = []
                for store, row in store_performance.iterrows():
                    insights['store_performance'].append({
                        'store': str(store),
                        'total_revenue': float(row['revenue_sum']),
                        'avg_transaction_value': float(row['revenue_mean']),
                        'units_sold': int(row[f'{qty_col}_sum']),
                        'total_transactions': int(row[f'{qty_col}_count'])
                    })
            
        except Exception as e:
            logger.error(f"Error in store performance analysis: {str(e)}")
        
        return insights

    def _analyze_seasonal_trends(self, df: pd.DataFrame, mappings: Dict[str, Optional[str]]) -> Dict[str, Any]:
        """Analyze seasonal and time-based trends"""
        insights = {}
        
        date_col = mappings['date']
        qty_col = mappings['quantity_sold']
        price_col = mappings.get('price')
        
        try:
            df_clean = df.dropna(subset=[date_col, qty_col])
            if df_clean.empty:
                return {}
            
            # Convert to datetime
            date_formats = ['%Y-%m-%d', '%m/%d/%Y', '%d/%m/%Y', '%Y-%m-%d %H:%M:%S']
            for fmt in date_formats:
                try:
                    df_clean[date_col] = pd.to_datetime(df_clean[date_col], format=fmt)
                    break
                except:
                    continue
            else:
                df_clean[date_col] = pd.to_datetime(df_clean[date_col], errors='coerce')
            
            df_clean = df_clean.dropna(subset=[date_col])
            if df_clean.empty:
                return {}
            
            # Monthly trends
            df_clean['month'] = df_clean[date_col].dt.month
            df_clean['season'] = df_clean['month'].map({12: 'Winter', 1: 'Winter', 2: 'Winter',
                                                       3: 'Spring', 4: 'Spring', 5: 'Spring',
                                                       6: 'Summer', 7: 'Summer', 8: 'Summer',
                                                       9: 'Fall', 10: 'Fall', 11: 'Fall'})
            
            if price_col:
                df_clean = df_clean.dropna(subset=[price_col])
                df_clean['revenue'] = df_clean[qty_col] * df_clean[price_col]
                
                seasonal_trends = df_clean.groupby('season').agg({
                    'revenue': 'sum',
                    qty_col: 'sum'
                }).round(2)
                
                insights['seasonal_trends'] = []
                for season, row in seasonal_trends.iterrows():
                    insights['seasonal_trends'].append({
                        'season': season,
                        'total_revenue': float(row['revenue']),
                        'units_sold': int(row[qty_col])
                    })
            
            # Day of week patterns
            df_clean['day_of_week'] = df_clean[date_col].dt.day_name()
            daily_sales = df_clean.groupby('day_of_week')[qty_col].sum()
            
            insights['daily_patterns'] = [
                {'day': day, 'units_sold': int(sales)}
                for day, sales in daily_sales.items()
            ]
            
        except Exception as e:
            logger.error(f"Error in seasonal analysis: {str(e)}")
        
        return insights

    def _get_basic_retail_stats(self, df: pd.DataFrame, mappings: Dict[str, Optional[str]]) -> Dict[str, Any]:
        """Get basic retail statistical information"""
        stats = {
            'dataset_info': {
                'total_records': len(df),
                'total_columns': len(df.columns),
                'columns_mapped': len([v for v in mappings.values() if v is not None]),
                'data_completeness': round(float(df.count().sum() / (len(df) * len(df.columns))) * 100, 2)
            }
        }
        
        # Product diversity metrics
        if mappings.get('product_name'):
            stats['product_metrics'] = {
                'unique_products': df[mappings['product_name']].nunique(),
                'avg_records_per_product': round(len(df) / df[mappings['product_name']].nunique(), 2)
            }
        
        if mappings.get('category'):
            stats['category_metrics'] = {
                'unique_categories': df[mappings['category']].nunique()
            }
        
        if mappings.get('brand'):
            stats['brand_metrics'] = {
                'unique_brands': df[mappings['brand']].nunique()
            }
        
        return stats