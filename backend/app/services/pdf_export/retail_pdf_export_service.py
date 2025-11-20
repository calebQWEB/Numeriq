from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, 
    PageBreak, KeepTogether
)
from reportlab.graphics.shapes import Drawing, Line
from reportlab.graphics.charts.barcharts import VerticalBarChart, HorizontalBarChart
from reportlab.graphics.charts.piecharts import Pie
from reportlab.graphics.charts.linecharts import HorizontalLineChart
from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT
from datetime import datetime
import io
from typing import Dict, Any, List

# Page layout constants
PAGE_SIZE = letter
PAGE_WIDTH, PAGE_HEIGHT = PAGE_SIZE
REPORT_MARGIN = 0.75 * inch
DRAWING_WIDTH = PAGE_WIDTH - 2 * REPORT_MARGIN
TWO_COL_WIDTH = DRAWING_WIDTH / 2.0
FIXED_COL_WIDTH = DRAWING_WIDTH / 4.0


class RetailPDFExporter:
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self.colors = {
            'primary': colors.HexColor('#2563eb'),
            'secondary': colors.HexColor('#7c3aed'),
            'success': colors.HexColor('#16a34a'),
            'warning': colors.HexColor('#ea580c'),
            'danger': colors.HexColor('#dc2626'),
            'info': colors.HexColor('#0891b2'),
            'light_bg': colors.HexColor('#f1f5f9'),
            'dark_text': colors.HexColor('#1e293b'),
            'header_bg': colors.HexColor('#e0f2fe')
        }
        self.setup_custom_styles()
    
    def setup_custom_styles(self):
        """Setup custom paragraph styles"""
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=28,
            textColor=self.colors['dark_text'],
            spaceAfter=30,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        ))
        
        self.styles.add(ParagraphStyle(
            name='SectionHeader',
            parent=self.styles['Heading2'],
            fontSize=18,
            textColor=self.colors['primary'],
            spaceAfter=15,
            spaceBefore=25,
            fontName='Helvetica-Bold'
        ))
        
        self.styles.add(ParagraphStyle(
            name='SubHeader',
            parent=self.styles['Heading3'],
            fontSize=14,
            textColor=self.colors['dark_text'],
            spaceAfter=10,
            spaceBefore=15,
            fontName='Helvetica-Bold'
        ))
        
        self.styles.add(ParagraphStyle(
            name='ReportDate',
            parent=self.styles['Normal'],
            fontSize=10,
            textColor=colors.grey,
            alignment=TA_CENTER
        ))

    def generate_pdf(self, insights: Dict[str, Any], output_path: str = None) -> bytes:
        """Generate comprehensive retail PDF report"""
        if output_path is None:
            buffer = io.BytesIO()
            doc = SimpleDocTemplate(
                buffer, pagesize=PAGE_SIZE,
                rightMargin=REPORT_MARGIN, leftMargin=REPORT_MARGIN,
                topMargin=REPORT_MARGIN, bottomMargin=REPORT_MARGIN
            )
        else:
            doc = SimpleDocTemplate(
                output_path, pagesize=PAGE_SIZE,
                rightMargin=REPORT_MARGIN, leftMargin=REPORT_MARGIN,
                topMargin=REPORT_MARGIN, bottomMargin=REPORT_MARGIN
            )
        
        story = []
        
        # Title Page
        story.extend(self._create_title_page())
        story.append(PageBreak())
        
        # Executive Summary
        story.extend(self._create_executive_summary(insights))
        
        # Product Performance Section
        if 'top_performing_products' in insights or 'top_selling_products' in insights:
            story.extend(self._create_product_section(insights))
            story.append(PageBreak())
        
        # Category Performance Section
        if 'category_performance' in insights:
            story.extend(self._create_category_section(insights))
            story.append(PageBreak())
        
        # Brand Performance Section
        if 'brand_performance' in insights:
            story.extend(self._create_brand_section(insights))
            story.append(PageBreak())
        
        # Inventory Management Section
        if 'inventory_metrics' in insights:
            story.extend(self._create_inventory_section(insights))
            story.append(PageBreak())
        
        # Pricing & Margin Section
        if 'pricing_metrics' in insights:
            story.extend(self._create_pricing_section(insights))
            story.append(PageBreak())
        
        # Store Performance Section
        if 'store_performance' in insights:
            story.extend(self._create_store_section(insights))
            story.append(PageBreak())
        
        # Seasonal Trends Section
        if 'seasonal_trends' in insights or 'daily_patterns' in insights:
            story.extend(self._create_trends_section(insights))
        
        doc.build(story, onFirstPage=self._header_footer, onLaterPages=self._header_footer)
        
        if output_path is None:
            pdf_bytes = buffer.getvalue()
            buffer.close()
            return pdf_bytes
        
        return None
    
    def _header_footer(self, canvas, doc):
        """Add page number footer"""
        canvas.saveState()
        footer_text = f"Page {canvas.getPageNumber()}"
        p = Paragraph(footer_text, self.styles['ReportDate'])
        p.wrapOn(canvas, DRAWING_WIDTH, 10)
        p.drawOn(canvas, REPORT_MARGIN, 0.5 * inch)
        canvas.restoreState()
    
    def _create_title_page(self) -> List:
        """Create title page"""
        elements = []
        elements.append(Spacer(1, 2.5*inch))
        
        title = Paragraph("RETAIL ANALYTICS REPORT", self.styles['CustomTitle'])
        elements.append(title)
        elements.append(Spacer(1, 0.5*inch))
        
        subtitle = Paragraph(
            f"Comprehensive Retail Analysis: {datetime.now().strftime('%B %d, %Y')}",
            self.styles['ReportDate']
        )
        elements.append(subtitle)
        elements.append(Spacer(1, 1.5*inch))
        
        drawing = Drawing(DRAWING_WIDTH, 5)
        drawing.add(Line(0, 2, DRAWING_WIDTH, 2, strokeColor=self.colors['primary'], strokeWidth=3))
        elements.append(drawing)
        
        return elements
    
    def _create_executive_summary(self, insights: Dict[str, Any]) -> List:
        """Create executive summary"""
        elements = []
        elements.append(Paragraph("Executive Summary", self.styles['SectionHeader']))
        elements.append(Spacer(1, 0.2*inch))
        
        summary_data = []
        
        if 'dataset_info' in insights:
            info = insights['dataset_info']
            summary_data.append(['Total Records', f"{info.get('total_records', 0):,}"])
            summary_data.append(['Data Completeness', f"{info.get('data_completeness', 0):.1f}%"])
        
        if 'product_metrics' in insights:
            prod = insights['product_metrics']
            summary_data.append(['Unique Products', f"{prod.get('unique_products', 0):,}"])
        
        if 'category_metrics' in insights:
            cat = insights['category_metrics']
            summary_data.append(['Unique Categories', f"{cat.get('unique_categories', 0):,}"])
        
        if 'brand_metrics' in insights:
            brand = insights['brand_metrics']
            summary_data.append(['Unique Brands', f"{brand.get('unique_brands', 0):,}"])
        
        if 'inventory_metrics' in insights:
            inv = insights['inventory_metrics']
            summary_data.append(['Total Inventory', f"{inv.get('total_inventory_value', 0):,.0f}"])
            summary_data.append(['Out of Stock Items', f"{inv.get('out_of_stock', 0):,}"])
        
        if 'pricing_metrics' in insights:
            price = insights['pricing_metrics']
            summary_data.append(['Avg Selling Price', f"${price.get('avg_selling_price', 0):,.2f}"])
        
        if summary_data:
            if len(summary_data) % 2 != 0:
                summary_data.append(['', ''])
            
            summary_grid = []
            for i in range(0, len(summary_data), 2):
                summary_grid.append(summary_data[i] + summary_data[i+1])
            
            col_widths = [FIXED_COL_WIDTH] * 4
            summary_table = Table(summary_grid, colWidths=col_widths)
            summary_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, -1), colors.white),
                ('TEXTCOLOR', (0, 0), (-1, -1), self.colors['dark_text']),
                ('ALIGN', (0, 0), (0, -1), 'LEFT'),
                ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
                ('ALIGN', (2, 0), (2, -1), 'LEFT'),
                ('ALIGN', (3, 0), (3, -1), 'RIGHT'),
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('FONTNAME', (1, 0), (1, -1), 'Helvetica-Bold'),
                ('FONTNAME', (3, 0), (3, -1), 'Helvetica-Bold'),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
                ('TOPPADDING', (0, 0), (-1, -1), 10),
                ('LINEBEFORE', (2, 0), (2, -1), 1, self.colors['light_bg']),
                ('LINEABOVE', (0, 0), (-1, -1), 0.5, self.colors['light_bg']),
                ('LINEBELOW', (0, -1), (-1, -1), 0.5, self.colors['light_bg']),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ]))
            elements.append(summary_table)
        
        return elements
    
    def _create_product_section(self, insights: Dict[str, Any]) -> List:
        """Create product performance section"""
        elements = []
        elements.append(Paragraph("Product Performance Analysis", self.styles['SectionHeader']))
        elements.append(Spacer(1, 0.2*inch))
        
        # Top performing products (with revenue)
        if 'top_performing_products' in insights:
            elements.append(Paragraph("Top 10 Products by Revenue", self.styles['SubHeader']))
            
            product_data = [['Product', 'Revenue', 'Units Sold', 'Transactions', 'Avg Price']]
            for product in insights['top_performing_products']:
                product_data.append([
                    product['product'][:35],
                    f"${product['total_revenue']:,.2f}",
                    f"{product['units_sold']:,}",
                    f"{product['transactions']:,}",
                    f"${product['avg_price']:,.2f}"
                ])
            
            col_widths = [DRAWING_WIDTH * 0.35, DRAWING_WIDTH * 0.2, DRAWING_WIDTH * 0.15, DRAWING_WIDTH * 0.15, DRAWING_WIDTH * 0.15]
            product_table = self._create_styled_table(product_data, col_widths=col_widths, align_values_right=True)
            elements.append(product_table)
        
        # Top selling products (by units, no revenue)
        elif 'top_selling_products' in insights:
            elements.append(Paragraph("Top 10 Products by Units Sold", self.styles['SubHeader']))
            
            product_data = [['Product', 'Units Sold', 'Transactions', 'Avg Units/Transaction']]
            for product in insights['top_selling_products']:
                product_data.append([
                    product['product'][:40],
                    f"{product['units_sold']:,}",
                    f"{product['transactions']:,}",
                    f"{product['avg_units_per_transaction']:,.2f}"
                ])
            
            col_widths = [DRAWING_WIDTH * 0.5, DRAWING_WIDTH * 0.2, DRAWING_WIDTH * 0.15, DRAWING_WIDTH * 0.15]
            product_table = self._create_styled_table(product_data, col_widths=col_widths, align_values_right=True)
            elements.append(product_table)
        
        return elements
    
    def _create_category_section(self, insights: Dict[str, Any]) -> List:
        """Create category performance section"""
        elements = []
        elements.append(Paragraph("Category Performance Analysis", self.styles['SectionHeader']))
        elements.append(Spacer(1, 0.2*inch))
        
        left_content = [Paragraph("Category Revenue Distribution", self.styles['SubHeader'])]
        chart = self._create_pie_chart(
            insights['category_performance'][:6],
            'category', 'total_revenue',
            "Category Distribution"
        )
        left_content.append(chart)
        
        right_content = [Paragraph("Category Breakdown", self.styles['SubHeader'])]
        cat_data = [['Category', 'Revenue', 'Revenue %', 'Units']]
        for cat in insights['category_performance']:
            cat_data.append([
                cat['category'][:20],
                f"${cat['total_revenue']:,.2f}",
                f"{cat['revenue_share_percent']:.1f}%",
                f"{cat['units_sold']:,}"
            ])
        
        cat_col_widths = [TWO_COL_WIDTH * 0.3, TWO_COL_WIDTH * 0.25, TWO_COL_WIDTH * 0.2, TWO_COL_WIDTH * 0.25]
        cat_table = self._create_styled_table(cat_data, col_widths=cat_col_widths, align_values_right=True)
        right_content.append(cat_table)
        
        side_by_side = Table([[left_content, right_content]], colWidths=[TWO_COL_WIDTH, TWO_COL_WIDTH])
        side_by_side.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('LEFTPADDING', (1, 0), (1, 0), 15),
        ]))
        elements.append(side_by_side)
        
        return elements
    
    def _create_brand_section(self, insights: Dict[str, Any]) -> List:
        """Create brand performance section"""
        elements = []
        elements.append(Paragraph("Brand Performance Analysis", self.styles['SectionHeader']))
        elements.append(Spacer(1, 0.2*inch))
        
        elements.append(Paragraph("Top Brands by Revenue", self.styles['SubHeader']))
        brand_data = [['Brand', 'Revenue', 'Units Sold', 'Avg Price', 'Price Consistency']]
        for brand in insights['brand_performance']:
            brand_data.append([
                brand['brand'][:30],
                f"${brand['total_revenue']:,.2f}",
                f"{brand['units_sold']:,}",
                f"${brand['avg_price']:,.2f}",
                f"${brand['price_consistency']:,.2f}"
            ])
        
        col_widths = [DRAWING_WIDTH * 0.3, DRAWING_WIDTH * 0.2, DRAWING_WIDTH * 0.15, DRAWING_WIDTH * 0.175, DRAWING_WIDTH * 0.175]
        brand_table = self._create_styled_table(brand_data, col_widths=col_widths, align_values_right=True)
        elements.append(brand_table)
        elements.append(Spacer(1, 0.3*inch))
        
        # Brand chart
        elements.append(Paragraph("Brand Revenue Comparison", self.styles['SubHeader']))
        chart = self._create_horizontal_bar_chart(
            insights['brand_performance'][:10],
            'brand', 'total_revenue',
            "Revenue by Brand"
        )
        chart_container = Table([[chart]], colWidths=[DRAWING_WIDTH])
        chart_container.setStyle(TableStyle([('ALIGN', (0,0), (-1,-1), 'CENTER')]))
        elements.append(chart_container)
        
        return elements
    
    def _create_inventory_section(self, insights: Dict[str, Any]) -> List:
        """Create inventory management section"""
        elements = []
        elements.append(Paragraph("Inventory Management", self.styles['SectionHeader']))
        elements.append(Spacer(1, 0.2*inch))
        
        inv = insights['inventory_metrics']
        
        left_content = [Paragraph("Inventory Overview", self.styles['SubHeader'])]
        inv_data = [
            ['Metric', 'Value'],
            ['Total Inventory', f"{inv.get('total_inventory_value', 0):,.0f}"],
            ['Avg Inventory/Product', f"{inv.get('avg_inventory_per_product', 0):,.2f}"],
            ['Low Stock Products', f"{inv.get('low_stock_products', 0):,}"],
            ['Overstock Products', f"{inv.get('overstock_products', 0):,}"],
            ['Out of Stock', f"{inv.get('out_of_stock', 0):,}"]
        ]
        col_widths = [TWO_COL_WIDTH * 0.6, TWO_COL_WIDTH * 0.4]
        inv_table = self._create_styled_table(inv_data, col_widths=col_widths, align_values_right=True)
        left_content.append(inv_table)
        
        right_content = []
        if 'inventory_alerts' in insights:
            alerts = insights['inventory_alerts']
            if 'low_stock_items' in alerts and alerts['low_stock_items']:
                right_content.append(Paragraph("Low Stock Alert (Top 5)", self.styles['SubHeader']))
                alert_data = [['Product', 'Stock Level']]
                for item in alerts['low_stock_items'][:5]:
                    alert_data.append([
                        item['product'][:25],
                        f"{item['stock_level']:,}"
                    ])
                alert_col_widths = [TWO_COL_WIDTH * 0.7, TWO_COL_WIDTH * 0.3]
                alert_table = self._create_styled_table(alert_data, col_widths=alert_col_widths, align_values_right=True, highlight_warning=True)
                right_content.append(alert_table)
        
        if left_content and right_content:
            side_by_side = Table([[left_content, right_content]], colWidths=[TWO_COL_WIDTH, TWO_COL_WIDTH])
            side_by_side.setStyle(TableStyle([
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('LEFTPADDING', (1, 0), (1, 0), 15),
            ]))
            elements.append(side_by_side)
        elif left_content:
            elements.extend(left_content)
        
        return elements
    
    def _create_pricing_section(self, insights: Dict[str, Any]) -> List:
        """Create pricing and margin section"""
        elements = []
        elements.append(Paragraph("Pricing & Margin Analysis", self.styles['SectionHeader']))
        elements.append(Spacer(1, 0.2*inch))
        
        pricing = insights['pricing_metrics']
        
        left_content = [Paragraph("Pricing Metrics", self.styles['SubHeader'])]
        price_data = [
            ['Metric', 'Value'],
            ['Avg Selling Price', f"${pricing.get('avg_selling_price', 0):,.2f}"],
            ['Median Price', f"${pricing.get('median_price', 0):,.2f}"],
            ['Min Price', f"${pricing.get('price_range', {}).get('min', 0):,.2f}"],
            ['Max Price', f"${pricing.get('price_range', {}).get('max', 0):,.2f}"],
            ['Price Std Dev', f"${pricing.get('price_std_dev', 0):,.2f}"]
        ]
        col_widths = [TWO_COL_WIDTH * 0.6, TWO_COL_WIDTH * 0.4]
        price_table = self._create_styled_table(price_data, col_widths=col_widths, align_values_right=True)
        left_content.append(price_table)
        
        right_content = []
        if 'margin_analysis' in insights:
            margin = insights['margin_analysis']
            right_content.append(Paragraph("Margin Analysis", self.styles['SubHeader']))
            margin_data = [
                ['Metric', 'Value'],
                ['Avg Margin', f"{margin.get('avg_margin_percent', 0):.1f}%"],
                ['Median Margin', f"{margin.get('median_margin_percent', 0):.1f}%"],
                ['Min Margin', f"{margin.get('margin_range', {}).get('min', 0):.1f}%"],
                ['Max Margin', f"{margin.get('margin_range', {}).get('max', 0):.1f}%"]
            ]
            col_widths = [TWO_COL_WIDTH * 0.6, TWO_COL_WIDTH * 0.4]
            margin_table = self._create_styled_table(margin_data, col_widths=col_widths, align_values_right=True)
            right_content.append(margin_table)
        
        if left_content and right_content:
            side_by_side = Table([[left_content, right_content]], colWidths=[TWO_COL_WIDTH, TWO_COL_WIDTH])
            side_by_side.setStyle(TableStyle([
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('LEFTPADDING', (1, 0), (1, 0), 15),
            ]))
            elements.append(side_by_side)
        elif left_content:
            elements.extend(left_content)
        
        elements.append(Spacer(1, 0.3*inch))
        
        # Discount analysis
        if 'discount_analysis' in insights:
            elements.append(Paragraph("Discount Analysis", self.styles['SubHeader']))
            discount = insights['discount_analysis']
            discount_data = [
                ['Metric', 'Value'],
                ['Avg Discount', f"{discount.get('avg_discount_percent', 0):.1f}%"],
                ['Discount Transactions', f"{discount.get('total_discount_transactions', 0):,}"],
                ['Discount Penetration', f"{discount.get('discount_penetration', 0):.1f}%"]
            ]
            col_widths = [TWO_COL_WIDTH, TWO_COL_WIDTH]
            discount_table = self._create_styled_table(discount_data, col_widths=col_widths, align_values_right=True)
            elements.append(discount_table)
        
        return elements
    
    def _create_store_section(self, insights: Dict[str, Any]) -> List:
        """Create store performance section"""
        elements = []
        elements.append(Paragraph("Store Performance Analysis", self.styles['SectionHeader']))
        elements.append(Spacer(1, 0.2*inch))
        
        elements.append(Paragraph("Store Performance Comparison", self.styles['SubHeader']))
        store_data = [['Store', 'Revenue', 'Avg Transaction', 'Units Sold', 'Transactions']]
        for store in insights['store_performance']:
            store_data.append([
                str(store['store'])[:25],
                f"${store['total_revenue']:,.2f}",
                f"${store['avg_transaction_value']:,.2f}",
                f"{store['units_sold']:,}",
                f"{store['total_transactions']:,}"
            ])
        
        col_widths = [DRAWING_WIDTH * 0.25, DRAWING_WIDTH * 0.2, DRAWING_WIDTH * 0.2, DRAWING_WIDTH * 0.175, DRAWING_WIDTH * 0.175]
        store_table = self._create_styled_table(store_data, col_widths=col_widths, align_values_right=True)
        elements.append(store_table)
        elements.append(Spacer(1, 0.3*inch))
        
        # Store chart
        elements.append(Paragraph("Store Revenue Distribution", self.styles['SubHeader']))
        chart = self._create_horizontal_bar_chart(
            insights['store_performance'][:10],
            'store', 'total_revenue',
            "Revenue by Store"
        )
        chart_container = Table([[chart]], colWidths=[DRAWING_WIDTH])
        chart_container.setStyle(TableStyle([('ALIGN', (0,0), (-1,-1), 'CENTER')]))
        elements.append(chart_container)
        
        return elements
    
    def _create_trends_section(self, insights: Dict[str, Any]) -> List:
        """Create seasonal trends section"""
        elements = []
        elements.append(Paragraph("Seasonal & Time Trends", self.styles['SectionHeader']))
        elements.append(Spacer(1, 0.2*inch))
        
        # Seasonal trends
        if 'seasonal_trends' in insights:
            elements.append(Paragraph("Seasonal Performance", self.styles['SubHeader']))
            
            season_data = [['Season', 'Total Revenue', 'Units Sold']]
            for season in insights['seasonal_trends']:
                season_data.append([
                    season['season'],
                    f"${season['total_revenue']:,.2f}",
                    f"{season['units_sold']:,}"
                ])
            
            col_widths = [DRAWING_WIDTH * 0.4, DRAWING_WIDTH * 0.3, DRAWING_WIDTH * 0.3]
            season_table = self._create_styled_table(season_data, col_widths=col_widths, align_values_right=True)
            elements.append(season_table)
            elements.append(Spacer(1, 0.3*inch))
        
        # Daily patterns
        if 'daily_patterns' in insights:
            elements.append(Paragraph("Day of Week Sales Pattern", self.styles['SubHeader']))
            chart = self._create_bar_chart(
                insights['daily_patterns'],
                'day', 'units_sold',
                "Sales by Day of Week"
            )
            chart_container = Table([[chart]], colWidths=[DRAWING_WIDTH])
            chart_container.setStyle(TableStyle([('ALIGN', (0,0), (-1,-1), 'CENTER')]))
            elements.append(chart_container)
        
        return elements
    
    def _create_styled_table(self, data: List[List], col_widths: List = None,
                            highlight_warning: bool = False, align_values_right: bool = False) -> Table:
        """Create a styled table"""
        if col_widths is None:
            table = Table(data, colWidths=[DRAWING_WIDTH / len(data[0])] * len(data[0]))
        else:
            table = Table(data, colWidths=col_widths)
        
        style_commands = [
            ('BACKGROUND', (0, 0), (-1, 0), self.colors['primary']),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('TEXTCOLOR', (0, 1), (-1, -1), self.colors['dark_text']),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, self.colors['light_bg']]),
            ('LINEBELOW', (0, 0), (-1, -1), 0.5, colors.lightgrey),
            ('LINEABOVE', (0, 0), (-1, 0), 0.5, colors.lightgrey),
            ('TOPPADDING', (0, 1), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
        ]
        
        if align_values_right and len(data) > 0:
            for col_index in range(1, len(data[0])):
                style_commands.append(('ALIGN', (col_index, 0), (col_index, -1), 'RIGHT'))
        
        if highlight_warning and len(data) > 1:
            style_commands.append(('TEXTCOLOR', (0, 1), (0, -1), self.colors['warning']))
            style_commands.append(('FONTNAME', (0, 1), (0, -1), 'Helvetica-Bold'))
        
        table.setStyle(TableStyle(style_commands))
        return table
    
    def _create_pie_chart(self, data: List[Dict], label_key: str, value_key: str, title: str) -> Drawing:
        """Create a pie chart"""
        drawing = Drawing(TWO_COL_WIDTH, 250)
        
        pie = Pie()
    def _create_pie_chart(self, data: List[Dict], label_key: str, value_key: str, title: str) -> Drawing:
        """Create a pie chart"""
        drawing = Drawing(TWO_COL_WIDTH, 250)
        
        pie = Pie()
        pie.x = TWO_COL_WIDTH / 2 - 75
        pie.y = 50
        pie.width = 150
        pie.height = 150
        
        pie.data = [item[value_key] for item in data[:6]]
        pie.labels = [item[label_key][:15] for item in data[:6]]
        
        pie.sideLabels = 1
        pie.sideLabelsOffset = 1
        pie.slices.fontName = 'Helvetica'
        pie.slices.fontSize = 8
        
        color_list = [self.colors['primary'], self.colors['secondary'], self.colors['info'],
                      self.colors['success'], self.colors['warning'], self.colors['danger']]
        for i, color in enumerate(color_list):
            if i < len(pie.slices):
                pie.slices[i].fillColor = color
        
        drawing.add(pie)
        return drawing
    
    def _create_bar_chart(self, data: List[Dict], label_key: str, value_key: str, title: str) -> Drawing:
        """Create a vertical bar chart"""
        drawing = Drawing(DRAWING_WIDTH, 250)
        
        chart = VerticalBarChart()
        chart.x = 50
        chart.y = 50
        chart.height = 175
        chart.width = DRAWING_WIDTH - 100
        
        chart.data = [[item[value_key] for item in data[:8]]]
        chart.categoryAxis.categoryNames = [item[label_key][:12] for item in data[:8]]
        chart.categoryAxis.labels.angle = 30
        chart.categoryAxis.labels.fontSize = 9
        chart.valueAxis.labels.fontName = 'Helvetica'
        chart.valueAxis.labels.fontSize = 9
        chart.bars[0].fillColor = self.colors['primary']
        
        drawing.add(chart)
        return drawing
    
    def _create_horizontal_bar_chart(self, data: List[Dict], label_key: str, value_key: str, title: str) -> Drawing:
        """Create a horizontal bar chart"""
        drawing = Drawing(DRAWING_WIDTH, 300)
        
        chart = HorizontalBarChart()
        chart.x = 100
        chart.y = 30
        chart.height = 250
        chart.width = DRAWING_WIDTH - 150
        
        chart.data = [[item[value_key] for item in data[:10]]]
        chart.categoryAxis.categoryNames = [str(item[label_key])[:25] for item in data[:10]]
        chart.categoryAxis.labels.fontSize = 9
        chart.categoryAxis.labels.fontName = 'Helvetica'
        chart.valueAxis.labels.fontName = 'Helvetica'
        chart.valueAxis.labels.fontSize = 9
        chart.bars[0].fillColor = self.colors['info']
        
        drawing.add(chart)
        return drawing


# Main function to export retail insights to PDF
def export_retail_to_pdf(insights: Dict[str, Any], company_name: str = "Company") -> bytes:
    """
    Export retail insights to PDF
    
    Args:
        insights: Dictionary containing retail insights from RetailAnalysisService
        company_name: Optional company name for the report
    
    Returns:
        PDF file as bytes
    """
    exporter = RetailPDFExporter()
    pdf_bytes = exporter.generate_pdf(insights)
    return pdf_bytes


def save_retail_pdf(insights: Dict[str, Any], output_path: str):
    """
    Save retail insights to a PDF file
    
    Args:
        insights: Dictionary containing retail insights
        output_path: Path where PDF should be saved
    """
    exporter = RetailPDFExporter()
    exporter.generate_pdf(insights, output_path=output_path)