from django.shortcuts import render

from mango.models import MangoProduct, MangoProductFile


def index(request):
    mango_products = MangoProduct.objects.all()
    return render(request, "index.html", {"products": mango_products})


def view_product_data_files(request, id):
    files = MangoProductFile.objects.filter(mango_product_id=id)
    return render(
        request,
        "view_product.html",
        {
            "files": files,
            "product_id": id,
        },
    )


def label_data_file(request, product_id, id):
    return render(request, "label_data_file.html")
