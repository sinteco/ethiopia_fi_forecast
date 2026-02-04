from fpdf import FPDF
import datetime
import os

class NarrativePDF(FPDF):
    def header(self):
        if self.page_no() == 1:
            return
        self.set_fill_color(30, 58, 138)
        self.rect(0, 0, 210, 15, 'F')
        self.set_font('helvetica', 'B', 9)
        self.set_text_color(255, 255, 255)
        self.set_y(5)
        self.cell(0, 5, 'THE DIGITAL LEAP: NAVIGATING ETHIOPIA\'S FINANCIAL FUTURE', 0, 1, 'C')
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('helvetica', 'I', 8)
        self.set_text_color(150, 150, 150)
        self.cell(0, 10, f'Page {self.page_no()} | Selam Analytics Strategic Outlook', 0, 0, 'C')

    def section_title(self, title):
        self.set_font('helvetica', 'B', 18)
        self.set_text_color(30, 58, 138)
        self.cell(0, 15, title, ln=True)
        self.ln(2)

    def body_text(self, text):
        self.set_font('helvetica', '', 12)
        self.set_text_color(50, 50, 50)
        self.multi_cell(0, 8, text)
        self.ln(5)

    def draw_matrix(self):
        # Table Header
        self.set_fill_color(240, 244, 255)
        self.set_font('helvetica', 'B', 10)
        self.set_text_color(30, 58, 138)
        self.cell(45, 10, ' Strategic Event', 1, 0, 'L', True)
        self.cell(40, 10, ' Target Metric', 1, 0, 'L', True)
        self.cell(35, 10, ' Impact', 1, 0, 'L', True)
        self.cell(70, 10, ' Rationale', 1, 1, 'L', True)
        
        # Table Content
        self.set_font('helvetica', '', 9)
        self.set_text_color(0, 0, 0)
        data = [
            ("Telebirr Launch", "Usage & Access", "High", "Market-making effect (National)."),
            ("Fayda Digital ID", "Access", "High", "Removes ID barriers for rural KYC."),
            ("Safaricom Entrada", "Usage", "Medium", "Competition and reliability."),
            ("NBE MM Directive", "Usage Depth", "Low", "Regulatory enabling/interop.")
        ]
        for row in data:
            self.cell(45, 10, f" {row[0]}", 1)
            self.cell(40, 10, f" {row[1]}", 1)
            self.cell(35, 10, f" {row[2]}", 1)
            self.cell(70, 10, f" {row[3]}", 1)
            self.ln(0)
            self.set_y(self.get_y() + 10)
        self.ln(10)

def generate_report():
    pdf = NarrativePDF()
    pdf.set_auto_page_break(auto=True, margin=20)
    
    # --- PAGE 1: HERO & VISION ---
    pdf.add_page()
    pdf.set_y(40)
    pdf.set_font('helvetica', 'B', 32)
    pdf.set_text_color(30, 58, 138)
    pdf.multi_cell(0, 15, "The Digital Leap: Navigating Ethiopia's Financial Future")
    pdf.ln(5)
    pdf.set_font('helvetica', 'I', 16)
    pdf.set_text_color(120, 120, 120)
    pdf.cell(0, 10, "Strategic Outlook 2025-2027", ln=True)
    pdf.ln(15)

    pdf.section_title("1. The Vision: Why Financial Inclusion?")
    pdf.body_text("For the NBE Consortium, inclusion is the bedrock of a modern economy. The goal is Universal Access - bringing every Ethiopian into the formal fold to reduce poverty and empower entrepreneurs. Our forecast cuts through the noise of surging registrations to reveal the true path to this objective.")

    # --- PAGE 2: DATA STORY ---
    pdf.add_page()
    pdf.section_title("2. Setting the Stage: The Data Story")
    pdf.body_text("We bridge data gaps by 'enriching' our map with 2024 baselines. We track Smartphone Penetration and Branch Density as the 'pipes' of inclusion. Our methodology relies on historical benchmarking from top African markets to ensure reality-based modeling.")

    pdf.section_title("3. The 'How': Predicting Change")
    pdf.body_text("We use the 'Snowball Effect' (S-Curve) to model adoption. Change starts slow, accelerates through popularity, and stabilizes. Below is our Strategic Association Matrix - the impact map of our engine.")
    pdf.draw_matrix()

    # --- PAGE 3: INSIGHTS & ANALOGIES ---
    pdf.add_page()
    pdf.section_title("4. Key Lessons from the Past")
    pdf.body_text("The 'Slowdown Paradox' reminds us that big registration numbers don't always mean new inclusion. The 'Two-Wallet' Analogy clarifies why many Ethiopians simply have two accounts rather than being newly served. We apply a 0.6 discount factor to account for this overlap.")

    pdf.section_title("5. The Forecast: 2025-2027")
    pdf.body_text("We project 64.6% Access and 48.4% Usage by 2027. This signifies that while we are on the right track, the 70% national target requires accelerated Digital ID (Fayda) adoption to reach the final remaining unbanked populations.")

    # --- PAGE 4: DASHBOARD & LIMITS ---
    pdf.add_page()
    pdf.section_title("6. The Decision-Support Dashboard")
    pdf.body_text("Managers can explore outcomes in our interactive dashboard: the Overview scorecard for liquidity, the Trend Browser for correlations, and the Forecast Simulator for scenario planning.")
    
    img_path = "/Users/sintayehuabaynhe/.gemini/antigravity/brain/14481e5b-0c6f-45aa-9dcd-ff2015e7d439/dashboard_mockup_overview_1770238251694.png"
    if os.path.exists(img_path):
        pdf.image(img_path, x=20, w=170)
        pdf.ln(5)
        pdf.set_font('helvetica', 'I', 9)
        pdf.cell(0, 10, "Visualizing the Future: The Ethiopia FI Stakeholder Dashboard", 0, 1, 'C')
        pdf.ln(5)

    pdf.section_title("7. Knowing the Limits")
    pdf.body_text("No model is perfect. We acknowledge Survey Lag (rear-view mirror effect), Registration Bias (active vs passive users), and the assumption that history will continue without 'black swan' interruptions.")

    # --- FINAL PAGE: RECOMMENDATIONS ---
    pdf.add_page()
    pdf.section_title("8. The Road Ahead")
    pdf.body_text("1. Prioritize Fayda ID: The single biggest accelerator.\n2. Focus on Usage Depth: Move from 'counting accounts' to 'measuring frequency'.\n3. Bridge the Gender Gap: Target the 18% disparity with rural-first initiatives.")
    
    pdf.ln(20)
    pdf.set_font('helvetica', 'B', 14)
    pdf.set_text_color(30, 58, 138)
    pdf.cell(0, 10, "SELAM ANALYTICS - EMPOWERING CLARITY", 0, 1, 'C')

    pdf.output("reports/ethiopia_fi_strategic_outlook_2027.pdf")
    print("Narrative Strategic Outlook PDF generated successfully.")

if __name__ == "__main__":
    generate_report()
