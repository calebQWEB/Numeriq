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


class FinancePDFExporter:
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
        """Generate comprehensive finance PDF report"""
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
        
        # Transaction Summary
        if 'transaction_summary' in insights:
            story.extend(self._create_transaction_section(insights))
            story.append(PageBreak())
        
        # Revenue Analysis
        if 'revenue_overview' in insights:
            story.extend(self._create_revenue_section(insights))
            story.append(PageBreak())
        
        # Expense Analysis
        if 'expense_overview' in insights:
            story.extend(self._create_expense_section(insights))
            story.append(PageBreak())
        
        # Profitability Analysis
        if 'profitability_overview' in insights:
            story.extend(self._create_profitability_section(insights))
            story.append(PageBreak())
        
        # Cash Flow Analysis
        if 'cashflow_overview' in insights:
            story.extend(self._create_cashflow_section(insights))
            story.append(PageBreak())
        
        # Budget Variance Analysis
        if 'budget_performance' in insights:
            story.extend(self._create_budget_section(insights))
            story.append(PageBreak())
        
        # Account Performance
        if 'account_performance' in insights:
            story.extend(self._create_account_section(insights))
            story.append(PageBreak())
        
        # Department/Segment Financials
        if 'department_financials' in insights or 'segment_financials' in insights:
            story.extend(self._create_department_section(insights))
            story.append(PageBreak())
        
        # Vendor/Customer Analysis
        if 'vendor_metrics' in insights or 'customer_metrics' in insights:
            story.extend(self._create_vendor_customer_section(insights))
            story.append(PageBreak())
        
        # Financial Trends
        if 'monthly_financial_trends' in insights:
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
        
        title = Paragraph("FINANCIAL ANALYSIS REPORT", self.styles['CustomTitle'])
        elements.append(title)
        elements.append(Spacer(1, 0.5*inch))
        
        subtitle = Paragraph(
            f"Comprehensive Financial Review: {datetime.now().strftime('%B %d, %Y')}",
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
        
        if 'transaction_summary' in insights:
            trans = insights['transaction_summary']
            summary_data.append(['Total Transactions', f"{trans.get('total_transactions', 0):,}"])
            summary_data.append(['Total Amount', f"${trans.get('total_amount', 0):,.2f}"])
        
        if 'revenue_overview' in insights:
            rev = insights['revenue_overview']
            summary_data.append(['Total Revenue', f"${rev.get('total_revenue', 0):,.2f}"])
        
        if 'expense_overview' in insights:
            exp = insights['expense_overview']
            summary_data.append(['Total Expenses', f"${exp.get('total_expenses', 0):,.2f}"])
        
        if 'profitability_overview' in insights:
            profit = insights['profitability_overview']
            summary_data.append(['Total Profit', f"${profit.get('total_profit', 0):,.2f}"])
            if 'profit_margin' in profit:
                summary_data.append(['Profit Margin', f"{profit.get('profit_margin', 0):.1f}%"])
        
        if 'cashflow_overview' in insights:
            cf = insights['cashflow_overview']
            summary_data.append(['Net Cash Flow', f"${cf.get('net_cashflow', 0):,.2f}"])
        
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
    
    def _create_transaction_section(self, insights: Dict[str, Any]) -> List:
        """Create transaction summary section"""
        elements = []
        elements.append(Paragraph("Transaction Analysis", self.styles['SectionHeader']))
        elements.append(Spacer(1, 0.2*inch))
        
        trans = insights['transaction_summary']
        data = [
            ['Metric', 'Value'],
            ['Total Transactions', f"{trans.get('total_transactions', 0):,}"],
            ['Total Amount', f"${trans.get('total_amount', 0):,.2f}"],
            ['Average Transaction', f"${trans.get('average_transaction', 0):,.2f}"],
            ['Median Transaction', f"${trans.get('median_transaction', 0):,.2f}"],
            ['Largest Transaction', f"${trans.get('largest_transaction', 0):,.2f}"],
            ['Smallest Transaction', f"${trans.get('smallest_transaction', 0):,.2f}"],
            ['Positive Transactions', f"{trans.get('positive_transactions', 0):,}"],
            ['Negative Transactions', f"{trans.get('negative_transactions', 0):,}"]
        ]
        
        col_widths = [TWO_COL_WIDTH, TWO_COL_WIDTH]
        table = self._create_styled_table(data, col_widths=col_widths, align_values_right=True)
        elements.append(table)
        elements.append(Spacer(1, 0.3*inch))
        
        # Transactions by grouping (category, department, etc.)
        grouping_keys = ['category', 'department', 'account', 'vendor', 'customer']
        for group_key in grouping_keys:
            insight_key = f'transactions_by_{group_key}'
            if insight_key in insights:
                elements.append(Paragraph(f"Transactions by {group_key.title()}", self.styles['SubHeader']))
                group_data = [['Name', 'Total Amount', '% of Total', 'Count', 'Avg Amount']]
                for item in insights[insight_key][:15]:
                    group_data.append([
                        str(item[f'{group_key}_name'])[:30],
                        f"${item['total_amount']:,.2f}",
                        f"{item['percentage_of_total']:.1f}%",
                        f"{item['transaction_count']:,}",
                        f"${item['average_amount']:,.2f}"
                    ])
                
                col_widths = [DRAWING_WIDTH * 0.3, DRAWING_WIDTH * 0.2, DRAWING_WIDTH * 0.15, DRAWING_WIDTH * 0.15, DRAWING_WIDTH * 0.2]
                group_table = self._create_styled_table(group_data, col_widths=col_widths, align_values_right=True)
                elements.append(group_table)
                break  # Only show first available grouping
        
        return elements
    
    def _create_revenue_section(self, insights: Dict[str, Any]) -> List:
        """Create revenue analysis section"""
        elements = []
        elements.append(Paragraph("Revenue Analysis", self.styles['SectionHeader']))
        elements.append(Spacer(1, 0.2*inch))
        
        rev = insights['revenue_overview']
        data = [
            ['Metric', 'Value'],
            ['Total Revenue', f"${rev.get('total_revenue', 0):,.2f}"],
            ['Average Revenue', f"${rev.get('average_revenue', 0):,.2f}"],
            ['Median Revenue', f"${rev.get('median_revenue', 0):,.2f}"],
            ['Revenue Transactions', f"{rev.get('revenue_transactions', 0):,}"],
            ['Max Single Revenue', f"${rev.get('max_single_revenue', 0):,.2f}"],
            ['Min Single Revenue', f"${rev.get('min_single_revenue', 0):,.2f}"]
        ]
        
        col_widths = [TWO_COL_WIDTH, TWO_COL_WIDTH]
        table = self._create_styled_table(data, col_widths=col_widths, align_values_right=True)
        elements.append(table)
        elements.append(Spacer(1, 0.3*inch))
        
        # Revenue by category
        if 'revenue_by_category' in insights:
            left_content = [Paragraph("Revenue by Category", self.styles['SubHeader'])]
            chart = self._create_pie_chart(
                insights['revenue_by_category'][:6],
                'category', 'total_revenue',
                "Revenue Distribution"
            )
            left_content.append(chart)
            
            right_content = [Paragraph("Top Revenue Categories", self.styles['SubHeader'])]
            cat_data = [['Category', 'Revenue', '% of Total']]
            for item in insights['revenue_by_category'][:8]:
                cat_data.append([
                    item['category'][:25],
                    f"${item['total_revenue']:,.2f}",
                    f"{item['percentage_of_total']:.1f}%"
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
            elements.append(Spacer(1, 0.3*inch))
        
        # Monthly revenue trends
        if 'monthly_revenue_trends' in insights:
            elements.append(Paragraph("Monthly Revenue Trends", self.styles['SubHeader']))
            chart = self._create_line_chart(
                insights['monthly_revenue_trends'],
                'month', 'revenue',
                "Monthly Revenue"
            )
            chart_container = Table([[chart]], colWidths=[DRAWING_WIDTH])
            chart_container.setStyle(TableStyle([('ALIGN', (0,0), (-1,-1), 'CENTER')]))
            elements.append(chart_container)
        
        return elements
    
    def _create_expense_section(self, insights: Dict[str, Any]) -> List:
        """Create expense analysis section"""
        elements = []
        elements.append(Paragraph("Expense Analysis", self.styles['SectionHeader']))
        elements.append(Spacer(1, 0.2*inch))
        
        exp = insights['expense_overview']
        data = [
            ['Metric', 'Value'],
            ['Total Expenses', f"${exp.get('total_expenses', 0):,.2f}"],
            ['Average Expense', f"${exp.get('average_expense', 0):,.2f}"],
            ['Median Expense', f"${exp.get('median_expense', 0):,.2f}"],
            ['Expense Transactions', f"{exp.get('expense_transactions', 0):,}"],
            ['Largest Expense', f"${exp.get('largest_expense', 0):,.2f}"],
            ['Smallest Expense', f"${exp.get('smallest_expense', 0):,.2f}"]
        ]
        
        col_widths = [TWO_COL_WIDTH, TWO_COL_WIDTH]
        table = self._create_styled_table(data, col_widths=col_widths, align_values_right=True)
        elements.append(table)
        elements.append(Spacer(1, 0.3*inch))
        
        # Expense by category
        if 'expense_by_category' in insights:
            elements.append(Paragraph("Expense Breakdown by Category", self.styles['SubHeader']))
            cat_data = [['Category', 'Total Expense', '% of Total', 'Count', 'Avg Expense']]
            for item in insights['expense_by_category'][:15]:
                cat_data.append([
                    item['category'][:25],
                    f"${item['total_expense']:,.2f}",
                    f"{item['percentage_of_total']:.1f}%",
                    f"{item['transaction_count']:,}",
                    f"${item['average_expense']:,.2f}"
                ])
            
            col_widths = [DRAWING_WIDTH * 0.3, DRAWING_WIDTH * 0.2, DRAWING_WIDTH * 0.15, DRAWING_WIDTH * 0.15, DRAWING_WIDTH * 0.2]
            cat_table = self._create_styled_table(cat_data, col_widths=col_widths, align_values_right=True)
            elements.append(cat_table)
            elements.append(Spacer(1, 0.3*inch))
        
        # Top vendors by expense
        if 'top_expense_vendors' in insights:
            elements.append(Paragraph("Top 15 Expense Vendors", self.styles['SubHeader']))
            vendor_data = [['Vendor', 'Total Expense', 'Transactions']]
            for item in insights['top_expense_vendors']:
                vendor_data.append([
                    item['vendor'][:35],
                    f"${item['total_expense']:,.2f}",
                    f"{item['transaction_count']:,}"
                ])
            
            col_widths = [DRAWING_WIDTH * 0.5, DRAWING_WIDTH * 0.3, DRAWING_WIDTH * 0.2]
            vendor_table = self._create_styled_table(vendor_data, col_widths=col_widths, align_values_right=True)
            elements.append(vendor_table)
        
        return elements
    
    def _create_profitability_section(self, insights: Dict[str, Any]) -> List:
        """Create profitability analysis section"""
        elements = []
        elements.append(Paragraph("Profitability Analysis", self.styles['SectionHeader']))
        elements.append(Spacer(1, 0.2*inch))
        
        profit = insights['profitability_overview']
        
        data_rows = [['Metric', 'Value']]
        
        if 'total_revenue' in profit:
            data_rows.append(['Total Revenue', f"${profit['total_revenue']:,.2f}"])
        if 'total_expenses' in profit:
            data_rows.append(['Total Expenses', f"${profit['total_expenses']:,.2f}"])
        if 'total_profit' in profit:
            data_rows.append(['Total Profit', f"${profit['total_profit']:,.2f}"])
        if 'average_profit_margin' in profit:
            data_rows.append(['Avg Profit Margin', f"{profit['average_profit_margin']:.2f}%"])
        if 'profitable_periods' in profit:
            data_rows.append(['Profitable Periods', f"{profit.get('profitable_periods', 0):,}"])
        if 'loss_periods' in profit:
            data_rows.append(['Loss Periods', f"{profit.get('loss_periods', 0):,}"])
        
        col_widths = [TWO_COL_WIDTH, TWO_COL_WIDTH]
        table = self._create_styled_table(data_rows, col_widths=col_widths, align_values_right=True)
        elements.append(table)
        elements.append(Spacer(1, 0.3*inch))
        
        # Monthly profit trends
        if 'monthly_profit_trends' in insights:
            elements.append(Paragraph("Monthly Profit Trends", self.styles['SubHeader']))
            chart = self._create_line_chart(
                insights['monthly_profit_trends'],
                'month', 'profit',
                "Monthly Profit"
            )
            chart_container = Table([[chart]], colWidths=[DRAWING_WIDTH])
            chart_container.setStyle(TableStyle([('ALIGN', (0,0), (-1,-1), 'CENTER')]))
            elements.append(chart_container)
        
        return elements
    
    def _create_cashflow_section(self, insights: Dict[str, Any]) -> List:
        """Create cash flow analysis section"""
        elements = []
        elements.append(Paragraph("Cash Flow Analysis", self.styles['SectionHeader']))
        elements.append(Spacer(1, 0.2*inch))
        
        cf = insights['cashflow_overview']
        
        left_content = [Paragraph("Cash Flow Overview", self.styles['SubHeader'])]
        data = [
            ['Metric', 'Value'],
            ['Total Inflows', f"${cf.get('total_inflows', 0):,.2f}"],
            ['Total Outflows', f"${cf.get('total_outflows', 0):,.2f}"],
            ['Net Cash Flow', f"${cf.get('net_cashflow', 0):,.2f}"],
            ['Inflow Transactions', f"{cf.get('inflow_transactions', 0):,}"],
            ['Outflow Transactions', f"{cf.get('outflow_transactions', 0):,}"]
        ]
        col_widths = [TWO_COL_WIDTH * 0.6, TWO_COL_WIDTH * 0.4]
        cf_table = self._create_styled_table(data, col_widths=col_widths, align_values_right=True)
        left_content.append(cf_table)
        
        right_content = []
        if 'monthly_cashflow_trends' in insights and len(insights['monthly_cashflow_trends']) > 0:
            right_content.append(Paragraph("Cash Flow Trends", self.styles['SubHeader']))
            # Create mini chart for trends
            trend_data = insights['monthly_cashflow_trends'][-6:]  # Last 6 months
            trend_table_data = [['Month', 'Net Flow']]
            for item in trend_data:
                trend_table_data.append([
                    str(item['month'])[-7:],
                    f"${item['net_cashflow']:,.2f}"
                ])
            trend_col_widths = [TWO_COL_WIDTH * 0.5, TWO_COL_WIDTH * 0.5]
            trend_table = self._create_styled_table(trend_table_data, col_widths=trend_col_widths, align_values_right=True)
            right_content.append(trend_table)
        
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
    
    def _create_budget_section(self, insights: Dict[str, Any]) -> List:
        """Create budget variance section"""
        elements = []
        elements.append(Paragraph("Budget Performance Analysis", self.styles['SectionHeader']))
        elements.append(Spacer(1, 0.2*inch))
        
        budget = insights['budget_performance']
        data = [
            ['Metric', 'Value'],
            ['Total Budget', f"${budget.get('total_budget', 0):,.2f}"],
            ['Total Actual', f"${budget.get('total_actual', 0):,.2f}"],
            ['Total Variance', f"${budget.get('total_variance', 0):,.2f}"],
            ['Variance %', f"{budget.get('variance_percentage', 0):.1f}%"],
            ['Budget Utilization', f"{budget.get('budget_utilization_rate', 0):.1f}%"],
            ['Over Budget Items', f"{budget.get('over_budget_items', 0):,}"],
            ['Under Budget Items', f"{budget.get('under_budget_items', 0):,}"],
            ['On Budget Items', f"{budget.get('on_budget_items', 0):,}"]
        ]
        
        col_widths = [TWO_COL_WIDTH, TWO_COL_WIDTH]
        table = self._create_styled_table(data, col_widths=col_widths, align_values_right=True)
        elements.append(table)
        elements.append(Spacer(1, 0.3*inch))
        
        # Budget variance by category
        if 'budget_variance_by_category' in insights:
            elements.append(Paragraph("Budget Variance by Category", self.styles['SubHeader']))
            var_data = [['Category', 'Budget', 'Actual', 'Variance', 'Var %', 'Util %']]
            for item in insights['budget_variance_by_category'][:15]:
                var_data.append([
                    item['category'][:20],
                    f"${item['budgeted']:,.2f}",
                    f"${item['actual']:,.2f}",
                    f"${item['variance']:,.2f}",
                    f"{item['variance_percentage']:.1f}%",
                    f"{item['utilization_rate']:.1f}%"
                ])
            
            col_widths = [DRAWING_WIDTH * 0.25, DRAWING_WIDTH * 0.15, DRAWING_WIDTH * 0.15, DRAWING_WIDTH * 0.15, DRAWING_WIDTH * 0.15, DRAWING_WIDTH * 0.15]
            var_table = self._create_styled_table(var_data, col_widths=col_widths, align_values_right=True)
            elements.append(var_table)
        
        return elements
    
    def _create_account_section(self, insights: Dict[str, Any]) -> List:
        """Create account performance section"""
        elements = []
        elements.append(Paragraph("Account Performance", self.styles['SectionHeader']))
        elements.append(Spacer(1, 0.2*inch))
        
        elements.append(Paragraph("Top 15 Accounts by Volume", self.styles['SubHeader']))
        acc_data = [['Account', 'Total', '% of Total', 'Txns', 'Avg', 'Volatility']]
        for item in insights['account_performance'][:15]:
            acc_data.append([
                item['account'][:25],
                f"${item['total_amount']:,.2f}",
                f"{item['percentage_of_total']:.1f}%",
                f"{item['transaction_count']:,}",
                f"${item['average_transaction']:,.2f}",
                f"${item['amount_volatility']:,.2f}"
            ])
        
        col_widths = [DRAWING_WIDTH * 0.3, DRAWING_WIDTH * 0.15, DRAWING_WIDTH * 0.1, DRAWING_WIDTH * 0.1, DRAWING_WIDTH * 0.15, DRAWING_WIDTH * 0.2]
        acc_table = self._create_styled_table(acc_data, col_widths=col_widths, align_values_right=True)
        elements.append(acc_table)
        
        return elements
    
    def _create_department_section(self, insights: Dict[str, Any]) -> List:
        """Create department/segment financials section"""
        elements = []
        
        # Determine if we're working with departments or segments
        is_department = 'department_financials' in insights
        section_key = 'department_financials' if is_department else 'segment_financials'
        section_name = 'Department' if is_department else 'Segment'
        
        if section_key not in insights:
            return elements
        
        elements.append(Paragraph(f"{section_name} Financial Analysis", self.styles['SectionHeader']))
        elements.append(Spacer(1, 0.2*inch))
        
        elements.append(Paragraph(f"Financial Performance by {section_name}", self.styles['SubHeader']))
        dept_data = [['Name', 'Total', '% of Total', 'Txns', 'Avg', 'Volatility']]
        for item in insights[section_key][:15]:
            dept_key = 'department' if is_department else 'segment'
            dept_data.append([
                item[dept_key][:25],
                f"${item['total_amount']:,.2f}",
                f"{item['percentage_of_total']:.1f}%",
                f"{item['transaction_count']:,}",
                f"${item['average_transaction']:,.2f}",
                f"${item['amount_volatility']:,.2f}"
            ])
        
        col_widths = [DRAWING_WIDTH * 0.3, DRAWING_WIDTH * 0.15, DRAWING_WIDTH * 0.1, DRAWING_WIDTH * 0.1, DRAWING_WIDTH * 0.15, DRAWING_WIDTH * 0.2]
        dept_table = self._create_styled_table(dept_data, col_widths=col_widths, align_values_right=True)
        elements.append(dept_table)
        
        return elements
    
    def _create_vendor_customer_section(self, insights: Dict[str, Any]) -> List:
        """Create vendor and customer analysis section"""
        elements = []
        elements.append(Paragraph("Vendor & Customer Analysis", self.styles['SectionHeader']))
        elements.append(Spacer(1, 0.2*inch))
        
        # Vendor metrics
        if 'vendor_metrics' in insights:
            elements.append(Paragraph("Top 15 Vendors by Spend", self.styles['SubHeader']))
            vendor_data = [['Vendor', 'Total', '% of Total', 'Txns', 'Avg']]
            for item in insights['vendor_metrics'][:15]:
                vendor_data.append([
                    item['vendor'][:30],
                    f"${item['total_amount']:,.2f}",
                    f"{item['percentage_of_total']:.1f}%",
                    f"{item['transaction_count']:,}",
                    f"${item['average_transaction']:,.2f}"
                ])
            
            col_widths = [DRAWING_WIDTH * 0.35, DRAWING_WIDTH * 0.2, DRAWING_WIDTH * 0.15, DRAWING_WIDTH * 0.15, DRAWING_WIDTH * 0.15]
            vendor_table = self._create_styled_table(vendor_data, col_widths=col_widths, align_values_right=True)
            elements.append(vendor_table)
            elements.append(Spacer(1, 0.3*inch))
            
            # Vendor concentration
            if 'vendor_concentration' in insights:
                conc = insights['vendor_concentration']
                elements.append(Paragraph("Vendor Concentration Analysis", self.styles['SubHeader']))
                conc_data = [
                    ['Metric', 'Value'],
                    ['Top 5 Vendor %', f"{conc.get('top_5_vendor_percentage', 0):.1f}%"],
                    ['Vendor Diversity', f"{conc.get('vendor_diversity_index', 0):,}"],
                    ['Avg Vendor Transaction', f"${conc.get('average_vendor_transaction_value', 0):,.2f}"]
                ]
                col_widths = [TWO_COL_WIDTH, TWO_COL_WIDTH]
                conc_table = self._create_styled_table(conc_data, col_widths=col_widths, align_values_right=True)
                elements.append(conc_table)
                elements.append(Spacer(1, 0.3*inch))
        
        # Customer metrics
        if 'customer_metrics' in insights:
            elements.append(Paragraph("Top 15 Customers by Revenue", self.styles['SubHeader']))
            customer_data = [['Customer', 'Total', '% of Total', 'Txns', 'Avg']]
            for item in insights['customer_metrics'][:15]:
                customer_data.append([
                    item['customer'][:30],
                    f"${item['total_amount']:,.2f}",
                    f"{item['percentage_of_total']:.1f}%",
                    f"{item['transaction_count']:,}",
                    f"${item['average_transaction']:,.2f}"
                ])
            
            col_widths = [DRAWING_WIDTH * 0.35, DRAWING_WIDTH * 0.2, DRAWING_WIDTH * 0.15, DRAWING_WIDTH * 0.15, DRAWING_WIDTH * 0.15]
            customer_table = self._create_styled_table(customer_data, col_widths=col_widths, align_values_right=True)
            elements.append(customer_table)
            elements.append(Spacer(1, 0.3*inch))
            
            # Customer concentration
            if 'customer_concentration' in insights:
                conc = insights['customer_concentration']
                elements.append(Paragraph("Customer Concentration Analysis", self.styles['SubHeader']))
                conc_data = [
                    ['Metric', 'Value'],
                    ['Top 5 Customer %', f"{conc.get('top_5_customer_percentage', 0):.1f}%"],
                    ['Customer Diversity', f"{conc.get('customer_diversity_index', 0):,}"],
                    ['Avg Customer Transaction', f"${conc.get('average_customer_transaction_value', 0):,.2f}"]
                ]
                col_widths = [TWO_COL_WIDTH, TWO_COL_WIDTH]
                conc_table = self._create_styled_table(conc_data, col_widths=col_widths, align_values_right=True)
                elements.append(conc_table)
        
        return elements
    
    def _create_trends_section(self, insights: Dict[str, Any]) -> List:
        """Create financial trends section"""
        elements = []
        elements.append(Paragraph("Financial Trends Analysis", self.styles['SectionHeader']))
        elements.append(Spacer(1, 0.2*inch))
        
        # Monthly trends chart
        if 'monthly_financial_trends' in insights:
            elements.append(Paragraph("Monthly Financial Trends", self.styles['SubHeader']))
            chart = self._create_line_chart(
                insights['monthly_financial_trends'],
                'month', 'total_amount',
                "Monthly Trends"
            )
            chart_container = Table([[chart]], colWidths=[DRAWING_WIDTH])
            chart_container.setStyle(TableStyle([('ALIGN', (0,0), (-1,-1), 'CENTER')]))
            elements.append(chart_container)
            elements.append(Spacer(1, 0.3*inch))
        
        # Month-over-month growth
        if 'month_over_month_growth' in insights:
            elements.append(Paragraph("Month-over-Month Growth", self.styles['SubHeader']))
            growth_data = [['Month', 'Growth Rate']]
            for item in insights['month_over_month_growth'][-12:]:  # Last 12 months
                growth_data.append([
                    str(item['month'])[-7:],
                    f"{item['growth_rate_percent']:+.1f}%"
                ])
            
            col_widths = [TWO_COL_WIDTH, TWO_COL_WIDTH]
            growth_table = self._create_styled_table(growth_data, col_widths=col_widths, align_values_right=True)
            elements.append(growth_table)
            elements.append(Spacer(1, 0.3*inch))
        
        # Quarterly trends
        if 'quarterly_trends' in insights:
            elements.append(Paragraph("Quarterly Performance", self.styles['SubHeader']))
            quarter_data = [['Quarter', 'Total Amount', 'Transactions', 'Avg Transaction']]
            for item in insights['quarterly_trends']:
                quarter_data.append([
                    str(item['quarter']),
                    f"${item['total_amount']:,.2f}",
                    f"{item['transaction_count']:,}",
                    f"${item['average_transaction']:,.2f}"
                ])
            
            col_widths = [DRAWING_WIDTH * 0.25, DRAWING_WIDTH * 0.25, DRAWING_WIDTH * 0.25, DRAWING_WIDTH * 0.25]
            quarter_table = self._create_styled_table(quarter_data, col_widths=col_widths, align_values_right=True)
            elements.append(quarter_table)
            elements.append(Spacer(1, 0.3*inch))
        
        # Year-over-year growth
        if 'year_over_year_growth' in insights:
            elements.append(Paragraph("Year-over-Year Growth", self.styles['SubHeader']))
            yoy_data = [['Year', 'Growth Rate', 'Absolute Change']]
            for item in insights['year_over_year_growth']:
                yoy_data.append([
                    str(item['year']),
                    f"{item['growth_rate_percent']:+.1f}%",
                    f"${item['absolute_change']:+,.2f}"
                ])
            
            col_widths = [DRAWING_WIDTH * 0.33, DRAWING_WIDTH * 0.33, DRAWING_WIDTH * 0.34]
            yoy_table = self._create_styled_table(yoy_data, col_widths=col_widths, align_values_right=True)
            elements.append(yoy_table)
            elements.append(Spacer(1, 0.3*inch))
        
        # Day of week patterns
        if 'day_of_week_patterns' in insights:
            elements.append(Paragraph("Day of Week Patterns", self.styles['SubHeader']))
            chart = self._create_bar_chart(
                insights['day_of_week_patterns'],
                'day_of_week', 'total_amount',
                "Day of Week Patterns"
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


# Main function to export finance insights to PDF
def export_finance_to_pdf(insights: Dict[str, Any], company_name: str = "Company") -> bytes:
    """
    Export finance insights to PDF
    
    Args:
        insights: Dictionary containing finance insights from FinanceAnalysisService
        company_name: Optional company name for the report
    
    Returns:
        PDF file as bytes
    """
    exporter = FinancePDFExporter()
    pdf_bytes = exporter.generate_pdf(insights)
    return pdf_bytes


def save_finance_pdf(insights: Dict[str, Any], output_path: str):
    """
    Save finance insights to a PDF file
    
    Args:
        insights: Dictionary containing finance insights
        output_path: Path where PDF should be saved
    """
    exporter = FinancePDFExporter()
    exporter.generate_pdf(insights, output_path=output_path)