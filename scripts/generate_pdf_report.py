from fpdf import FPDF
import datetime
import os

class PDFReport(FPDF):
    def header(self):
        # Draw a blue stripe at the top
        self.set_fill_color(30, 58, 138)
        self.rect(0, 0, 210, 15, 'F')
        self.set_font('helvetica', 'B', 10)
        self.set_text_color(255, 255, 255)
        self.set_y(5)
        self.cell(0, 5, 'NATIONAL BANK OF ETHIOPIA CONSORTIUM - STRATEGIC REPORT', 0, 1, 'C')
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('helvetica', 'I', 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f'Page {self.page_no()} | Selam Financial Inclusion Forecasting Engine', 0, 0, 'C')

    def chapter_title(self, title):
        self.set_font('helvetica', 'B', 16)
        self.set_text_color(30, 58, 138)
        self.cell(0, 12, title, ln=True)
        self.ln(2)

    def chapter_body(self, body):
        self.set_font('helvetica', '', 11)
        self.set_text_color(0, 0, 0)
        self.multi_cell(0, 7, body)
        self.ln(8)

def generate_report():
    pdf = PDFReport()
    pdf.set_auto_page_break(auto=True, margin=20)
    pdf.add_page()
    
    # Title
    pdf.set_y(30)
    pdf.set_font('helvetica', 'B', 28)
    pdf.set_text_color(30, 58, 138)
    pdf.multi_cell(0, 12, "Ethiopia's Digital Financial Transformation: A Data-Driven Forecast (2025-2027)")
    pdf.ln(5)
    
    # Subtitle
    pdf.set_font('helvetica', 'I', 14)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 10, "By the Selam Analytics Team", ln=True)
    pdf.ln(15)
    
    # Executive Summary
    pdf.chapter_title("Executive Summary")
    pdf.chapter_body("Ethiopia is navigating one of the most significant economic transformations in Sub-Saharan Africa. With the structural shift from a state-led monopoly to a dynamic, multi-operator ecosystem, the stakes for financial inclusion have never been higher.\n\nOur analysis reveals a market of deep contrasts. On one hand, infrastructure and digital adoption are moving at breakneck speed, highlighted by the 'P2P Crossover' milestone where digital transfers now outpace cash withdrawals. On the other hand, unique account ownership is meeting significant headwind, growing only 3 percentage points between 2021 and 2024 despite tens of millions of new mobile money registrations. This report provides a detailed forecast for the 2025-2027 period, offering a roadmap for achieving ambitious national targets.")

    # Data and Methodology
    pdf.chapter_title("Data and Methodology Description")
    pdf.chapter_body("1. The Unified Dataset: We aggregated 13 years of temporal data (2014-2025) across Global Findex, Operator Reports, IMF Surveys, and GSMA data.\n\n2. Hybrid Forecasting Framework: A dual-approach system combining baseline status-quo regression with an Event-Augmented S-Curve model. This simulates the lag-time adoption build-up post-launch and accounts for user overlap via a 0.6 calibration multiplier.")

    # Key Insights
    pdf.chapter_title("Key Insights from Exploratory Analysis")
    pdf.chapter_body("- The P2P Crossover Milestone (2024): Digital peer-to-peer transfers officially surpassed ATM cash withdrawal counts, signaling a self-sustaining digital liquidity pool.\n- The Slowdown Paradox: 60M+ new registrations only yielded a 3pp growth in unique inclusion, revealing high duplication among existing bank users.\n- The Structural Gender Gap: A persistent 18-20pp gap remains, primarily driven by disparities in smartphone access and digital literacy.")

    # Event Impact Model
    pdf.chapter_title("Event Impact Model & Forecasts")
    pdf.chapter_body("Our projections show Ethiopia reaching 64.6% Account Ownership and 48.4% Digital Payment Usage by 2027. While a significant leap, the 70% NFIS-II target planned for 2025 is likely to be reached in 2028-2029 under base conditions.")

    # Dashboard Showcase (New Page)
    pdf.add_page()
    pdf.chapter_title("Stakeholder Dashboard: Exploring the Future")
    pdf.chapter_body("To put this data into the hands of decision-makers, we developed an interactive Streamlit Dashboard. It features scenario toggles, real-time KPI tracking, and channel-level comparisons.")
    
    # Embed Image
    img_path = "/Users/sintayehuabaynhe/.gemini/antigravity/brain/14481e5b-0c6f-45aa-9dcd-ff2015e7d439/dashboard_mockup_overview_1770238251694.png"
    if os.path.exists(img_path):
        pdf.image(img_path, x=15, y=50, w=180)
        pdf.set_y(230)
        pdf.set_font('helvetica', 'I', 9)
        pdf.cell(0, 10, "Figure 1: High-fidelity mockup of the Ethiopia Financial Inclusion Dashboard", 0, 1, 'C')
    
    # Limitations
    pdf.add_page()
    pdf.set_y(30)
    pdf.chapter_title("Limitations and Future Work")
    pdf.chapter_body("Focus should shift from 'Account Count' toward 'Usage Depth'. We recommend prioritizing merchant payment integration and micro-insurance. Data sparsity remains a constraint, necessitating a shift toward quarterly proxy reporting from regional operators.")

    pdf.set_font('helvetica', 'B', 12)
    pdf.set_text_color(30, 58, 138)
    pdf.ln(10)
    pdf.cell(0, 10, "END OF REPORT", 0, 1, 'C')

    pdf.output("reports/ethiopia_fi_final_report_detailed.pdf")
    print("Detailed PDF report generated successfully at reports/ethiopia_fi_final_report_detailed.pdf")

if __name__ == "__main__":
    generate_report()
