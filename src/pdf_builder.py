"""
Module de construction du rapport PDF avec ReportLab.
"""
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                                 TableStyle, Image, PageBreak, HRFlowable)
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from datetime import datetime
import io


BRAND_BLUE = colors.HexColor('#1565C0')
BRAND_LIGHT = colors.HexColor('#E3F2FD')
BRAND_GRAY = colors.HexColor('#546E7A')


def build_pdf(output_path: str, title: str, df, stats: dict,
              insights: list, charts: dict) -> None:
    """Construit le rapport PDF complet."""
    doc = SimpleDocTemplate(output_path, pagesize=A4,
                            leftMargin=2*cm, rightMargin=2*cm,
                            topMargin=2*cm, bottomMargin=2*cm)
    styles = getSampleStyleSheet()
    story = []

    # ── Styles personnalisés ──────────────────────────────────────────────────
    h1 = ParagraphStyle('H1', parent=styles['Heading1'],
                         fontSize=22, textColor=BRAND_BLUE,
                         spaceAfter=12, alignment=TA_CENTER)
    h2 = ParagraphStyle('H2', parent=styles['Heading2'],
                         fontSize=14, textColor=BRAND_BLUE, spaceAfter=8)
    body = ParagraphStyle('Body', parent=styles['Normal'],
                           fontSize=10, leading=16, textColor=BRAND_GRAY)
    caption = ParagraphStyle('Caption', parent=styles['Normal'],
                              fontSize=8, textColor=colors.gray, alignment=TA_CENTER)

    # ── Page de garde ─────────────────────────────────────────────────────────
    story.append(Spacer(1, 3*cm))
    story.append(Paragraph(title, h1))
    story.append(HRFlowable(width='100%', color=BRAND_BLUE, thickness=2))
    story.append(Spacer(1, 0.5*cm))
    story.append(Paragraph(f"Rapport généré le {datetime.now().strftime('%d/%m/%Y à %H:%M')}",
                            caption))
    story.append(Spacer(1, 0.5*cm))
    story.append(Paragraph(
        f"<b>{len(df):,} lignes</b> · <b>{len(df.columns)} colonnes</b> · "
        f"<b>{len(stats)} variables numériques analysées</b>", body))
    story.append(PageBreak())

    # ── Synthèse exécutive ────────────────────────────────────────────────────
    story.append(Paragraph("📋 Synthèse Exécutive", h2))
    for insight in insights:
        story.append(Paragraph(f"• {insight}", body))
        story.append(Spacer(1, 0.2*cm))
    story.append(Spacer(1, 0.5*cm))

    # ── Statistiques descriptives ─────────────────────────────────────────────
    story.append(Paragraph("📊 Statistiques Descriptives", h2))
    headers = ['Variable', 'Nb obs.', 'Moyenne', 'Médiane', 'Écart-type', 'Min', 'Max']
    table_data = [headers]
    for col, s in stats.items():
        table_data.append([col, f"{s['count']:,}", f"{s['mean']:,.2f}",
                           f"{s['median']:,.2f}", f"{s['std']:,.2f}",
                           f"{s['min']:,.2f}", f"{s['max']:,.2f}"])
    t = Table(table_data, hAlign='LEFT')
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), BRAND_BLUE),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 9),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, BRAND_LIGHT]),
        ('GRID', (0,0), (-1,-1), 0.5, colors.lightgrey),
        ('ALIGN', (1,0), (-1,-1), 'RIGHT'),
        ('PADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t)
    story.append(PageBreak())

    # ── Graphiques ────────────────────────────────────────────────────────────
    for chart_name, chart_bytes in charts.items():
        if chart_bytes:
            story.append(Paragraph(f"📈 {chart_name}", h2))
            img = Image(io.BytesIO(chart_bytes), width=16*cm, height=10*cm)
            story.append(img)
            story.append(Spacer(1, 0.5*cm))

    # ── Pied de page ──────────────────────────────────────────────────────────
    story.append(Spacer(1, 1*cm))
    story.append(HRFlowable(width='100%', color=BRAND_GRAY, thickness=0.5))
    story.append(Paragraph("Rapport généré par Harry TEGUE — Data Analyst · harrytegue@gmail.com", caption))

    doc.build(story)
    print(f"  ✅ Rapport PDF généré : {output_path}")
