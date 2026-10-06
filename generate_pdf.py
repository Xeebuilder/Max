import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            super().showPage()
        super().save()
        print(f"Total pages generated: {num_pages}")
        if num_pages > 1:
            print("WARNING: Resume exceeded 1 page!")

def build_pdf(filename="Maximiliano_Rodriguez_Resume_Optimized.pdf"):
    # Page setup: Letter is 612 x 792 pt. Margins: 30 pt
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        leftMargin=30,
        rightMargin=30,
        topMargin=26,
        bottomMargin=26
    )

    styles = getSampleStyleSheet()
    
    PRIMARY = colors.HexColor("#0F294A")   # Deep Navy
    SECONDARY = colors.HexColor("#1E3A8A") # Royal Navy
    DARK_TEXT = colors.HexColor("#1A202C") # Charcoal
    MUTED_TEXT = colors.HexColor("#4A5568")# Cool Gray
    LINE_COLOR = colors.HexColor("#CBD5E1")# Slate border

    name_style = ParagraphStyle(
        'NameStyle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=17.5,
        leading=19.5,
        textColor=PRIMARY,
        alignment=1
    )

    title_style = ParagraphStyle(
        'TitleStyle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=11.5,
        textColor=SECONDARY,
        alignment=1
    )

    contact_style = ParagraphStyle(
        'ContactStyle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.8,
        leading=10,
        textColor=MUTED_TEXT,
        alignment=1
    )

    section_heading = ParagraphStyle(
        'SectionHeading',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9.2,
        leading=11,
        textColor=PRIMARY,
        spaceBefore=4,
        spaceAfter=1.5,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'BodyStyle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.8,
        leading=9.8,
        textColor=DARK_TEXT
    )

    summary_style = ParagraphStyle(
        'SummaryStyle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.8,
        leading=10,
        textColor=DARK_TEXT
    )

    item_title_style = ParagraphStyle(
        'ItemTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.3,
        leading=10,
        textColor=DARK_TEXT
    )

    item_meta_style = ParagraphStyle(
        'ItemMeta',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=7.8,
        leading=10,
        textColor=MUTED_TEXT,
        alignment=2
    )

    bullet_style = ParagraphStyle(
        'BulletStyle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.6,
        leading=9.5,
        textColor=DARK_TEXT,
        leftIndent=10,
        firstLineIndent=-10
    )

    story = []

    # 1. Header
    story.append(Paragraph("MAXIMILIANO RODRIGUEZ", name_style))
    story.append(Spacer(1, 1.5))
    story.append(Paragraph("ROBOTICS ENGINEER &bull; EMBEDDED SYSTEMS &bull; AI SOLUTIONS ARCHITECT", title_style))
    story.append(Spacer(1, 1.5))
    contact_text = (
        "Puerto La Cruz, Venezuela &nbsp;|&nbsp; "
        "<b>Email:</b> maxrsilvagni@gmail.com &nbsp;|&nbsp; "
        "<b>Phone:</b> +58 412 046 6522 &nbsp;|&nbsp; "
        "<b>LinkedIn:</b> linkedin.com/in/maximilianorodriguez &nbsp;|&nbsp; "
        "<b>Studio:</b> papervortexstudio.com"
    )
    story.append(Paragraph(contact_text, contact_style))
    story.append(Spacer(1, 3))
    story.append(HRFlowable(width="100%", thickness=0.75, color=PRIMARY, spaceBefore=1, spaceAfter=3))

    # 2. Executive Summary
    story.append(Paragraph("PROFESSIONAL SUMMARY", section_heading))
    story.append(HRFlowable(width="100%", thickness=0.4, color=LINE_COLOR, spaceBefore=0, spaceAfter=2))
    summary_text = (
        "High-performance robotics engineer and software developer with 4+ years of competitive international experience. "
        "<b>Ranked #19 Worldwide (WRO 2023)</b> and selected as <b>2026 World Finalist</b> representing the Venezuelan National Delegation. "
        "Demonstrated technical expertise in embedded C++/C# architecture, autonomous multi-sensor platforms (Raspberry Pi, Arduino), "
        "and real-time signal processing. Founder of <b>Paper Vortex Studio</b>, engineering commercial AI automations, "
        "custom business web infrastructure, and interactive software systems."
    )
    story.append(Paragraph(summary_text, summary_style))
    story.append(Spacer(1, 2.5))

    # 3. Honors & International Competitions
    story.append(Paragraph("HONORS &amp; COMPETITIVE AWARDS", section_heading))
    story.append(HRFlowable(width="100%", thickness=0.4, color=LINE_COLOR, spaceBefore=0, spaceAfter=2))

    awards = [
        ("<b>World Robot Olympiad (WRO) International Finalist</b> (Panama City, Panama)", "Nov 2023",
         "Ranked <b>#19 Worldwide</b> and <b>#4 in the Americas</b> representing Venezuela; competed among elite global robotics delegations."),
        ("<b>World Robot Olympiad (WRO) International Finalist</b> (San Juan, Puerto Rico)", "2026",
         "Selected to represent Venezuela at the World Finals with the ORBIT autonomous AI social robotics system."),
        ("<b>WRO Venezuela National Championship</b> (Caracas, Venezuela)", "2024",
         "Secured a <b>Top 4 National Ranking</b> in the high-stakes senior robotics division."),
        ("<b>Kurios Robotics Championship</b> (Puerto La Cruz, Venezuela)", "2022 – 2025",
         "Awarded <b>1st Place Overall (2022, 2023)</b> and <b>2nd Place Overall (2024, 2025)</b> across 4 consecutive competition seasons.")
    ]

    for title, date, desc in awards:
        tbl = Table([
            [Paragraph(title, item_title_style), Paragraph(date, item_meta_style)]
        ], colWidths=[428, 124])
        tbl.setStyle(TableStyle([
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('LEFTPADDING', (0,0), (-1,-1), 0),
            ('RIGHTPADDING', (0,0), (-1,-1), 0),
            ('TOPPADDING', (0,0), (-1,-1), 0.3),
            ('BOTTOMPADDING', (0,0), (-1,-1), 0.3),
        ]))
        story.append(tbl)
        story.append(Paragraph(f"&bull; {desc}", bullet_style))
        story.append(Spacer(1, 1))

    story.append(Spacer(1, 1.5))

    # 4. Engineering, AI & Commercial Ventures
    story.append(Paragraph("ENGINEERING SYSTEMS &amp; COMMERCIAL VENTURES", section_heading))
    story.append(HRFlowable(width="100%", thickness=0.4, color=LINE_COLOR, spaceBefore=0, spaceAfter=2))

    projects = [
        {
            "header": ("<b>ORBIT – Autonomous Social Robot</b> | <i>Golden Codex (WRO Team)</i>", "Oct 2025 – Present"),
            "bullets": [
                "Architected an autonomous social robot on <b>Raspberry Pi 5</b> equipped with a custom 4-motor chassis and animated facial telemetry.",
                "Engineered a real-time <b>acoustic trilateration</b> localization system using 3 directional microphones to triangulate human speakers.",
                "Integrated conversational AI to guide public discourse toward culture and STEM; modeled as an interactive kiosk for museums."
            ]
        },
        {
            "header": ("<b>Founder &amp; Principal Solutions Developer</b> | <i>Paper Vortex Studio</i>", "Aug 2024 – Present"),
            "bullets": [
                "Founded a commercial technology studio delivering enterprise AI integrations, custom web architecture, and interactive software.",
                "Engineered 24/7 AI conversational automation for real estate and business sales, integrating WhatsApp APIs with live property databases for instant inventory inquiries, intelligent lead qualification, and CRM logging (papervortexstudio.com).",
                "Designs, deploys, and manages high-performance web infrastructure and automated digital workflows for emerging entrepreneurships.",
                "Directs an experimental game mechanics lab; designed procedural state machines and physics in <b>Unity (C#)</b> for <i>'The Other Side'</i>."
            ]
        },
        {
            "header": ("<b>Automated Maritime Tide Monitoring System</b> | <i>Tomorrow’s Innovators (WRO Team)</i>", "Mar 2023 – Dec 2023"),
            "bullets": [
                "Prototyped a real-time coastal flood hazard alert system on <b>Arduino UNO</b> targeting maritime safety and coral reef conservation.",
                "Programmed analog signal filters in <b>C++</b> across multi-depth submersible sensor terminals to trigger instant color-coded LED warnings.",
                "Built and demonstrated a closed-loop fluid simulation apparatus driven by automated water pumps to validate variable tidal spikes."
            ]
        },
        {
            "header": ("<b>Autonomous Seed-to-Microgreen Agricultural System</b> | <i>Tomorrow’s Innovators (WRO Team)</i>", "Jan 2024 – Dec 2024"),
            "bullets": [
                "Engineered a fully autonomous indoor agricultural robot executing an 8-day seed-to-harvest growth cycle aligned with <b>UN SDG-12</b>.",
                "Integrated Arduino UNO, Raspberry Pi 4, stepper motors, servos, and programmed timed LED grow lighting schedules in C++."
            ]
        }
    ]

    for p in projects:
        tbl = Table([
            [Paragraph(p["header"][0], item_title_style), Paragraph(p["header"][1], item_meta_style)]
        ], colWidths=[428, 124])
        tbl.setStyle(TableStyle([
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('LEFTPADDING', (0,0), (-1,-1), 0),
            ('RIGHTPADDING', (0,0), (-1,-1), 0),
            ('TOPPADDING', (0,0), (-1,-1), 0.3),
            ('BOTTOMPADDING', (0,0), (-1,-1), 0.3),
        ]))
        story.append(tbl)
        for b in p["bullets"]:
            story.append(Paragraph(f"&bull; {b}", bullet_style))
        story.append(Spacer(1, 1.5))

    story.append(Spacer(1, 1))

    # 5. Technical Skills
    story.append(Paragraph("TECHNICAL PROFICIENCIES", section_heading))
    story.append(HRFlowable(width="100%", thickness=0.4, color=LINE_COLOR, spaceBefore=0, spaceAfter=2))

    skills_data = [
        [Paragraph("<b>Programming &amp; Software:</b>", item_title_style), Paragraph("C++, C#, Python (Certified), HTML5/CSS/JavaScript, Bash/Shell Scripting, Git/GitHub", body_style)],
        [Paragraph("<b>AI &amp; Enterprise Integration:</b>", item_title_style), Paragraph("LLM API Integrations, WhatsApp Business Automation, Conversational Agents, CRM &amp; Database Sync", body_style)],
        [Paragraph("<b>Embedded Hardware &amp; IoT:</b>", item_title_style), Paragraph("Raspberry Pi (4 &amp; 5), Arduino (UNO), Steppers, Servos, Analog Sensors, Circuit Prototyping", body_style)],
        [Paragraph("<b>Core Specialties:</b>", item_title_style), Paragraph("Autonomous Robotics, Acoustic Trilateration, Real-Time Signal Processing, Full-Stack Web Infrastructure", body_style)],
    ]
    skills_tbl = Table(skills_data, colWidths=[135, 417])
    skills_tbl.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
        ('TOPPADDING', (0,0), (-1,-1), 0.3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 0.3),
    ]))
    story.append(skills_tbl)
    story.append(Spacer(1, 2.5))

    # 6. Education, Certifications & Athletics
    story.append(Paragraph("EDUCATION, TRAINING &amp; ATHLETICS", section_heading))
    story.append(HRFlowable(width="100%", thickness=0.4, color=LINE_COLOR, spaceBefore=0, spaceAfter=2))

    edu_tbl = Table([
        [Paragraph("<b>Colegio &Iacute;talo Venezolano 'Angelo De Marta'</b> &mdash; High School Diploma", item_title_style),
         Paragraph("Expected June 2027", item_meta_style)]
    ], colWidths=[428, 124])
    edu_tbl.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
        ('TOPPADDING', (0,0), (-1,-1), 0.3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 0.3),
    ]))
    story.append(edu_tbl)
    story.append(Paragraph("&bull; <b>Academic Standing:</b> 10th Grade (Sophomore). Consistent top-tier academic marks in Mathematics, Physics, and Chemistry.", bullet_style))
    story.append(Paragraph("&bull; <b>Supplemental Technical Training:</b> Kurios Academy (Robotics &amp; Strategy, 2022&ndash;Pres.); Tech Academy (Advanced Prototyping, 2025&ndash;Pres.); ADAKADEMY (Python Certification, 2022).", bullet_style))
    story.append(Paragraph("&bull; <b>Athletics &amp; Discipline:</b> Angelo Escudero Taekwondo Academy (2018&ndash;Pres.) &mdash; <b>Red Belt with 1 Black Stripe</b>; 8 consecutive years of competitive training.", bullet_style))
    story.append(Paragraph("&bull; <b>Languages:</b> Spanish (Native), English (C1 &ndash; Advanced Professional Proficiency), French (A2 &ndash; Elementary).", bullet_style))

    # Build
    doc.build(story, canvasmaker=NumberedCanvas)

if __name__ == "__main__":
    build_pdf()
