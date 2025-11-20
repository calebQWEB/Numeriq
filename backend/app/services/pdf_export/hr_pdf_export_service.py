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


class HRPDFExporter:
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
        """Generate comprehensive HR PDF report"""
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
        
        # Workforce Composition
        if 'workforce_overview' in insights:
            story.extend(self._create_workforce_section(insights))
            story.append(PageBreak())
        
        # Department Analysis
        if 'department_metrics' in insights:
            story.extend(self._create_department_section(insights))
            story.append(PageBreak())
        
        # Compensation Analysis
        if 'compensation_overview' in insights:
            story.extend(self._create_compensation_section(insights))
            story.append(PageBreak())
        
        # Performance Analysis
        if 'performance_overview' in insights:
            story.extend(self._create_performance_section(insights))
            story.append(PageBreak())
        
        # Turnover & Retention
        if 'tenure_metrics' in insights or 'turnover_metrics' in insights:
            story.extend(self._create_turnover_section(insights))
            story.append(PageBreak())
        
        # Training & Development
        if 'training_overview' in insights:
            story.extend(self._create_training_section(insights))
            story.append(PageBreak())
        
        # Demographics
        if 'demographics' in insights:
            story.extend(self._create_demographics_section(insights))
            story.append(PageBreak())
        
        # Attendance & Leave
        if 'attendance_metrics' in insights:
            story.extend(self._create_attendance_section(insights))
        
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
        
        title = Paragraph("HUMAN RESOURCES ANALYTICS REPORT", self.styles['CustomTitle'])
        elements.append(title)
        elements.append(Spacer(1, 0.5*inch))
        
        subtitle = Paragraph(
            f"Workforce Analysis: {datetime.now().strftime('%B %d, %Y')}",
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
        
        if 'workforce_overview' in insights:
            overview = insights['workforce_overview']
            summary_data.append(['Total Employees', f"{overview.get('total_employees', 0):,}"])
            summary_data.append(['Active Employees', f"{overview.get('active_employees', 0):,}"])
        
        if 'compensation_overview' in insights:
            comp = insights['compensation_overview']
            summary_data.append(['Average Salary', f"${comp.get('avg_salary', 0):,.2f}"])
            summary_data.append(['Total Payroll', f"${comp.get('total_payroll', 0):,.2f}"])
        
        if 'tenure_metrics' in insights:
            tenure = insights['tenure_metrics']
            summary_data.append(['Avg Tenure (Years)', f"{tenure.get('avg_tenure_years', 0):.1f}"])
        
        if 'turnover_metrics' in insights:
            turnover = insights['turnover_metrics']
            summary_data.append(['Annual Turnover Rate', f"{turnover.get('annual_turnover_rate', 0):.1f}%"])
        
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
    
    def _create_workforce_section(self, insights: Dict[str, Any]) -> List:
        """Create workforce composition section"""
        elements = []
        elements.append(Paragraph("Workforce Composition", self.styles['SectionHeader']))
        elements.append(Spacer(1, 0.2*inch))
        
        if 'workforce_overview' in insights:
            overview = insights['workforce_overview']
            data = [
                ['Metric', 'Value'],
                ['Total Employees', f"{overview.get('total_employees', 0):,}"],
                ['Active Employees', f"{overview.get('active_employees', 0):,}"]
            ]
            col_widths = [TWO_COL_WIDTH, TWO_COL_WIDTH]
            table = self._create_styled_table(data, col_widths=col_widths, align_values_right=True)
            elements.append(table)
            elements.append(Spacer(1, 0.3*inch))
        
        # Department and Position Distribution side by side
        left_content = []
        right_content = []
        
        if 'department_distribution' in insights:
            left_content.append(Paragraph("Department Distribution", self.styles['SubHeader']))
            chart = self._create_pie_chart(
                insights['department_distribution'][:6],
                'department', 'employee_count',
                "Department Distribution"
            )
            left_content.append(chart)
        
        if 'position_distribution' in insights:
            right_content.append(Paragraph("Top 10 Positions", self.styles['SubHeader']))
            position_data = [['Position', 'Count']]
            for item in insights['position_distribution'][:10]:
                position_data.append([
                    item['position'][:30],
                    f"{item['employee_count']:,}"
                ])
            pos_col_widths = [TWO_COL_WIDTH * 0.7, TWO_COL_WIDTH * 0.3]
            pos_table = self._create_styled_table(position_data, col_widths=pos_col_widths, align_values_right=True)
            right_content.append(pos_table)
        
        if left_content and right_content:
            side_by_side = Table([[left_content, right_content]], colWidths=[TWO_COL_WIDTH, TWO_COL_WIDTH])
            side_by_side.setStyle(TableStyle([
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('LEFTPADDING', (1, 0), (1, 0), 15),
            ]))
            elements.append(side_by_side)
        elif left_content:
            elements.extend(left_content)
        elif right_content:
            elements.extend(right_content)
        
        # Location Distribution
        if 'location_distribution' in insights:
            elements.append(Spacer(1, 0.3*inch))
            elements.append(Paragraph("Location Distribution", self.styles['SubHeader']))
            loc_data = [['Location', 'Employee Count']]
            for item in insights['location_distribution']:
                loc_data.append([item['location'], f"{item['employee_count']:,}"])
            loc_col_widths = [TWO_COL_WIDTH, TWO_COL_WIDTH]
            loc_table = self._create_styled_table(loc_data, col_widths=loc_col_widths, align_values_right=True)
            elements.append(loc_table)
        
        return elements
    
    def _create_department_section(self, insights: Dict[str, Any]) -> List:
        """Create department metrics section"""
        elements = []
        elements.append(Paragraph("Department Analysis", self.styles['SectionHeader']))
        elements.append(Spacer(1, 0.2*inch))
        
        dept_metrics = insights.get('department_metrics', {})
        
        if 'salary_by_department' in dept_metrics:
            elements.append(Paragraph("Salary by Department", self.styles['SubHeader']))
            salary_data = [['Department', 'Avg Salary', 'Median Salary', 'Employees']]
            for item in dept_metrics['salary_by_department']:
                salary_data.append([
                    item['department'][:25],
                    f"${item['avg_salary']:,.2f}",
                    f"${item['median_salary']:,.2f}",
                    f"{item['employee_count']:,}"
                ])
            col_widths = [DRAWING_WIDTH * 0.4, DRAWING_WIDTH * 0.2, DRAWING_WIDTH * 0.2, DRAWING_WIDTH * 0.2]
            salary_table = self._create_styled_table(salary_data, col_widths=col_widths, align_values_right=True)
            elements.append(salary_table)
            elements.append(Spacer(1, 0.3*inch))
        
        if 'performance_by_department' in dept_metrics:
            elements.append(Paragraph("Performance by Department", self.styles['SubHeader']))
            perf_data = [['Department', 'Avg Rating', 'Employees Rated']]
            for item in dept_metrics['performance_by_department']:
                perf_data.append([
                    item['department'][:25],
                    f"{item['avg_performance_rating']:.2f}",
                    f"{item['employees_rated']:,}"
                ])
            col_widths = [DRAWING_WIDTH * 0.5, DRAWING_WIDTH * 0.25, DRAWING_WIDTH * 0.25]
            perf_table = self._create_styled_table(perf_data, col_widths=col_widths, align_values_right=True)
            elements.append(perf_table)
        
        return elements
    
    def _create_compensation_section(self, insights: Dict[str, Any]) -> List:
        """Create compensation analysis section"""
        elements = []
        elements.append(Paragraph("Compensation Analysis", self.styles['SectionHeader']))
        elements.append(Spacer(1, 0.2*inch))
        
        if 'compensation_overview' in insights:
            comp = insights['compensation_overview']
            data = [
                ['Metric', 'Value'],
                ['Average Salary', f"${comp.get('avg_salary', 0):,.2f}"],
                ['Median Salary', f"${comp.get('median_salary', 0):,.2f}"],
                ['Salary Range', f"${comp.get('salary_range', {}).get('min', 0):,.2f} - ${comp.get('salary_range', {}).get('max', 0):,.2f}"],
                ['Total Payroll', f"${comp.get('total_payroll', 0):,.2f}"],
                ['Salary Std Dev', f"${comp.get('salary_std_dev', 0):,.2f}"]
            ]
            col_widths = [TWO_COL_WIDTH, TWO_COL_WIDTH]
            table = self._create_styled_table(data, col_widths=col_widths, align_values_right=True)
            elements.append(table)
            elements.append(Spacer(1, 0.3*inch))
        
        if 'salary_by_position' in insights:
            elements.append(Paragraph("Top 15 Highest Paid Positions", self.styles['SubHeader']))
            position_data = [['Position', 'Avg Salary', 'Median Salary', 'Employees']]
            for item in insights['salary_by_position'][:15]:
                position_data.append([
                    item['position'][:30],
                    f"${item['avg_salary']:,.2f}",
                    f"${item['median_salary']:,.2f}",
                    f"{item['employee_count']:,}"
                ])
            col_widths = [DRAWING_WIDTH * 0.4, DRAWING_WIDTH * 0.2, DRAWING_WIDTH * 0.2, DRAWING_WIDTH * 0.2]
            pos_table = self._create_styled_table(position_data, col_widths=col_widths, align_values_right=True)
            elements.append(pos_table)
            elements.append(Spacer(1, 0.3*inch))
        
        if 'salary_distribution' in insights:
            elements.append(Paragraph("Salary Distribution", self.styles['SubHeader']))
            dist = insights['salary_distribution']
            quartiles = dist.get('quartiles', {})
            percentiles = dist.get('percentiles', {})
            
            dist_data = [
                ['Metric', 'Value'],
                ['Q1 (25th Percentile)', f"${quartiles.get('q1', 0):,.2f}"],
                ['Q2 (Median)', f"${quartiles.get('q2', 0):,.2f}"],
                ['Q3 (75th Percentile)', f"${quartiles.get('q3', 0):,.2f}"],
                ['P10', f"${percentiles.get('p10', 0):,.2f}"],
                ['P90', f"${percentiles.get('p90', 0):,.2f}"]
            ]
            col_widths = [TWO_COL_WIDTH, TWO_COL_WIDTH]
            dist_table = self._create_styled_table(dist_data, col_widths=col_widths, align_values_right=True)
            elements.append(dist_table)
        
        return elements
    
    def _create_performance_section(self, insights: Dict[str, Any]) -> List:
        """Create performance analysis section"""
        elements = []
        elements.append(Paragraph("Performance Analysis", self.styles['SectionHeader']))
        elements.append(Spacer(1, 0.2*inch))
        
        left_content = []
        right_content = []
        
        if 'performance_overview' in insights:
            perf = insights['performance_overview']
            left_content.append(Paragraph("Performance Metrics", self.styles['SubHeader']))
            data = [
                ['Metric', 'Value'],
                ['Avg Performance Rating', f"{perf.get('avg_performance_rating', 0):.2f}"],
                ['Median Rating', f"{perf.get('median_performance_rating', 0):.2f}"],
                ['High Performers', f"{perf.get('high_performers', 0):,}"],
                ['Low Performers', f"{perf.get('low_performers', 0):,}"]
            ]
            col_widths = [TWO_COL_WIDTH * 0.6, TWO_COL_WIDTH * 0.4]
            perf_table = self._create_styled_table(data, col_widths=col_widths, align_values_right=True)
            left_content.append(perf_table)
        
        if 'performance_distribution' in insights:
            right_content.append(Paragraph("Performance Distribution", self.styles['SubHeader']))
            chart = self._create_bar_chart(
                insights['performance_distribution'],
                'category', 'employee_count',
                "Performance Distribution"
            )
            right_content.append(chart)
        
        if left_content and right_content:
            side_by_side = Table([[left_content, right_content]], colWidths=[TWO_COL_WIDTH, TWO_COL_WIDTH])
            side_by_side.setStyle(TableStyle([
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('LEFTPADDING', (1, 0), (1, 0), 15),
            ]))
            elements.append(side_by_side)
        elif left_content:
            elements.extend(left_content)
        elif right_content:
            elements.extend(right_content)
        
        return elements
    
    def _create_turnover_section(self, insights: Dict[str, Any]) -> List:
        """Create turnover and retention section"""
        elements = []
        elements.append(Paragraph("Turnover & Retention Analysis", self.styles['SectionHeader']))
        elements.append(Spacer(1, 0.2*inch))
        
        left_content = []
        right_content = []
        
        if 'tenure_metrics' in insights:
            tenure = insights['tenure_metrics']
            left_content.append(Paragraph("Tenure Metrics", self.styles['SubHeader']))
            data = [
                ['Metric', 'Value'],
                ['Avg Tenure (Years)', f"{tenure.get('avg_tenure_years', 0):.1f}"],
                ['Median Tenure (Years)', f"{tenure.get('median_tenure_years', 0):.1f}"],
                ['New Hires (Last Year)', f"{tenure.get('new_hires_last_year', 0):,}"],
                ['Long Tenure (5+ Years)', f"{tenure.get('long_tenure_employees', 0):,}"]
            ]
            col_widths = [TWO_COL_WIDTH * 0.6, TWO_COL_WIDTH * 0.4]
            tenure_table = self._create_styled_table(data, col_widths=col_widths, align_values_right=True)
            left_content.append(tenure_table)
        
        if 'turnover_metrics' in insights:
            turnover = insights['turnover_metrics']
            right_content.append(Paragraph("Turnover Metrics", self.styles['SubHeader']))
            data = [
                ['Metric', 'Value'],
                ['Total Terminations', f"{turnover.get('total_terminations', 0):,}"],
                ['Terminations (Last Year)', f"{turnover.get('terminations_last_year', 0):,}"],
                ['Annual Turnover Rate', f"{turnover.get('annual_turnover_rate', 0):.2f}%"]
            ]
            col_widths = [TWO_COL_WIDTH * 0.6, TWO_COL_WIDTH * 0.4]
            turnover_table = self._create_styled_table(data, col_widths=col_widths, align_values_right=True)
            right_content.append(turnover_table)
        
        if left_content and right_content:
            side_by_side = Table([[left_content, right_content]], colWidths=[TWO_COL_WIDTH, TWO_COL_WIDTH])
            side_by_side.setStyle(TableStyle([
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('LEFTPADDING', (1, 0), (1, 0), 15),
            ]))
            elements.append(side_by_side)
        elif left_content:
            elements.extend(left_content)
        elif right_content:
            elements.extend(right_content)
        
        if 'hiring_trends' in insights:
            elements.append(Spacer(1, 0.3*inch))
            elements.append(Paragraph("Hiring Trends (Last 12 Months)", self.styles['SubHeader']))
            chart = self._create_line_chart(
                insights['hiring_trends'],
                'month', 'hires',
                "Hiring Trends"
            )
            chart_container = Table([[chart]], colWidths=[DRAWING_WIDTH])
            chart_container.setStyle(TableStyle([('ALIGN', (0,0), (-1,-1), 'CENTER')]))
            elements.append(chart_container)
        
        return elements
    
    def _create_training_section(self, insights: Dict[str, Any]) -> List:
        """Create training and development section"""
        elements = []
        elements.append(Paragraph("Training & Development", self.styles['SectionHeader']))
        elements.append(Spacer(1, 0.2*inch))
        
        if 'training_overview' in insights:
            training = insights['training_overview']
            data = [
                ['Metric', 'Value'],
                ['Avg Training Hours', f"{training.get('avg_training_hours', 0):.1f}"],
                ['Median Training Hours', f"{training.get('median_training_hours', 0):.1f}"],
                ['Total Training Hours', f"{training.get('total_training_hours', 0):,.0f}"],
                ['Employees with Training', f"{training.get('employees_with_training', 0):,}"],
                ['Avg Hours per Employee', f"{training.get('avg_training_per_employee', 0):.1f}"]
            ]
            col_widths = [TWO_COL_WIDTH, TWO_COL_WIDTH]
            training_table = self._create_styled_table(data, col_widths=col_widths, align_values_right=True)
            elements.append(training_table)
            elements.append(Spacer(1, 0.3*inch))
        
        if 'training_by_department' in insights:
            elements.append(Paragraph("Training by Department", self.styles['SubHeader']))
            dept_data = [['Department', 'Avg Hours', 'Total Hours', 'Employees']]
            for item in insights['training_by_department']:
                dept_data.append([
                    item['department'][:25],
                    f"{item['avg_training_hours']:.1f}",
                    f"{item['total_training_hours']:,.0f}",
                    f"{item['employees_trained']:,}"
                ])
            col_widths = [DRAWING_WIDTH * 0.4, DRAWING_WIDTH * 0.2, DRAWING_WIDTH * 0.2, DRAWING_WIDTH * 0.2]
            dept_table = self._create_styled_table(dept_data, col_widths=col_widths, align_values_right=True)
            elements.append(dept_table)
        
        return elements
    
    def _create_demographics_section(self, insights: Dict[str, Any]) -> List:
        """Create demographics section"""
        elements = []
        elements.append(Paragraph("Workforce Demographics", self.styles['SectionHeader']))
        elements.append(Spacer(1, 0.2*inch))
        
        demographics = insights.get('demographics', {})
        left_content = []
        right_content = []
        
        if 'age_metrics' in demographics:
            age = demographics['age_metrics']
            left_content.append(Paragraph("Age Metrics", self.styles['SubHeader']))
            data = [
                ['Metric', 'Value'],
                ['Average Age', f"{age.get('avg_age', 0):.1f}"],
                ['Median Age', f"{age.get('median_age', 0):.1f}"],
                ['Age Range', f"{age.get('age_range', {}).get('min', 0):.0f} - {age.get('age_range', {}).get('max', 0):.0f}"]
            ]
            col_widths = [TWO_COL_WIDTH * 0.6, TWO_COL_WIDTH * 0.4]
            age_table = self._create_styled_table(data, col_widths=col_widths, align_values_right=True)
            left_content.append(age_table)
            
            if 'age_distribution' in demographics:
                left_content.append(Spacer(1, 0.2*inch))
                age_dist_data = [['Age Group', 'Count']]
                for item in demographics['age_distribution']:
                    age_dist_data.append([item['age_group'], f"{item['employee_count']:,}"])
                col_widths = [TWO_COL_WIDTH * 0.5, TWO_COL_WIDTH * 0.5]
                age_dist_table = self._create_styled_table(age_dist_data, col_widths=col_widths, align_values_right=True)
                left_content.append(age_dist_table)
        
        if 'gender_distribution' in demographics:
            right_content.append(Paragraph("Gender Distribution", self.styles['SubHeader']))
            chart = self._create_pie_chart(
                demographics['gender_distribution'],
                'gender', 'employee_count',
                "Gender Distribution"
            )
            right_content.append(chart)
        
        if left_content and right_content:
            side_by_side = Table([[left_content, right_content]], colWidths=[TWO_COL_WIDTH, TWO_COL_WIDTH])
            side_by_side.setStyle(TableStyle([
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('LEFTPADDING', (1, 0), (1, 0), 15),
            ]))
            elements.append(side_by_side)
        elif left_content:
            elements.extend(left_content)
        elif right_content:
            elements.extend(right_content)
        
        return elements
    
    def _create_attendance_section(self, insights: Dict[str, Any]) -> List:
        """Create attendance and leave section"""
        elements = []
        elements.append(Paragraph("Attendance & Leave Analysis", self.styles['SectionHeader']))
        elements.append(Spacer(1, 0.2*inch))
        
        attendance = insights.get('attendance_metrics', {})
        
        # Create three columns for sick leave, vacation, and overtime
        columns = []
        
        if 'sick_leave' in attendance:
            sick = attendance['sick_leave']
            sick_content = [
                Paragraph("Sick Leave", self.styles['SubHeader']),
                self._create_styled_table([
                    ['Metric', 'Value'],
                    ['Avg Days', f"{sick.get('avg_sick_days', 0):.1f}"],
                    ['Median Days', f"{sick.get('median_sick_days', 0):.1f}"],
                    ['Total Days', f"{sick.get('total_sick_days', 0):,.0f}"],
                    ['Employees', f"{sick.get('employees_with_sick_leave', 0):,}"]
                ], col_widths=[DRAWING_WIDTH/3 * 0.6, DRAWING_WIDTH/3 * 0.4], align_values_right=True)
            ]
            columns.append(sick_content)
        
        if 'vacation' in attendance:
            vac = attendance['vacation']
            vac_content = [
                Paragraph("Vacation Leave", self.styles['SubHeader']),
                self._create_styled_table([
                    ['Metric', 'Value'],
                    ['Avg Days', f"{vac.get('avg_vacation_days', 0):.1f}"],
                    ['Median Days', f"{vac.get('median_vacation_days', 0):.1f}"],
                    ['Total Days', f"{vac.get('total_vacation_days', 0):,.0f}"]
                ], col_widths=[DRAWING_WIDTH/3 * 0.6, DRAWING_WIDTH/3 * 0.4], align_values_right=True)
            ]
            columns.append(vac_content)
        
        if 'overtime' in attendance:
            ot = attendance['overtime']
            ot_content = [
                Paragraph("Overtime Hours", self.styles['SubHeader']),
                self._create_styled_table([
                    ['Metric', 'Value'],
                    ['Avg Hours', f"{ot.get('avg_overtime_hours', 0):.1f}"],
                    ['Total Hours', f"{ot.get('total_overtime_hours', 0):,.0f}"],
                    ['Employees', f"{ot.get('employees_with_overtime', 0):,}"]
                ], col_widths=[DRAWING_WIDTH/3 * 0.6, DRAWING_WIDTH/3 * 0.4], align_values_right=True)
            ]
            columns.append(ot_content)
        
        if columns:
            # Pad to 3 columns if needed
            while len(columns) < 3:
                columns.append([])
            
            # Create side-by-side layout
            col_width = DRAWING_WIDTH / 3
            multi_col_table = Table([columns], colWidths=[col_width] * 3)
            multi_col_table.setStyle(TableStyle([
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('LEFTPADDING', (1, 0), (1, 0), 10),
                ('LEFTPADDING', (2, 0), (2, 0), 10),
            ]))
            elements.append(multi_col_table)
        
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
        drawing = Drawing(TWO_COL_WIDTH, 250)
        
        chart = VerticalBarChart()
        chart.x = 30
        chart.y = 50
        chart.height = 175
        chart.width = TWO_COL_WIDTH - 60
        
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


# Main function to export HR insights to PDF
def export_hr_to_pdf(insights: Dict[str, Any], company_name: str = "Company") -> bytes:
    """
    Export HR insights to PDF
    
    Args:
        insights: Dictionary containing HR insights from HRAnalysisService
        company_name: Optional company name for the report
    
    Returns:
        PDF file as bytes
    """
    exporter = HRPDFExporter()
    pdf_bytes = exporter.generate_pdf(insights)
    return pdf_bytes


def save_hr_pdf(insights: Dict[str, Any], output_path: str):
    """
    Save HR insights to a PDF file
    
    Args:
        insights: Dictionary containing HR insights
        output_path: Path where PDF should be saved
    """
    exporter = HRPDFExporter()
    exporter.generate_pdf(insights, output_path=output_path)