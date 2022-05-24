import os

from django.http.response import HttpResponse

from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

from ingredients_recipes.models import IngredientInRecipe


def get_pdf_file(data, response):
    page = canvas.Canvas(response, pagesize=A4)

    djvsans_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), 'DejaVuSans.ttf'
    )
    pdfmetrics.registerFont(TTFont('DejaVuSans', djvsans_path))
    page.setFont('DejaVuSans', 20)
    page.drawString(130, 600, 'Список покупок:')
    page.setFont('DejaVuSans', 16)
    height = 550

    for name, quantity in data.items():
        page.drawString(
            40,
            height,
            '•  {} - {} {}'.format(
                name, quantity['amount'], quantity['measurement_unit']
            )
        )
        height -= 25
    page.showPage()
    page.save()


def get_download_shopping_cart(self, request):
    shopping_list_data = IngredientInRecipe.objects.filter(
        recipe__shopping_cart__user=request.user
    )
    shopping_list = {}
    for item in shopping_list_data:
        name = item.ingredient.name
        measurement_unit = item.ingredient.measurement_unit
        amount = item.amount
        if name not in shopping_list:
            shopping_list[name] = {
                'measurement_unit': measurement_unit,
                'amount': amount
            }
        else:
            shopping_list[name]['amount'] += amount

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = ('attachment; '
                                       'filename="shopping_list.pdf"')

    get_pdf_file(shopping_list, response)

    return response
