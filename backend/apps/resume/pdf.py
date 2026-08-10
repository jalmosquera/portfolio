from io import BytesIO
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    Image,
    ListFlowable,
    ListItem,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)
from apps.projects.models import Project


ACCENT = colors.HexColor("#F17D34")
CYAN = colors.HexColor("#35A9D3")
OFF_WHITE = colors.HexColor("#F4F1EE")
MUTED = colors.HexColor("#B4ADA7")
INK = colors.HexColor("#171717")
ASSET_DIR = Path(__file__).resolve().parent / "assets"


def translated(instance, field, language, fallback=""):
    value = instance.safe_translation_getter(field, language_code=language, any_language=True)
    return value or fallback


def paragraph(text, style):
    return Paragraph((text or "").replace("\n", "<br/>"), style)


def section_title(text, style, dark=False):
    title = Table([[Paragraph(text.upper(), style)]], colWidths=[None])
    title.setStyle(TableStyle([
        ("LINEBELOW", (0, 0), (-1, -1), 1, ACCENT if dark else INK),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6 if dark else 3),
    ]))
    return title


def icon_flowable(icon_name, size=11):
    if not icon_name:
        return Spacer(size, size)
    path = ASSET_DIR / "icons" / f"{Path(icon_name).stem}.png"
    if not path.exists():
        return Spacer(size, size)
    return Image(str(path), width=size, height=size, kind="proportional")


def project_rows(language, body, small):
    rows = []
    for project in Project.objects.filter(visible=True).order_by("created_at")[:4]:
        content = getattr(project, "localized_content", None)
        title = project.title
        description = project.short_description
        if content:
            title = translated(content, "title", language, title)
            description = translated(content, "short_description", language, description)
        links = []
        if project.github:
            links.append(f'<link href="{project.github}" color="#35A9D3">GitHub</link>')
        if project.live_url:
            links.append(f'<link href="{project.live_url}" color="#35A9D3">Demo</link>')
        rows.extend([
            Paragraph(f"<b>{title}</b>", body),
            Paragraph(description, small),
            Paragraph(" · ".join(links), small) if links else Spacer(1, 1),
            Spacer(1, 8 if body.fontSize > 9 else 4),
        ])
    return rows


def styles_for(visual):
    base = getSampleStyleSheet()
    foreground = OFF_WHITE if visual else INK
    secondary = MUTED if visual else colors.HexColor("#333333")
    return {
        "name": ParagraphStyle("Name", parent=base["Title"], fontName="Helvetica-Bold", fontSize=30 if visual else 18, leading=33 if visual else 21, textColor=foreground, alignment=TA_LEFT),
        "headline": ParagraphStyle("Headline", parent=base["Normal"], fontName="Helvetica", fontSize=13 if visual else 9, leading=17 if visual else 12, textColor=foreground),
        "contact": ParagraphStyle("Contact", parent=base["Normal"], fontName="Helvetica", fontSize=9.2 if visual else 7.5, leading=12.5 if visual else 10, textColor=CYAN if visual else INK),
        "section": ParagraphStyle("Section", parent=base["Heading2"], fontName="Helvetica-Bold", fontSize=14 if visual else 10.5, leading=17 if visual else 13, textColor=ACCENT if visual else INK, spaceBefore=3),
        "body": ParagraphStyle("Body", parent=base["Normal"], fontName="Helvetica", fontSize=10.7 if visual else 8, leading=13.8 if visual else 10.5, textColor=foreground, alignment=TA_JUSTIFY),
        "small": ParagraphStyle("Small", parent=base["Normal"], fontName="Helvetica", fontSize=9.2 if visual else 7.2, leading=11.8 if visual else 9, textColor=secondary, alignment=TA_JUSTIFY),
    }


