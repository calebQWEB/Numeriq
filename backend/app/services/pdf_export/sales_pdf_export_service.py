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


class SalesPDFExporter:
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
        """Generate comprehensive sales PDF report"""
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
        
        # Sales Performance Section
        if 'top_sales_reps' in insights:
            story.extend(self._create_sales_performance_section(insights))
            story.append(PageBreak())
        
        # Product Analysis Section
        if 'top_products' in insights or 'revenue_by_category' in insights:
            story.extend(self._create_product_section(insights))
            story.append(PageBreak())
        
        # Customer Analysis Section
        if 'top_customers' in insights:
            story.extend(self._create_customer_section(insights))
            story.append(PageBreak())
        
        # Time Trends Section
        if 'monthly_trends' in insights:
            story.extend(self._create_trends_section(insights))
            story.append(PageBreak())
        
        # Regional Performance Section
        if 'regional_performance' in insights:
            story.extend(self._create_regional_section(insights))
        
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
        
        title = Paragraph("SALES PERFORMANCE REPORT", self.styles['CustomTitle'])
        elements.append(title)
        elements.append(Spacer(1, 0.5*inch))
        
        subtitle = Paragraph(
            f"Comprehensive Sales Analysis: {datetime.now().strftime('%B %d, %Y')}",
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
        
        if 'sales_metrics' in insights:
            metrics = insights['sales_metrics']
            summary_data.append(['Total Revenue', f"${metrics.get('total_revenue', 0):,.2f}"])
            summary_data.append(['Total Transactions', f"{metrics.get('total_transactions', 0):,}"])
            summary_data.append(['Avg Transaction', f"${metrics.get('average_transaction', 0):,.2f}"])
            summary_data.append(['Median Transaction', f"${metrics.get('median_transaction', 0):,.2f}"])
        
        if 'customer_metrics' in insights:
            cust = insights['customer_metrics']
            summary_data.append(['Total Customers', f"{cust.get('total_customers', 0):,}"])
            summary_data.append(['Avg Customer Value', f"${cust.get('avg_customer_value', 0):,.2f}"])
        
        if 'growth_metrics' in insights:
            growth = insights['growth_metrics']
            summary_data.append(['Monthly Growth', f"{growth.get('monthly_growth_rate', 0):+.1f}%"])
            summary_data.append(['Trend', growth.get('trend_direction', 'N/A').title()])
        
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
    
    def _create_sales_performance_section(self, insights: Dict[str, Any]) -> List:
        """Create sales representative performance section"""
        elements = []
        elements.append(Paragraph("Sales Team Performance", self.styles['SectionHeader']))
        elements.append(Spacer(1, 0.2*inch))
        
        sales_reps = insights['top_sales_reps']
        
        # Best performer highlight
        if 'best_performer' in sales_reps:
            best = sales_reps['best_performer']
            elements.append(Paragraph("Top Performer", self.styles['SubHeader']))
            
            best_data = [
                ['Metric', 'Value'],
                ['Sales Representative', best['name']],
                ['Total Sales', f"${best['total_sales']:,.2f}"],
                ['Transactions', f"{best['transactions']:,}"],
                ['Avg Transaction', f"${best['avg_transaction']:,.2f}"],
                ['Consistency Score', f"{best['consistency']:.2f}"]
            ]
            
            col_widths = [TWO_COL_WIDTH, TWO_COL_WIDTH]
            best_table = self._create_styled_table(best_data, col_widths=col_widths, align_values_right=True)
            elements.append(best_table)
            elements.append(Spacer(1, 0.3*inch))
        
        # All sales reps performance
        if 'all_reps' in sales_reps:
            elements.append(Paragraph("All Sales Representatives", self.styles['SubHeader']))
            
            reps_data = [['Rep Name', 'Total Sales', 'Transactions', 'Avg Sale', 'Consistency']]
            for rep in sales_reps['all_reps']:
                reps_data.append([
                    rep['name'][:30],
                    f"${rep['total_sales']:,.2f}",
                    f"{rep['transactions']:,}",
                    f"${rep['avg_transaction']:,.2f}",
                    f"{rep['consistency']:.2f}"
                ])
            
            col_widths = [DRAWING_WIDTH * 0.3, DRAWING_WIDTH * 0.2, DRAWING_WIDTH * 0.15, DRAWING_WIDTH * 0.2, DRAWING_WIDTH * 0.15]
            reps_table = self._create_styled_table(reps_data, col_widths=col_widths, align_values_right=True)
            elements.append(reps_table)
            elements.append(Spacer(1, 0.3*inch))
            
            # Create performance chart
            chart_data = sales_reps['all_reps'][:10]  # Top 10 for chart
            if chart_data:
                elements.append(Paragraph("Sales Performance Comparison", self.styles['SubHeader']))
                chart = self._create_horizontal_bar_chart(
                    chart_data,
                    'name', 'total_sales',
                    "Sales by Representative"
                )
                chart_container = Table([[chart]], colWidths=[DRAWING_WIDTH])
                chart_container.setStyle(TableStyle([('ALIGN', (0,0), (-1,-1), 'CENTER')]))
                elements.append(chart_container)
        
        return elements
    
    def _create_product_section(self, insights: Dict[str, Any]) -> List:
        """Create product performance section"""
        elements = []
        elements.append(Paragraph("Product Performance Analysis", self.styles['SectionHeader']))
        elements.append(Spacer(1, 0.2*inch))
        
        # Top products
        if 'top_products' in insights:
            elements.append(Paragraph("Top 10 Products by Revenue", self.styles['SubHeader']))
            
            product_data = [['Product', 'Revenue', 'Units Sold', 'Avg Revenue/Sale']]
            for product in insights['top_products']:
                product_data.append([
                    product['name'][:35],
                    f"${product['total_revenue']:,.2f}",
                    f"{product['units_sold']:,}",
                    f"${product['avg_revenue_per_sale']:,.2f}"
                ])
            
            col_widths = [DRAWING_WIDTH * 0.4, DRAWING_WIDTH * 0.2, DRAWING_WIDTH * 0.2, DRAWING_WIDTH * 0.2]
            product_table = self._create_styled_table(product_data, col_widths=col_widths, align_values_right=True)
            elements.append(product_table)
            elements.append(Spacer(1, 0.3*inch))
        
        # Revenue by category
        if 'revenue_by_category' in insights:
            left_content = [Paragraph("Revenue by Category", self.styles['SubHeader'])]
            chart = self._create_pie_chart(
                insights['revenue_by_category'][:6],
                'category', 'revenue',
                "Category Distribution"
            )
            left_content.append(chart)
            
            right_content = [Paragraph("Category Breakdown", self.styles['SubHeader'])]
            cat_data = [['Category', 'Revenue', 'Transactions']]
            for cat in insights['revenue_by_category']:
                cat_data.append([
                    cat['category'][:25],
                    f"${cat['revenue']:,.2f}",
                    f"{cat['transactions']:,}"
                ])
            
            cat_col_widths = [TWO_COL_WIDTH * 0.5, TWO_COL_WIDTH * 0.25, TWO_COL_WIDTH * 0.25]
            cat_table = self._create_styled_table(cat_data, col_widths=cat_col_widths, align_values_right=True)
            right_content.append(cat_table)
            
            side_by_side = Table([[left_content, right_content]], colWidths=[TWO_COL_WIDTH, TWO_COL_WIDTH])
            side_by_side.setStyle(TableStyle([
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('LEFTPADDING', (1, 0), (1, 0), 15),
            ]))
            elements.append(side_by_side)
        
        return elements
    
    def _create_customer_section(self, insights: Dict[str, Any]) -> List:
        """Create customer analysis section"""
        elements = []
        elements.append(Paragraph("Customer Analysis", self.styles['SectionHeader']))
        elements.append(Spacer(1, 0.2*inch))
        
        # Customer metrics overview
        if 'customer_metrics' in insights:
            cust = insights['customer_metrics']
            
            left_content = [Paragraph("Customer Overview", self.styles['SubHeader'])]
            metrics_data = [
                ['Metric', 'Value'],
                ['Total Customers', f"{cust.get('total_customers', 0):,}"],
                ['Avg Customer Value', f"${cust.get('avg_customer_value', 0):,.2f}"],
                ['Median Customer Value', f"${cust.get('median_customer_value', 0):,.2f}"],
                ['Top Customer Value', f"${cust.get('top_customer_value', 0):,.2f}"]
            ]
            col_widths = [TWO_COL_WIDTH * 0.6, TWO_COL_WIDTH * 0.4]
            metrics_table = self._create_styled_table(metrics_data, col_widths=col_widths, align_values_right=True)
            left_content.append(metrics_table)
            
            right_content = []
            if 'customer_concentration' in cust:
                conc = cust['customer_concentration']
                right_content.append(Paragraph("Customer Concentration", self.styles['SubHeader']))
                conc_data = [
                    ['Metric', 'Value'],
                    ['Top 10% Revenue Share', f"{conc.get('top_10_percent_revenue_share', 0):.1f}%"],
                    ['Top Customer Share', f"{conc.get('top_customer_revenue_share', 0):.1f}%"]
                ]
                col_widths = [TWO_COL_WIDTH * 0.6, TWO_COL_WIDTH * 0.4]
                conc_table = self._create_styled_table(conc_data, col_widths=col_widths, align_values_right=True)
                right_content.append(conc_table)
            
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
        
        # Top customers
        if 'top_customers' in insights:
            elements.append(Paragraph("Top 10 Customers by Revenue", self.styles['SubHeader']))
            
            customer_data = [['Customer', 'Total Spent', 'Transactions', 'Avg Transaction']]
            for customer in insights['top_customers']:
                customer_data.append([
                    customer['name'][:35],
                    f"${customer['total_spent']:,.2f}",
                    f"{customer['transactions']:,}",
                    f"${customer['avg_transaction']:,.2f}"
                ])
            
            col_widths = [DRAWING_WIDTH * 0.4, DRAWING_WIDTH * 0.2, DRAWING_WIDTH * 0.2, DRAWING_WIDTH * 0.2]
            customer_table = self._create_styled_table(customer_data, col_widths=col_widths, align_values_right=True)
            elements.append(customer_table)
        
        return elements
    
    def _create_trends_section(self, insights: Dict[str, Any]) -> List:
        """Create time trends section"""
        elements = []
        elements.append(Paragraph("Sales Trends Analysis", self.styles['SectionHeader']))
        elements.append(Spacer(1, 0.2*inch))
        
        # Monthly trends chart
        if 'monthly_trends' in insights:
            elements.append(Paragraph("Monthly Revenue Trends", self.styles['SubHeader']))
            chart = self._create_line_chart(
                insights['monthly_trends'],
                'month', 'revenue',
                "Monthly Sales"
            )
            chart_container = Table([[chart]], colWidths=[DRAWING_WIDTH])
            chart_container.setStyle(TableStyle([('ALIGN', (0,0), (-1,-1), 'CENTER')]))
            elements.append(chart_container)
            elements.append(Spacer(1, 0.3*inch))
            
            # Monthly data table
            elements.append(Paragraph("Monthly Performance Details", self.styles['SubHeader']))
            monthly_data = [['Month', 'Revenue', 'Transactions']]
            for month in insights['monthly_trends']:
                monthly_data.append([
                    str(month['month'])[-7:],
                    f"${month['revenue']:,.2f}",
                    f"{month['transactions']:,}"
                ])
            
            col_widths = [DRAWING_WIDTH * 0.4, DRAWING_WIDTH * 0.3, DRAWING_WIDTH * 0.3]
            monthly_table = self._create_styled_table(monthly_data, col_widths=col_widths, align_values_right=True)
            elements.append(monthly_table)
            elements.append(Spacer(1, 0.3*inch))
        
        # Growth metrics
        if 'growth_metrics' in insights:
            growth = insights['growth_metrics']
            elements.append(Paragraph("Growth Analysis", self.styles['SubHeader']))
            
            growth_data = [
                ['Metric', 'Value'],
                ['Monthly Growth Rate', f"{growth.get('monthly_growth_rate', 0):+.2f}%"],
                ['Trend Direction', growth.get('trend_direction', 'N/A').title()]
            ]
            
            col_widths = [TWO_COL_WIDTH, TWO_COL_WIDTH]
            growth_table = self._create_styled_table(growth_data, col_widths=col_widths, align_values_right=True)
            elements.append(growth_table)
            elements.append(Spacer(1, 0.3*inch))
        
        # Daily patterns
        if 'daily_patterns' in insights:
            elements.append(Paragraph("Day of Week Performance", self.styles['SubHeader']))
            chart = self._create_bar_chart(
                insights['daily_patterns'],
                'day', 'total_revenue',
                "Revenue by Day"
            )
            chart_container = Table([[chart]], colWidths=[DRAWING_WIDTH])
            chart_container.setStyle(TableStyle([('ALIGN', (0,0), (-1,-1), 'CENTER')]))
            elements.append(chart_container)
        
        return elements
    
    def _create_regional_section(self, insights: Dict[str, Any]) -> List:
        """Create regional performance section"""
        elements = []
        elements.append(Paragraph("Regional Performance Analysis", self.styles['SectionHeader']))
        elements.append(Spacer(1, 0.2*inch))
        
        elements.append(Paragraph("Performance by Region", self.styles['SubHeader']))
        regional_data = [['Region', 'Revenue', 'Revenue %', 'Transactions', 'Avg Transaction']]
        for region in insights['regional_performance']:
            regional_data.append([
                region['region'][:30],
                f"${region['total_revenue']:,.2f}",
                f"{region['revenue_share_percent']:.1f}%",
                f"{region['transactions']:,}",
                f"${region['avg_transaction']:,.2f}"
            ])
        
        col_widths = [DRAWING_WIDTH * 0.3, DRAWING_WIDTH * 0.2, DRAWING_WIDTH * 0.15, DRAWING_WIDTH * 0.15, DRAWING_WIDTH * 0.2]
        regional_table = self._create_styled_table(regional_data, col_widths=col_widths, align_values_right=True)
        elements.append(regional_table)
        elements.append(Spacer(1, 0.3*inch))
        
        # Regional chart
        elements.append(Paragraph("Regional Revenue Distribution", self.styles['SubHeader']))
        chart = self._create_horizontal_bar_chart(
            insights['regional_performance'][:10],
            'region', 'total_revenue',
            "Revenue by Region"
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
        
    def _create_horizontal_bar_chart(self, data: List[Dict], label_key: str, value_key: str, title: str) -> Drawing:
        """Create a horizontal bar chart"""
        drawing = Drawing(DRAWING_WIDTH, 300)
        
        chart = HorizontalBarChart()
        chart.x = 100
        chart.y = 30
        chart.height = 250
        chart.width = DRAWING_WIDTH - 150
        
        chart.data = [[item[value_key] for item in data[:10]]]
        chart.categoryAxis.categoryNames = [item[label_key][:25] for item in data[:10]]
        chart.categoryAxis.labels.fontSize = 9
        chart.categoryAxis.labels.fontName = 'Helvetica'
        chart.valueAxis.labels.fontName = 'Helvetica'
        chart.valueAxis.labels.fontSize = 9
        chart.bars[0].fillColor = self.colors['info']
        
        drawing.add(chart)
        return drawing
    
    def _create_line_chart(self, data: List[Dict], label_key: str, value_key: str, title: str) -> Drawing:
        """Create a line chart"""
        drawing = Drawing(DRAWING_WIDTH, 250)
        
        chart = HorizontalLineChart()
        chart.x = 50
        chart.y = 50
        chart.height = 175
        chart.width = DRAWING_WIDTH - 100
        
        chart.data = [[item[value_key] for item in data[:12]]]
        chart.categoryAxis.categoryNames = [str(item[label_key])[-7:] for item in data[:12]]
        chart.categoryAxis.labels.angle = 30
        chart.categoryAxis.labels.fontSize = 8
        chart.valueAxis.labels.fontName = 'Helvetica'
        chart.valueAxis.labels.fontSize = 9
        chart.lines[0].strokeColor = self.colors['primary']
        chart.lines[0].strokeWidth = 2
        
        drawing.add(chart)
        return drawing


# Main function to export sales insights to PDF
def export_sales_to_pdf(insights: Dict[str, Any], company_name: str = "Company") -> bytes:
    """
    Export sales insights to PDF
    
    Args:
        insights: Dictionary containing sales insights from SalesAnalysisService
        company_name: Optional company name for the report
    
    Returns:
        PDF file as bytes
    """
    exporter = SalesPDFExporter()
    pdf_bytes = exporter.generate_pdf(insights)
    return pdf_bytes


def save_sales_pdf(insights: Dict[str, Any], output_path: str):
    """
    Save sales insights to a PDF file
    
    Args:
        insights: Dictionary containing sales insights
        output_path: Path where PDF should be saved
    """
    exporter = SalesPDFExporter()
    exporter.generate_pdf(insights, output_path=output_path)