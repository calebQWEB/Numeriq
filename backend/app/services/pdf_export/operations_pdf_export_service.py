from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, 
    PageBreak, Image, KeepTogether
)
from reportlab.graphics.shapes import Drawing, Line
from reportlab.graphics.charts.barcharts import VerticalBarChart, HorizontalBarChart
from reportlab.graphics.charts.piecharts import Pie
from reportlab.graphics.charts.linecharts import HorizontalLineChart
from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT, TA_JUSTIFY
from datetime import datetime
import io
from typing import Dict, Any, List
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')

# Define standard page dimensions and margins for convenience
PAGE_SIZE = letter
PAGE_WIDTH, PAGE_HEIGHT = PAGE_SIZE
REPORT_MARGIN = 0.75 * inch # Unified margin for better control
DRAWING_WIDTH = PAGE_WIDTH - 2 * REPORT_MARGIN
# Calculate column width for tables that need to span the full page
# For 2-column tables:
TWO_COL_WIDTH = DRAWING_WIDTH / 2.0
# For fixed-column tables:
FIXED_COL_WIDTH = DRAWING_WIDTH / 4.0 


class OperationsPDFExporter:
    # --- Constructor and Setup (Minor Visual Changes) ---
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self.colors = {
            # Keeping your color palette but adding a header background
            'primary': colors.HexColor('#2563eb'),
            'secondary': colors.HexColor('#7c3aed'),
            'success': colors.HexColor('#16a34a'),
            'warning': colors.HexColor('#ea580c'),
            'danger': colors.HexColor('#dc2626'),
            'info': colors.HexColor('#0891b2'),
            'light_bg': colors.HexColor('#f1f5f9'), # Lighter tone for better contrast
            'dark_text': colors.HexColor('#1e293b'),
            'header_bg': colors.HexColor('#e0f2fe') # Light blue background for sections
        }
        self.setup_custom_styles()
    
    def setup_custom_styles(self):
        """Setup custom paragraph styles"""
        # ... (Your existing styles remain)
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=28, # Slightly larger title
            textColor=self.colors['dark_text'],
            spaceAfter=30,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        ))
        
        self.styles.add(ParagraphStyle(
            name='SectionHeader',
            parent=self.styles['Heading2'],
            fontSize=18, # Slightly larger section header
            textColor=self.colors['primary'],
            spaceAfter=15,
            spaceBefore=25,
            fontName='Helvetica-Bold'
        ))
        
        self.styles.add(ParagraphStyle(
            name='SubHeader',
            parent=self.styles['Heading3'],
            fontSize=14,
            textColor=self.colors['dark_text'], # Use dark text for subheaders
            spaceAfter=10,
            spaceBefore=15,
            fontName='Helvetica-Bold'
        ))
        
        self.styles.add(ParagraphStyle(
            name='MetricLabel',
            parent=self.styles['Normal'],
            fontSize=10,
            textColor=colors.HexColor('#64748b'),
            fontName='Helvetica'
        ))
        
        self.styles.add(ParagraphStyle(
            name='MetricValue',
            parent=self.styles['Normal'],
            fontSize=16, # Slightly larger value
            textColor=self.colors['dark_text'],
            fontName='Helvetica-Bold',
            alignment=TA_RIGHT # Ensure metric values align right
        ))
        
        # New style for page footer/subtitle
        self.styles.add(ParagraphStyle(
            name='ReportDate',
            parent=self.styles['Normal'],
            fontSize=10,
            textColor=colors.grey,
            alignment=TA_CENTER
        ))

    # --- PDF Generation (Margin Fix) ---
    def generate_pdf(self, insights: Dict[str, Any], output_path: str = None) -> bytes:
        """Generate comprehensive operations PDF report"""
        
        # **ALIGNMENT FIX: Use calculated margins for full-width content**
        if output_path is None:
            buffer = io.BytesIO()
            doc = SimpleDocTemplate(
                buffer, 
                pagesize=PAGE_SIZE, 
                rightMargin=REPORT_MARGIN, 
                leftMargin=REPORT_MARGIN,
                topMargin=REPORT_MARGIN, 
                bottomMargin=REPORT_MARGIN
            )
        else:
            doc = SimpleDocTemplate(
                output_path, 
                pagesize=PAGE_SIZE,
                rightMargin=REPORT_MARGIN, 
                leftMargin=REPORT_MARGIN,
                topMargin=REPORT_MARGIN, 
                bottomMargin=REPORT_MARGIN
            )
        
        story = []
        
        # Title Page
        story.extend(self._create_title_page())
        story.append(PageBreak())
        
        # ... (Remaining sections remain the same) ...
        # Executive Summary
        story.extend(self._create_executive_summary(insights))
        # No PageBreak here, let content flow naturally after summary

        # Order Fulfillment Section
        if 'order_overview' in insights:
            story.extend(self._create_order_fulfillment_section(insights))
            story.append(PageBreak())
        
        # Inventory Management Section
        if 'inventory_overview' in insights:
            story.extend(self._create_inventory_section(insights))
            story.append(PageBreak())
        
        # Supply Chain Performance Section
        if 'supplier_performance' in insights or 'lead_time_metrics' in insights:
            story.extend(self._create_supply_chain_section(insights))
            story.append(PageBreak())
        
        # Quality Metrics Section
        if 'quality_metrics' in insights:
            story.extend(self._create_quality_section(insights))
            story.append(PageBreak())
        
        # Production Efficiency Section
        if 'production_efficiency' in insights:
            story.extend(self._create_production_section(insights))
            story.append(PageBreak())
        
        # Delivery Performance Section
        if 'delivery_performance' in insights:
            story.extend(self._create_delivery_section(insights))
            story.append(PageBreak())
        
        # Regional Operations Section
        if 'regional_operations' in insights:
            story.extend(self._create_regional_section(insights))
            story.append(PageBreak())
        
        # Cost Analysis Section
        if 'cost_overview' in insights:
            story.extend(self._create_cost_section(insights))
            story.append(PageBreak())
        
        # Operational Trends Section
        if 'monthly_operational_trends' in insights:
            story.extend(self._create_trends_section(insights))
        
        # Use a footer for the page number and date
        doc.build(story, onFirstPage=self._header_footer, onLaterPages=self._header_footer)
        
        if output_path is None:
            pdf_bytes = buffer.getvalue()
            buffer.close()
            return pdf_bytes
        
        return None
    
    # --- New Utility for Header/Footer (Visual Enhancement) ---
    def _header_footer(self, canvas, doc):
        """A simple page number and date footer on every page"""
        canvas.saveState()
        
        # Footer
        footer_text = f"Page {canvas.getPageNumber()}"
        p = Paragraph(footer_text, self.styles['ReportDate'])
        # Position footer slightly above the bottom margin
        p.wrapOn(canvas, DRAWING_WIDTH, 10)
        p.drawOn(canvas, REPORT_MARGIN, 0.5 * inch)
        
        # Header: Date and time on the top right
        date_text = f"Report Date: {datetime.now().strftime('%Y-%m-%d')}"
        p_date = Paragraph(date_text, self.styles['MetricLabel'])
        p_date.wrapOn(canvas, 100, 10)
        p_date.drawOn(canvas, PAGE_WIDTH - REPORT_MARGIN - 100, PAGE_HEIGHT - REPORT_MARGIN + 10)

        canvas.restoreState()

    # --- Section Helpers (Alignment and Visual Fixes) ---
    
    def _create_title_page(self) -> List:
        """Create title page - Improved centering and decorative element"""
        elements = []
        
        elements.append(Spacer(1, 2.5*inch))
        
        title = Paragraph("OPERATIONS ANALYSIS REPORT", self.styles['CustomTitle'])
        elements.append(title)
        
        elements.append(Spacer(1, 0.5*inch))
        
        subtitle = Paragraph(
            f"Detailed Performance Review: {datetime.now().strftime('%B %d, %Y')}",
            self.styles['ReportDate'] # Use the new date style
        )
        elements.append(subtitle)
        
        elements.append(Spacer(1, 1.5*inch))
        
        # Add decorative line spanning the full width
        drawing = Drawing(DRAWING_WIDTH, 5)
        drawing.add(Line(0, 2, DRAWING_WIDTH, 2, strokeColor=self.colors['primary'], strokeWidth=3))
        elements.append(drawing)
        
        elements.append(Spacer(1, 0.5*inch))
        
        # Add a placeholder image/logo (optional but visually appealing)
        # elements.append(Image("path/to/logo.png", width=1*inch, height=1*inch))
        
        return elements

    def _create_executive_summary(self, insights: Dict[str, Any]) -> List:
        """Create executive summary with key metrics - **ALIGNMENT FIX**"""
        elements = []
        
        elements.append(Paragraph("Executive Summary", self.styles['SectionHeader']))
        elements.append(Spacer(1, 0.2*inch))
        
        summary_data = []
        
        # ... (Data extraction logic remains the same) ...
        if 'dataset_info' in insights:
            info = insights['dataset_info']
            summary_data.append(['Total Records', f"{info.get('total_records', 0):,}"])
            summary_data.append(['Data Completeness', f"{info.get('data_completeness', 0)}%"])
        
        if 'order_overview' in insights:
            order = insights['order_overview']
            summary_data.append(['Total Orders', f"{order.get('total_orders', 0):,}"])
            summary_data.append(['Total Quantity', f"{order.get('total_quantity_ordered', 0):,.0f}"])
        
        if 'fulfillment_metrics' in insights:
            fulfillment = insights['fulfillment_metrics']
            summary_data.append(['Fulfillment Rate', f"{fulfillment.get('fulfillment_rate_percent', 0):.2f}%"]) # Add precision
        
        if 'cost_overview' in insights:
            cost = insights['cost_overview']
            summary_data.append(['Total Operational Costs', f"${cost.get('total_operational_costs', 0):,.2f}"])
        
        # **ALIGNMENT FIX**: Set colWidths to span full page width, aligned in 2 columns
        if summary_data:
            num_rows = len(summary_data)
            # Reshape into a 2x(num_rows/2) grid for a balanced look
            
            # Pad if odd number of elements to maintain 2-column structure
            if num_rows % 2 != 0:
                summary_data.append(['', ''])
            
            summary_grid = []
            for i in range(0, len(summary_data), 2):
                summary_grid.append(summary_data[i] + summary_data[i+1])
                
            # Define column widths for a 4-column layout
            col_widths = [FIXED_COL_WIDTH, FIXED_COL_WIDTH, FIXED_COL_WIDTH, FIXED_COL_WIDTH]
            summary_table = Table(summary_grid, colWidths=col_widths)
            
            # **VISUAL ENHANCEMENT**: Better style for the summary dashboard look
            summary_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, -1), colors.white),
                ('TEXTCOLOR', (0, 0), (-1, -1), self.colors['dark_text']),
                ('ALIGN', (0, 0), (0, -1), 'LEFT'), # Label 1 left
                ('ALIGN', (1, 0), (1, -1), 'RIGHT'), # Value 1 right
                ('ALIGN', (2, 0), (2, -1), 'LEFT'), # Label 2 left
                ('ALIGN', (3, 0), (3, -1), 'RIGHT'), # Value 2 right
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('FONTNAME', (1, 0), (1, -1), 'Helvetica-Bold'),
                ('FONTNAME', (3, 0), (3, -1), 'Helvetica-Bold'),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
                ('TOPPADDING', (0, 0), (-1, -1), 10),
                # Use internal grid for visual separation instead of full box
                ('LINEBEFORE', (2, 0), (2, -1), 1, self.colors['light_bg']),
                ('LINEABOVE', (0, 0), (-1, -1), 0.5, self.colors['light_bg']),
                ('LINEBELOW', (0, -1), (-1, -1), 0.5, self.colors['light_bg']),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ]))
            elements.append(summary_table)
        
        return elements
    
    def _create_order_fulfillment_section(self, insights: Dict[str, Any]) -> List:
        """Create order fulfillment analysis section - ALIGNMENT FIX"""
        elements = []
        
        elements.append(Paragraph("Order Fulfillment Analysis", self.styles['SectionHeader']))
        elements.append(Spacer(1, 0.2*inch))
        
        if 'order_overview' in insights:
            elements.append(Paragraph("Order Metrics Overview", self.styles['SubHeader']))
            overview = insights['order_overview']
            
            data = [
                ['Metric', 'Value'],
                ['Total Orders', f"{overview.get('total_orders', 0):,}"],
                ['Total Quantity', f"{overview.get('total_quantity_ordered', 0):,.0f}"],
                ['Average Order Quantity', f"{overview.get('average_order_quantity', 0):,.2f}"],
                ['Median Order Quantity', f"{overview.get('median_order_quantity', 0):,.2f}"],
                ['Largest Order', f"{overview.get('largest_order', 0):,.0f}"],
                ['Smallest Order', f"{overview.get('smallest_order', 0):,.0f}"],
            ]
            
            col_widths=[TWO_COL_WIDTH * 0.6, TWO_COL_WIDTH * 0.4]
            table = self._create_styled_table(data, col_widths=col_widths, align_values_right=True)
            elements.append(table)
            elements.append(Spacer(1, 0.3*inch))
        
        # Order Status Breakdown Chart and Priority Analysis Table side-by-side
        chart_and_table_contents = [] # List to hold the contents of the two cells
        
        # Order Status Breakdown Chart (on left)
        chart_elements = []
        if 'order_status_breakdown' in insights:
            chart_elements.append(Paragraph("Order Status Distribution", self.styles['SubHeader']))
            status_chart = self._create_pie_chart(
                insights['order_status_breakdown'],
                'status', 'order_count',
                "Order Status Distribution"
            )
            chart_elements.append(status_chart)
            # --- FIX: Append the list of elements directly, NOT wrapped in KeepTogether ---
            chart_and_table_contents.append(chart_elements)
        
        # Priority Analysis Table (on right)
        table_elements = []
        if 'priority_analysis' in insights:
            table_elements.append(Paragraph("Order Priority Analysis", self.styles['SubHeader']))
            
            priority_data = [['Priority', 'Total Quantity', 'Order Count', 'Avg Qty/Order']]
            for item in insights['priority_analysis']:
                priority_data.append([
                    item['priority'],
                    f"{item['total_quantity']:,.0f}",
                    f"{item['order_count']:,}",
                    f"{item['avg_quantity_per_order']:,.2f}"
                ])
            
            priority_col_widths = [TWO_COL_WIDTH / 4.0] * 4
            table = self._create_styled_table(priority_data, col_widths=priority_col_widths, align_values_right=True)
            table_elements.append(table)
            # --- FIX: Append the list of elements directly, NOT wrapped in KeepTogether ---
            chart_and_table_contents.append(table_elements)
            
        if chart_and_table_contents:
            # Pad if only one element exists to ensure the Table structure is maintained
            while len(chart_and_table_contents) < 2:
                chart_and_table_contents.append([]) 
                
            # Put the two lists of flowables into a single-row Table
            side_by_side_table = Table([chart_and_table_contents], colWidths=[TWO_COL_WIDTH, TWO_COL_WIDTH])
            side_by_side_table.setStyle(TableStyle([
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('LEFTPADDING', (1, 0), (1, 0), 15),
            ]))
            elements.append(side_by_side_table)
        
        return elements
        
    # --- Inventory Section (Table Width Fix) ---
    def _create_inventory_section(self, insights: Dict[str, Any]) -> List:
        """Create inventory management section"""
        elements = []
        
        elements.append(Paragraph("Inventory Management", self.styles['SectionHeader']))
        elements.append(Spacer(1, 0.2*inch))
        
        # Inventory Overview
        if 'inventory_overview' in insights:
            elements.append(Paragraph("Inventory Metrics Overview", self.styles['SubHeader']))
            overview = insights['inventory_overview']
            
            data = [
                ['Metric', 'Value'],
                ['Total Inventory Units', f"{overview.get('total_inventory_units', 0):,.0f}"],
                ['Average Inventory/Item', f"{overview.get('average_inventory_per_item', 0):,.2f}"],
                ['Median Inventory', f"{overview.get('median_inventory', 0):,.0f}"],
                ['Total Items', f"{overview.get('inventory_items', 0):,}"],
                ['Zero Inventory Items', f"{overview.get('zero_inventory_items', 0):,}"],
                ['Low Inventory Items', f"{overview.get('low_inventory_items', 0):,}"],
            ]
            
            # **ALIGNMENT FIX**: Set colWidths for a metrics table
            col_widths = [TWO_COL_WIDTH, TWO_COL_WIDTH]
            table = self._create_styled_table(data, col_widths=col_widths, align_values_right=True)
            elements.append(table)
            elements.append(Spacer(1, 0.3*inch))
        
        # Inventory Distribution Chart
        if 'inventory_distribution' in insights:
            elements.append(Paragraph("Inventory Level Distribution", self.styles['SubHeader']))
            
            # Chart size will be fixed in the chart helper
            chart = self._create_bar_chart(
                insights['inventory_distribution'],
                'level', 'item_count',
                "Inventory Distribution"
            )
            
            # **ALIGNMENT FIX**: Center the chart
            chart_container = Table([[chart]], colWidths=[DRAWING_WIDTH], style=[('ALIGN', (0,0), (-1,-1), 'CENTER')])
            elements.append(chart_container)
            elements.append(Spacer(1, 0.3*inch))
        
        # Low Stock Alerts
        if 'product_inventory_alerts' in insights:
            elements.append(Paragraph("Low Stock Alerts (Top 10)", self.styles['SubHeader']))
            
            alert_data = [['Product', 'Total Inventory', 'Avg Inventory']]
            for item in insights['product_inventory_alerts'].get('lowest_stock_products', [])[:10]:
                alert_data.append([
                    item['product'][:40],
                    f"{item['total_inventory']:,.0f}",
                    f"{item['avg_inventory']:,.2f}"
                ])
            
            # **ALIGNMENT FIX**: Set colWidths for full width
            alert_col_widths = [DRAWING_WIDTH * 0.5, DRAWING_WIDTH * 0.25, DRAWING_WIDTH * 0.25]
            table = self._create_styled_table(alert_data, col_widths=alert_col_widths, highlight_warning=True, align_values_right=True)
            elements.append(table)
        
        return elements
        
    # --- Other Sections (Apply Table Width Fixes) ---

    # Apply full-width fixes to other sections (same logic as above)
    def _create_supply_chain_section(self, insights: Dict[str, Any]) -> List:
        elements = []
        elements.append(Paragraph("Supply Chain Performance", self.styles['SectionHeader']))
        elements.append(Spacer(1, 0.2*inch))
        
        if 'lead_time_metrics' in insights:
            elements.append(Paragraph("Lead Time Analysis", self.styles['SubHeader']))
            metrics = insights['lead_time_metrics']
            data = [
                ['Metric', 'Value'],
                ['Average Lead Time', f"{metrics.get('avg_lead_time', 0):.2f} days"],
                ['Median Lead Time', f"{metrics.get('median_lead_time', 0):.2f} days"],
                ['Minimum Lead Time', f"{metrics.get('min_lead_time', 0):.2f} days"],
                ['Maximum Lead Time', f"{metrics.get('max_lead_time', 0):.2f} days"],
                ['Consistency Score', f"{metrics.get('lead_time_consistency_score', 0):.2f}%"],
            ]
            col_widths = [TWO_COL_WIDTH, TWO_COL_WIDTH]
            table = self._create_styled_table(data, col_widths=col_widths, align_values_right=True)
            elements.append(table)
            elements.append(Spacer(1, 0.3*inch))
        
        if 'supplier_performance' in insights:
            elements.append(Paragraph("Supplier Performance (Top 10)", self.styles['SubHeader']))
            supplier_data = [['Supplier', 'Total Quantity', 'Orders', 'Avg Lead Time']]
            for supplier in insights['supplier_performance'][:10]:
                row = [supplier['supplier'][:30]]
                row.append(f"{supplier.get('total_quantity', 0):,.0f}")
                row.append(f"{supplier.get('order_count', 0):,}")
                row.append(f"{supplier.get('avg_lead_time', 0):.1f}")
                supplier_data.append(row)
            
            supplier_col_widths = [DRAWING_WIDTH * 0.4, DRAWING_WIDTH * 0.2, DRAWING_WIDTH * 0.2, DRAWING_WIDTH * 0.2]
            table = self._create_styled_table(supplier_data, col_widths=supplier_col_widths, align_values_right=True)
            elements.append(table)
        
        return elements

    def _create_quality_section(self, insights: Dict[str, Any]) -> List:
        elements = []
        elements.append(Paragraph("Quality Metrics", self.styles['SectionHeader']))
        elements.append(Spacer(1, 0.2*inch))
        
        quality = insights.get('quality_metrics', {})
        
        # Defect Analysis
        if 'defect_analysis' in quality:
            elements.append(Paragraph("Defect Analysis", self.styles['SubHeader']))
            defects = quality['defect_analysis']
            data = [
                ['Metric', 'Value'],
                ['Average Defect Rate', f"{defects.get('avg_defect_rate', 0):.2f}%"],
                ['Median Defect Rate', f"{defects.get('median_defect_rate', 0):.2f}%"],
                ['Total Defects', f"{defects.get('total_defects', 0):,.0f}"],
                ['Zero Defect Items', f"{defects.get('zero_defect_items', 0):,}"],
            ]
            col_widths = [TWO_COL_WIDTH, TWO_COL_WIDTH]
            table = self._create_styled_table(data, col_widths=col_widths, align_values_right=True)
            elements.append(table)
            elements.append(Spacer(1, 0.3*inch))
        
        # Quality Score Analysis
        if 'quality_score_analysis' in quality:
            elements.append(Paragraph("Quality Score Analysis", self.styles['SubHeader']))
            scores = quality['quality_score_analysis']
            data = [
                ['Metric', 'Value'],
                ['Average Quality Score', f"{scores.get('avg_quality_score', 0):.2f}"],
                ['Median Quality Score', f"{scores.get('median_quality_score', 0):.2f}"],
                ['High Quality Items', f"{scores.get('high_quality_items', 0):,}"],
                ['Low Quality Items', f"{scores.get('low_quality_items', 0):,}"],
            ]
            col_widths = [TWO_COL_WIDTH, TWO_COL_WIDTH]
            table = self._create_styled_table(data, col_widths=col_widths, align_values_right=True)
            elements.append(table)
        
        return elements
        
    def _create_production_section(self, insights: Dict[str, Any]) -> List:
        elements = []
        elements.append(Paragraph("Production Efficiency", self.styles['SectionHeader']))
        elements.append(Spacer(1, 0.2*inch))
        
        production = insights.get('production_efficiency', {})
        
        metrics_list = [] # List to hold the flowables for the left column
        if 'productivity' in production:
            prod = production['productivity']
            metrics_list.extend([
                Paragraph("Productivity Metrics", self.styles['SubHeader']),
                self._create_styled_table(
                    [['Metric', 'Value'],
                     ['Average Productivity', f"{prod.get('avg_productivity', 0):,.2f}"],
                     ['Median Productivity', f"{prod.get('median_productivity', 0):,.2f}"],
                     ['Maximum Productivity', f"{prod.get('max_productivity', 0):,.2f}"],
                     ['Minimum Productivity', f"{prod.get('min_productivity', 0):,.2f}"]],
                    col_widths=[TWO_COL_WIDTH * 0.6, TWO_COL_WIDTH * 0.4], align_values_right=True),
                Spacer(1, 0.15*inch)
            ])
        
        util_list = [] # List to hold the flowables for the right column
        if 'utilization' in production:
            util = production['utilization']
            util_list.extend([
                Paragraph("Utilization Analysis", self.styles['SubHeader']),
                self._create_styled_table(
                    [['Metric', 'Value'],
                     ['Average Utilization', f"{util.get('avg_utilization_percent', 0):.2f}%"],
                     ['High Utilization Periods', f"{util.get('high_utilization_periods', 0):,}"],
                     ['Optimal Utilization Periods', f"{util.get('optimal_utilization_periods', 0):,}"],
                     ['Low Utilization Periods', f"{util.get('low_utilization_periods', 0):,}"]],
                    col_widths=[TWO_COL_WIDTH * 0.6, TWO_COL_WIDTH * 0.4], align_values_right=True)
            ])
        
        if metrics_list or util_list:
            
            # --- FIX: Create the single-row layout Table with the lists of flowables directly ---
            if metrics_list and util_list:
                side_by_side_table = Table([[metrics_list, util_list]], colWidths=[TWO_COL_WIDTH, TWO_COL_WIDTH])
                side_by_side_table.setStyle(TableStyle([
                    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                    ('LEFTPADDING', (1, 0), (1, 0), 15),
                ]))
                elements.append(side_by_side_table)
            elif metrics_list:
                 elements.extend(metrics_list)
            elif util_list:
                 elements.extend(util_list)

        return elements

    def _create_delivery_section(self, insights: Dict[str, Any]) -> List:
        elements = []
        elements.append(Paragraph("Delivery Performance", self.styles['SectionHeader']))
        elements.append(Spacer(1, 0.2*inch))
        
        delivery = insights.get('delivery_performance', {})
        
        # On-Time Delivery
        otd_list = []
        if 'on_time_delivery' in delivery:
            otd_data = delivery['on_time_delivery']
            otd_list.extend([
                Paragraph("On-Time Delivery", self.styles['SubHeader']),
                self._create_styled_table(
                    [['Metric', 'Value'],
                     ['On-Time Delivery Rate', f"{otd_data.get('on_time_delivery_rate_percent', 0):.2f}%"],
                     ['Total Deliveries', f"{otd_data.get('total_deliveries', 0):,}"],
                     ['On-Time Deliveries', f"{otd_data.get('on_time_deliveries', 0):,}"]],
                    col_widths=[TWO_COL_WIDTH * 0.6, TWO_COL_WIDTH * 0.4], align_values_right=True)
            ])

        # Delivery Time Analysis
        time_list = []
        if 'delivery_time_analysis' in delivery:
            time_analysis = delivery['delivery_time_analysis']
            time_list.extend([
                Paragraph("Delivery Time Analysis", self.styles['SubHeader']),
                self._create_styled_table(
                    [['Metric', 'Value'],
                     ['Average Delivery Time', f"{time_analysis.get('avg_delivery_time_days', 0):.2f} days"],
                     ['Median Delivery Time', f"{time_analysis.get('median_delivery_time_days', 0):.2f} days"],
                     ['Fastest Delivery', f"{time_analysis.get('fastest_delivery_days', 0):.2f} days"],
                     ['Slowest Delivery', f"{time_analysis.get('slowest_delivery_days', 0):.2f} days"]],
                    col_widths=[TWO_COL_WIDTH * 0.6, TWO_COL_WIDTH * 0.4], align_values_right=True)
            ])

        # FIX: Place metric tables side-by-side using the flowable lists
        if otd_list and time_list:
            side_by_side_table = Table([[otd_list, time_list]], colWidths=[TWO_COL_WIDTH, TWO_COL_WIDTH])
            side_by_side_table.setStyle(TableStyle([
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('LEFTPADDING', (1, 0), (1, 0), 15),
            ]))
            elements.append(side_by_side_table)
        elif otd_list:
            elements.extend(otd_list)
        elif time_list:
            elements.extend(time_list)
            
        return elements

    def _create_regional_section(self, insights: Dict[str, Any]) -> List:
        elements = []
        
        elements.append(Paragraph("Regional Operations", self.styles['SectionHeader']))
        elements.append(Spacer(1, 0.2*inch))
        
        regional = insights.get('regional_operations', {})
        
        # Volume by Region
        if 'volume_by_region' in regional:
            elements.append(Paragraph("Volume Distribution by Region (Top 10)", self.styles['SubHeader']))
            
            region_data = [['Region', 'Total Quantity', '% of Total', 'Orders']]
            for region in regional['volume_by_region'][:10]:
                region_data.append([
                    region['region'][:25],
                    f"{region['total_quantity']:,.0f}",
                    f"{region['percentage_of_total']:.1f}%",
                    f"{region['order_count']:,}"
                ])
            
            # **ALIGNMENT FIX**: Set colWidths for full width
            region_col_widths = [DRAWING_WIDTH * 0.4, DRAWING_WIDTH * 0.2, DRAWING_WIDTH * 0.2, DRAWING_WIDTH * 0.2]
            table = self._create_styled_table(region_data, col_widths=region_col_widths, align_values_right=True)
            elements.append(table)
            elements.append(Spacer(1, 0.3*inch))
            
            # Regional Chart
            chart = self._create_horizontal_bar_chart(
                regional['volume_by_region'][:10],
                'region', 'total_quantity',
                "Quantity by Region"
            )
            # **ALIGNMENT FIX**: Center the chart
            chart_container = Table([[chart]], colWidths=[DRAWING_WIDTH], style=[('ALIGN', (0,0), (-1,-1), 'CENTER')])
            elements.append(chart_container)
        
        return elements

    def _create_cost_section(self, insights: Dict[str, Any]) -> List:
        elements = []
        elements.append(Paragraph("Operational Cost Analysis", self.styles['SectionHeader']))
        elements.append(Spacer(1, 0.2*inch))
        
        # Cost Overview
        if 'cost_overview' in insights:
            elements.append(Paragraph("Cost Metrics Overview", self.styles['SubHeader']))
            overview = insights['cost_overview']
            
            data = [
                ['Metric', 'Value'],
                ['Total Operational Costs', f"${overview.get('total_operational_costs', 0):,.2f}"],
                ['Average Cost', f"${overview.get('average_cost', 0):,.2f}"],
                ['Median Cost', f"${overview.get('median_cost', 0):,.2f}"],
                ['Highest Cost', f"${overview.get('highest_cost', 0):,.2f}"],
                ['Lowest Cost', f"${overview.get('lowest_cost', 0):,.2f}"],
            ]
            
            col_widths = [TWO_COL_WIDTH, TWO_COL_WIDTH]
            table = self._create_styled_table(data, col_widths=col_widths, align_values_right=True)
            elements.append(table)
            elements.append(Spacer(1, 0.3*inch))
        
        # Cost by Product
        if 'cost_by_product' in insights:
            elements.append(Paragraph("Top 10 Cost Drivers by Product", self.styles['SubHeader']))
            
            product_data = [['Product', 'Total Cost', 'Transactions', 'Avg Cost']]
            for product in insights['cost_by_product'][:10]:
                product_data.append([
                    product['product'][:35],
                    f"${product['total_cost']:,.2f}",
                    f"{product['transaction_count']:,}",
                    f"${product['avg_cost_per_transaction']:,.2f}"
                ])
            
            # **ALIGNMENT FIX**: Set colWidths for full width
            product_col_widths = [DRAWING_WIDTH * 0.4, DRAWING_WIDTH * 0.2, DRAWING_WIDTH * 0.2, DRAWING_WIDTH * 0.2]
            table = self._create_styled_table(product_data, col_widths=product_col_widths, align_values_right=True)
            elements.append(table)
        
        return elements

    def _create_trends_section(self, insights: Dict[str, Any]) -> List:
        elements = []
        
        elements.append(Paragraph("Operational Trends", self.styles['SectionHeader']))
        elements.append(Spacer(1, 0.2*inch))
        
        # Monthly Trends Chart
        if 'monthly_operational_trends' in insights:
            elements.append(Paragraph("Monthly Volume Trends", self.styles['SubHeader']))
            
            # Chart size will be fixed in the chart helper
            trends_chart = self._create_line_chart(
                insights['monthly_operational_trends'],
                'month', 'total_quantity',
                "Monthly Quantity Trends"
            )
            # **ALIGNMENT FIX**: Center the chart
            chart_container = Table([[trends_chart]], colWidths=[DRAWING_WIDTH], style=[('ALIGN', (0,0), (-1,-1), 'CENTER')])
            elements.append(chart_container)
            elements.append(Spacer(1, 0.3*inch))
        
        # Seasonal Trends
        if 'seasonal_trends' in insights:
            elements.append(Paragraph("Seasonal Analysis", self.styles['SubHeader']))
            
            seasonal_data = [['Season', 'Total Quantity', 'Order Count']]
            for season in insights['seasonal_trends']:
                seasonal_data.append([
                    season['season'],
                    f"{season['total_quantity']:,.0f}",
                    f"{season['order_count']:,}"
                ])
            
            # **ALIGNMENT FIX**: Set colWidths for full width
            seasonal_col_widths = [DRAWING_WIDTH * 0.4, DRAWING_WIDTH * 0.3, DRAWING_WIDTH * 0.3]
            table = self._create_styled_table(seasonal_data, col_widths=seasonal_col_widths, align_values_right=True)
            elements.append(table)
        
        return elements
        
    # --- Table and Chart Utilities (Core Alignment and Visual Fixes) ---
    
    def _create_styled_table(self, data: List[List], col_widths: List[Any] = None, highlight_warning: bool = False, align_values_right: bool = False) -> Table:
        """
        Create a beautifully styled table.
        
        **ALIGNMENT FIX**: Takes optional col_widths for full control.
        **VISUAL FIX**: Added `align_values_right` for number columns.
        """
        if col_widths is None:
            # Default to auto-size across the full drawing width
            table = Table(data, colWidths=[DRAWING_WIDTH / len(data[0])] * len(data[0]))
        else:
            table = Table(data, colWidths=col_widths)
            
        style_commands = [
            ('BACKGROUND', (0, 0), (-1, 0), self.colors['primary']), # Header background
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke), # Header text color
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'), # Default to LEFT alignment
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('TEXTCOLOR', (0, 1), (-1, -1), self.colors['dark_text']),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 10), # Slightly larger body font
            
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, self.colors['light_bg']]), # Zebra stripes
            ('LINEBELOW', (0, 0), (-1, -1), 0.5, colors.lightgrey), # Lighter grid lines
            ('LINEABOVE', (0, 0), (-1, 0), 0.5, colors.lightgrey),
            
            ('TOPPADDING', (0, 1), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
        ]
        
        if align_values_right and len(data) > 0:
            # Align all columns after the first (header) to the right for numbers
            for col_index in range(1, len(data[0])):
                style_commands.append(('ALIGN', (col_index, 0), (col_index, -1), 'RIGHT'))
            
        if highlight_warning and len(data) > 1:
            # Highlight first column (e.g., product name) in danger color
            style_commands.append(('TEXTCOLOR', (0, 1), (0, -1), self.colors['danger']))
            style_commands.append(('FONTNAME', (0, 1), (0, -1), 'Helvetica-Bold'))
        
        table.setStyle(TableStyle(style_commands))
        
        return table

    # **CHART FIXES**: Set Drawing size to span the page and center elements
    def _create_pie_chart(self, data: List[Dict], label_key: str, value_key: str, title: str) -> Drawing:
        """Create a pie chart - **ALIGNMENT FIX** on Drawing size and position"""
        # Drawing width is now half the page width to accommodate side-by-side placement
        drawing = Drawing(TWO_COL_WIDTH, 250)
        
        pie = Pie()
        pie.x = TWO_COL_WIDTH / 2 - 75 # Center the chart in its half-page box (150 width)
        pie.y = 50
        pie.width = 150
        pie.height = 150
        
        # ... (Slicing and colors remain the same) ...
        pie.data = [item[value_key] for item in data[:6]]
        pie.labels = [item[label_key][:15] for item in data[:6]]
        
        # Add a legend outside the pie to avoid clutter
        pie.sideLabels = 1
        pie.sideLabelsOffset = 1
        pie.slices.fontName = 'Helvetica'
        pie.slices.fontSize = 8
        
        # Set slice colors
        color_list = [self.colors['primary'], self.colors['secondary'], self.colors['info'], 
                      self.colors['success'], self.colors['warning'], self.colors['danger']]
        for i, color in enumerate(color_list):
             if i < len(pie.slices):
                pie.slices[i].fillColor = color
        
        drawing.add(pie)
        
        return drawing
    
    def _create_bar_chart(self, data: List[Dict], label_key: str, value_key: str, title: str) -> Drawing:
        """Create a vertical bar chart - **ALIGNMENT FIX** on Drawing size and position"""
        # Drawing width is now the full page width
        drawing = Drawing(DRAWING_WIDTH, 250)
        
        chart = VerticalBarChart()
        chart.x = 50
        chart.y = 50
        chart.height = 175 # Increased height
        chart.width = DRAWING_WIDTH - 100 # Span full width minus margins
        
        # ... (Data setup remains the same) ...
        chart.data = [[item[value_key] for item in data[:8]]]
        chart.categoryAxis.categoryNames = [item[label_key][:12] for item in data[:8]]
        
        # **VISUAL FIX**: Improve axis and label presentation
        chart.categoryAxis.labels.angle = 30 # Less harsh angle
        chart.categoryAxis.labels.fontSize = 9
        chart.valueAxis.labels.fontName = 'Helvetica'
        chart.valueAxis.labels.fontSize = 9
        chart.bars[0].fillColor = self.colors['primary']
        
        drawing.add(chart)
        
        return drawing
    
    def _create_horizontal_bar_chart(self, data: List[Dict], label_key: str, value_key: str, title: str) -> Drawing:
        """Create a horizontal bar chart - **ALIGNMENT FIX** on Drawing size and position"""
        # Drawing width is now the full page width
        drawing = Drawing(DRAWING_WIDTH, 300) # Increased height to fit 10 labels well
        
        chart = HorizontalBarChart()
        chart.x = 100 # Give more space for the category names
        chart.y = 30
        chart.height = 250 # Span vertically
        chart.width = DRAWING_WIDTH - 150 # Span width
        
        # ... (Data setup remains the same) ...
        chart.data = [[item[value_key] for item in data[:10]]]
        chart.categoryAxis.categoryNames = [item[label_key][:25] for item in data[:10]] # Allow longer labels
        
        # **VISUAL FIX**: Improve axis and label presentation
        chart.categoryAxis.labels.fontSize = 9
        chart.categoryAxis.labels.fontName = 'Helvetica'
        chart.valueAxis.labels.fontName = 'Helvetica'
        chart.valueAxis.labels.fontSize = 9
        chart.bars[0].fillColor = self.colors['info']
        
        drawing.add(chart)
        
        return drawing
    
    def _create_line_chart(self, data: List[Dict], label_key: str, value_key: str, title: str) -> Drawing:
        """Create a line chart for trends - **ALIGNMENT FIX** on Drawing size and position"""
        # Drawing width is now the full page width
        drawing = Drawing(DRAWING_WIDTH, 250)
        
        chart = HorizontalLineChart()
        chart.x = 50
        chart.y = 50
        chart.height = 175 # Increased height
        chart.width = DRAWING_WIDTH - 100 # Span full width
        
        # ... (Data setup remains the same) ...
        chart.data = [[item[value_key] for item in data[:12]]]
        chart.categoryAxis.categoryNames = [str(item[label_key])[-7:] for item in data[:12]]
        
        # **VISUAL FIX**: Improve axis and label presentation
        chart.categoryAxis.labels.angle = 30
        chart.categoryAxis.labels.fontSize = 8
        chart.valueAxis.labels.fontName = 'Helvetica'
        chart.valueAxis.labels.fontSize = 9
        chart.lines[0].strokeColor = self.colors['primary']
        chart.lines[0].strokeWidth = 2
        
        drawing.add(chart)
        
        return drawing


# Flask/FastAPI endpoint example (kept for context, no changes needed)
def export_operations_to_pdf(insights: Dict[str, Any], company_name: str = "Company") -> bytes:
    """
    Main function to export operations insights to PDF
    
    Args:
        insights: Dictionary containing operations insights from OperationsAnalysisService
        company_name: Optional company name for the report
    
    Returns:
        PDF file as bytes
    """
    exporter = OperationsPDFExporter()
    pdf_bytes = exporter.generate_pdf(insights)
    return pdf_bytes


# Example usage with file output (kept for context, no changes needed)
def save_operations_pdf(insights: Dict[str, Any], output_path: str):
    """
    Save operations insights to a PDF file
    
    Args:
        insights: Dictionary containing operations insights
        output_path: Path where PDF should be saved
    """
    exporter = OperationsPDFExporter()
    exporter.generate_pdf(insights, output_path=output_path)