def build_resume_pdf(resume, variant, language):
    visual = variant == "visual"
    labels = {
        "es": {"profile": "Perfil", "skills": "Competencias", "experience": "Experiencia profesional", "projects": "Proyectos", "education": "Formación"},
        "en": {"profile": "Profile", "skills": "Core skills", "experience": "Professional experience", "projects": "Projects", "education": "Education"},
    }[language]
    styles = styles_for(visual)
    content = resume.content
    buffer = BytesIO()
    margin = 13 * mm if visual else 17 * mm
    document = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=margin,
        leftMargin=margin,
        topMargin=margin,
        bottomMargin=margin,
        title=f"{resume.name} CV",
        author=resume.name,
    )

    def page_background(canvas, doc):
        canvas.saveState()
        canvas.setFillColor(colors.black if visual else colors.white)
        canvas.rect(0, 0, A4[0], A4[1], stroke=0, fill=1)
        canvas.restoreState()

    contact = [resume.email, resume.phone, resume.linkedin_url, resume.github_url]
    contact_html = "<br/>".join(item for item in contact if item)
    header_text = [
        Paragraph(resume.name, styles["name"]),
        Paragraph(translated(content, "headline", language), styles["headline"]),
        Spacer(1, 4),
        Paragraph(contact_html, styles["contact"]),
    ]
    portrait_path = Path(resume.portrait.path) if resume.portrait else ASSET_DIR / "portrait.jpg"
    if visual and portrait_path.exists():
        portrait = Image(str(portrait_path), width=54 * mm, height=54 * mm, kind="proportional")
        header = Table([[portrait, header_text]], colWidths=[62 * mm, 118 * mm], hAlign="LEFT")
        header.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("LEFTPADDING", (0, 0), (-1, -1), 0), ("RIGHTPADDING", (0, 0), (-1, -1), 3 * mm), ("TOPPADDING", (0, 0), (-1, -1), 0), ("BOTTOMPADDING", (0, 0), (-1, -1), 0)]))
    else:
        header = Table([[header_text]], colWidths=[176 * mm], hAlign="CENTER")
        header.setStyle(TableStyle([("ALIGN", (0, 0), (-1, -1), "CENTER"), ("LEFTPADDING", (0, 0), (-1, -1), 0), ("RIGHTPADDING", (0, 0), (-1, -1), 0)]))

    section_gap = 12 if visual else 7
    story = [header, Spacer(1, section_gap), section_title(labels["profile"], styles["section"], visual), Spacer(1, 4 if visual else 0), paragraph(translated(content, "profile", language), styles["body"])]
    highlights = [translated(item, "text", language) for item in resume.highlights.all()]
    if highlights:
        story.extend([Spacer(1, 6 if visual else 3), ListFlowable([ListItem(Paragraph(item, styles["body"])) for item in highlights], bulletType="bullet", bulletColor=ACCENT if visual else INK, leftIndent=14, bulletFontSize=6, spaceAfter=3 if visual else 0)])
    story.append(Spacer(1, 14 if visual else 7))

    skill_rows = [[icon_flowable(skill.icon_name), Paragraph(skill.name, styles["body"])] for skill in resume.skills.all()]
    skills = Table(skill_rows, colWidths=[7 * mm, 50 * mm], hAlign="LEFT")
    skill_padding = 4.2 if visual else 1.2
    skills.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("LEFTPADDING", (0, 0), (-1, -1), 0), ("RIGHTPADDING", (0, 0), (-1, -1), 1), ("TOPPADDING", (0, 0), (-1, -1), skill_padding), ("BOTTOMPADDING", (0, 0), (-1, -1), skill_padding)]))

    education_flow = []
    for education in resume.education.all():
        education_flow.extend([
            Paragraph(f'<b>{translated(education, "institution", language)}</b>', styles["body"]),
            Paragraph(translated(education, "qualification", language), styles["small"]),
            Paragraph(" · ".join(filter(None, [translated(education, "location", language), education.period])), styles["small"]),
            Spacer(1, 4),
        ])

    experience_flow = []
    for experience in resume.experiences.all():
        experience_flow.extend([
            Paragraph(f'<b>{experience.company}</b> · {translated(experience, "role", language)}', styles["body"]),
            Paragraph(" · ".join(filter(None, [experience.period, translated(experience, "location", language)])), styles["small"]),
        ])
        summary = translated(experience, "summary", language)
        if summary:
            experience_flow.append(Paragraph(summary, styles["small"]))
        bullets = [translated(item, "text", language) for item in experience.bullets.all()]
        if bullets:
            experience_flow.append(ListFlowable([ListItem(Paragraph(item, styles["small"])) for item in bullets], bulletType="bullet", leftIndent=11, bulletFontSize=4))
        experience_flow.append(Spacer(1, 10 if visual else 5))

    if visual:
        left = [section_title(labels["skills"], styles["section"], True), Spacer(1, 4), skills]
        right = [section_title(labels["experience"], styles["section"], True), Spacer(1, 4), *experience_flow, Spacer(1, 12), section_title(labels["projects"], styles["section"], True), Spacer(1, 4), *project_rows(language, styles["body"], styles["small"])]
        columns = Table([[left, right]], colWidths=[61 * mm, 115 * mm], hAlign="LEFT")
        columns.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"), ("LEFTPADDING", (0, 0), (-1, -1), 0), ("RIGHTPADDING", (0, 0), (0, -1), 5 * mm), ("RIGHTPADDING", (1, 0), (1, -1), 0), ("TOPPADDING", (0, 0), (-1, -1), 0), ("BOTTOMPADDING", (0, 0), (-1, -1), 0)]))
        story.extend([
            columns,
            Spacer(1, 18),
            section_title(labels["education"], styles["section"], True),
            Spacer(1, 5),
            *education_flow,
        ])
    else:
        story.extend([section_title(labels["experience"], styles["section"]), *experience_flow, section_title(labels["projects"], styles["section"]), *project_rows(language, styles["body"], styles["small"]), section_title(labels["skills"], styles["section"]), skills, Spacer(1, 5), section_title(labels["education"], styles["section"]), *education_flow])

    document.build(story, onFirstPage=page_background, onLaterPages=page_background)
    buffer.seek(0)
    return buffer
