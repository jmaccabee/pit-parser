from django.shortcuts import render

from mango.models import MangoProduct


def index(request):
    mango_products = MangoProduct.objects.all()
    return render(request, "index.html", {"products": mango_products})


def view_product_data_files(request, id):
    return render(request, "view_product.html", {"id": id})
