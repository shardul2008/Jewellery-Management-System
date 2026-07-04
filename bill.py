from io import BytesIO
from datetime import datetime

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)

from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.units import inch


def generate_bill(data):

    buffer = BytesIO()

    doc = SimpleDocTemplate(buffer)

    styles = getSampleStyleSheet()

    title = styles["Title"]
    title.alignment = TA_CENTER

    heading = styles["Heading2"]
    normal = styles["BodyText"]

    story = []

    # Shop Name
    story.append(Paragraph("BILL", title))
    story.append(Paragraph("Premium Gold & Silver Jewellery", normal))
    story.append(Spacer(1, 15))

    # Invoice Details
    story.append(
        Paragraph(
            f"<b>Invoice No:</b> {data['ID']}",
            normal
        )
    )

    story.append(
        Paragraph(
            f"<b>Date:</b> {datetime.now().strftime('%d-%m-%Y')}",
            normal
        )
    )

    story.append(Spacer(1, 15))

    # Table
    table_data = [

        ["Item", data["Name"]],

        ["Metal", data["Metal"]],

        ["Purity", data["Purity"]],

        ["Weight", f"{data['Weight']} gm"],

        ["Making Charges", f"{data['Making']}/-"],

        ["GST", f"{data['GST']} %"],

        ["Other Charges", f" {data['Other']}/-"],

        ["Total Price", f" {data['final_price']}/-"]

    ]

    table = Table(table_data, colWidths=[2.3*inch,3*inch])

    table.setStyle(TableStyle([

        ("BACKGROUND",(0,0),(-1,-1),colors.beige),

        ("TEXTCOLOR",(0,0),(-1,-1),colors.black),

        ("GRID",(0,0),(-1,-1),1,colors.lightgrey),

        #("BACKGROUND",(1,0),(1,-1),colors.whitesmoke),

        ("BOTTOMPADDING",(0,0),(-1,-1),10),

        ("TOPPADDING",(0,0),(-1,-1),10),

        ("FONTNAME",(0,0),(0,-1),"Helvetica-Bold"),

        ("FONTNAME",(1,0),(1,-1),"Helvetica"),

        ("BOX",(0,0),(-1,-1),0.5, colors.grey),

        ("VALGIN",(0,0),(-1,-1),"MIDDLE")

    ]))

    story.append(table)

    story.append(Spacer(1,20))

    story.append(
        Paragraph(
            "<b>Thank You For Shopping With Us!</b>",
            heading
        )
    )

    story.append(
        Paragraph(
            "Visit Again",
            normal
        )
    )

    story.append(Spacer(1,10))

    story.append(
        Paragraph(
            "Address: Pune, Maharashtra",
            normal
        )
    )

    story.append(
        Paragraph(
            "+91 9876543210",
            normal
        )
    )

    doc.build(story)

    buffer.seek(0)

    return buffer