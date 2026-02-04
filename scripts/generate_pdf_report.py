from fpdf import FPDF
import datetime
import os

class PDFReport(FPDF):
    def header(self):
        # Professional header with logo-like mark
        self.set_fill_color(30, 58, 138)
        self.rect(0, 0, 210, 20, 'F')
        self.set_font('helvetica', 'B', 12)
        self.set_text_color(255, 255, 255)
        self.set_xy(10, 7)
        self.cell(0, 5, 'ETHIOPIA FINANCIAL INCLUSION: STRATEGIC FORECAST 2025-2027', 0, 1, 'L')
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('helvetica', 'I', 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f'Page {self.page_no()} | Selam Analytics Forecasting Suite | Confidential', 0, 0, 'C')

    def chapter_title(self, title):
        self.set_font('helvetica', 'B', 16)
        self.set_text_color(30, 58, 138)
        self.cell(0, 12, title, ln=True)
        self.ln(2)

    def chapter_body(self, body):
        self.set_font('helvetica', '', 11)
        self.set_text_color(0, 0, 0)
        self.multi_cell(0, 7, body)
        self.ln(5)

    def embed_image(self, img_path, caption):
        if os.path.exists(img_path):
            # Check if image fits or need new page
            if self.get_y() > 200:
                self.add_page()
            self.image(img_path, x=20, w=170)
            self.ln(2)
            self.set_font('helvetica', 'I', 9)
            self.set_text_color(100, 100, 100)
            self.cell(0, 10, caption, 0, 1, 'C')
            self.ln(5)

def generate_report():
    pdf = PDFReport()
    pdf.set_auto_page_break(auto=True, margin=25)
    
    # --- PAGE 1: TITLE & EXECUTIVE SUMMARY ---
    pdf.add_page()
    pdf.set_y(35)
    pdf.set_font('helvetica', 'B', 28)
    pdf.set_text_color(30, 58, 138)
    pdf.multi_cell(0, 12, "Ethiopia's Digital Financial Transformation: A Data-Driven Forecast")
    pdf.ln(5)
    pdf.set_font('helvetica', 'I', 14)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 10, "Strategic Analysis for the NBE Consortium", ln=True)
    pdf.ln(10)

    pdf.chapter_title("1. Executive Summary")
    pdf.chapter_body("Ethiopia is undergoing a structural paradigm shift. The transition from a monopoly banking sector to a competitive digital-first ecosystem has unlocked transactional volume, but universal inclusion remains challenging. We project 64.6% Access by 2027, falling short of the 70% NFIS-II target. This report provides the technical evidence for this gap and outlines policy levers to close it.")

    # --- PAGE 2: METHODOLOGY ---
    pdf.add_page()
    pdf.set_y(30)
    pdf.chapter_title("2. Methodology & Data Enrichment")
    pdf.chapter_body("2.1 Data Enrichment: We performed strategic enrichment using Global Findex 2024 baselines, IMF infrastructure multipliers, and GSMA connectivity data to calibrate the model.\n\n2.2 Impact Modeling: We implemented a Logistic S-Curve function (Impact(t) = L / (1 + exp(-k(t-x0)))) to simulate the adoption build-up post-launch. This accounts for months of lag and market penetration speed.")

    # --- PAGE 3: KEY INSIGHTS & EVIDENCE ---
    pdf.add_page()
    pdf.set_y(30)
    pdf.chapter_title("3. Key Insights & Evidence")
    pdf.chapter_body("3.1 The 'Slowdown Paradox' (2021-2024): Evidence reveals a 0.6 Overlap Factor, meaning digital accounts primarily attract existing bank users rather than the unbanked.")
    pdf.embed_image("reports/figures/slowdown_paradox_evidence.png", "Figure 1: Comparison of Mobile Money Enrollment vs. Unique Account Ownership")
    
    pdf.chapter_body("3.2 The P2P Crossover: In 2024, digital P2P transaction counts officially surpassed ATM cash withdrawals, signaling a shift toward digital liquidity.")
    pdf.embed_image("reports/figures/p2p_crossover_evidence.png", "Figure 2: Transaction Volume Shift from Cash (ATM) to Digital (P2P)")

    # --- PAGE 4: FORECASTS & VALIDATION ---
    pdf.add_page()
    pdf.set_y(30)
    pdf.chapter_title("4. Forecasts & Scenario Analysis")
    pdf.chapter_body("We project a 'Base' trajectory of 64.6% Access by 2027, with an 'Optimistic' upside of 69.8% dependent on Digital ID (Fayda) acceleration.")
    pdf.embed_image("reports/figures/forecast_scenarios.png", "Figure 3: 2025-2027 Forecast Scenarios (Base, Optimistic, Pessimistic)")

    pdf.chapter_title("5. Impact Model Validation")
    pdf.chapter_body("Methodology backtesting against Telebirr (May 2021) shows a near-perfect match with historical growth when using our 0.6 calibrated overlap discount.")
    pdf.embed_image("reports/figures/impact_validation_evidence.png", "Figure 4: Predicted vs. Observed Impact Build-up for Telebirr Launch")

    # --- PAGE 5: RECOMMENDATIONS & LIMITATIONS ---
    pdf.add_page()
    pdf.set_y(30)
    pdf.chapter_title("6. Recommendations & Policy Levers")
    pdf.chapter_body("1. Accelerate Fayda ID: Modeling show this as the strongest net-new driver (+5pp).\n2. Harmonize Interoperability: Essential to reduce the 0.4 overlap loss identified.\n3. Rural Infrastructure: 4G is a primary leading indicator for our 48.4% Usage projection.")

    pdf.chapter_title("7. Limitations & Future Work")
    pdf.chapter_body("Primary constraints include Registration Bias (active vs registered gap) and the 3-year Findex survey lag. Future work will focus on Merchant Adoption and Regional Disaggregation (e.g., Oromia vs Amhara).")

    pdf.ln(10)
    pdf.set_font('helvetica', 'B', 12)
    pdf.cell(0, 10, "END OF STRATEGIC REPORT", 0, 1, 'C')

    pdf.output("reports/ethiopia_fi_final_report_detailed.pdf")
    print("Comprehensive PDF report generated successfully at reports/ethiopia_fi_final_report_detailed.pdf")

if __name__ == "__main__":
    generate_report()
