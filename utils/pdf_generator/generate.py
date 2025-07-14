import arabic_reshaper
from bidi.algorithm import get_display
from django.http import FileResponse
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from io import BytesIO
from apps.account_module.models import SubUser
from django.conf import settings
from apps.home_module.models import SettingSite


def reshape_text(text):
    return get_display(arabic_reshaper.reshape(text))


def generate_pdf_file(insurance_code, items):
    buffer = BytesIO()
    pdfmetrics.registerFont(TTFont("Vazir", settings.FONT_PATH))
    p = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    p.setFont("Vazir", 18)

    # عنوان
    if SettingSite.objects.exists():
        setting = SettingSite.objects.first()
        p.drawCentredString(
            width / 2, height - 50, reshape_text(f"سامانه {setting.name}")
        )
    else:
        p.drawCentredString(width / 2, height - 50, reshape_text("سامانه بیمه زائر"))

    p.setFont("Vazir", 14)
    p.drawCentredString(
        width / 2,
        height - 80,
        reshape_text(
            f"لیست زیرمجموعه‌های بیمه : {insurance_code}"
            if insurance_code != None
            else "لیست زیر مجموعه ها"
        ),
    )

    y = height - 130
    counter = 1
    subs = items

    for sub in subs:

        if y < 100:
            p.showPage()
            p.setFont("Vazir", 14)
            y = height - 100

        p.drawRightString(
            width - 50,
            y,
            reshape_text(f"{counter} - نام و نام خانوادگی: {sub.full_name}"),
        )
        p.drawRightString(
            width - 50, y - 40, reshape_text(f"کد ملی: {sub.national_code}")
        )

        p.setStrokeColor(colors.grey)
        p.setLineWidth(0.5)
        p.line(50, y - 50, width - 50, y - 50)
        y -= 80
        counter += 1

    p.showPage()
    p.save()
    buffer.seek(0)
    return buffer
