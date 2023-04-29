from django.http import HttpResponse
from django.shortcuts import render
from django.views import View

from mango.models import MangoProduct, MangoProductFile

import pandas as pd


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


class LabelDataFileView(View):
    template_name = "label_data_file.html"

    def get(self, request, product_id, id):
        # TO DO - COMPLETE VIEW
        # data_file = MangoProductFile.objects.get(id=id).data_file

        return render(request, "label_data_file.html")
