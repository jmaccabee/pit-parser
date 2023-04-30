from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.urls import reverse_lazy

from mango.models import MangoProduct, MangoProductFile, MangoProductAnnotation
from parser_backend.models import ExtractedPitData, ProcessedPitData
from parser_backend.forms import AnnotationForm

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


class AnnotateDataFileCreateView(CreateView):
    template_name = "annotate_data_file.html"
    form_class = AnnotationForm

    def get_context_data(self, **kwargs):
        context = super(AnnotateDataFileCreateView, self).get_context_data(**kwargs)
        mango_product_file_id = context["view"].kwargs["mango_product_file_id"]
        mango_product_id = context["view"].kwargs["mango_product_id"]

        next_timeseries_id_to_annotate = (
            ExtractedPitData.objects.filter(
                mango_product_file__id=mango_product_file_id
            )
            .filter(annotated=False)
            .values("timeseries_id")
            .distinct()
            .first()
        )["timeseries_id"]
        timeseries_to_annotate = (
            ExtractedPitData.objects.filter(
                mango_product_file__id=mango_product_file_id
            ).filter(timeseries_id=next_timeseries_id_to_annotate)
        )[:5]

        first_datapoint = timeseries_to_annotate[0]
        date_strings = sorted(
            [
                datapoint.date.strftime("%Y-%m-%d")
                for datapoint in timeseries_to_annotate
            ]
        )
        values = [datapoint.raw_value for datapoint in timeseries_to_annotate]

        mango_annotations = MangoProductAnnotation.objects.filter(
            mango_product_id=mango_product_id
        ).order_by("field_value")
        metric_names = [
            a.field_value
            for a in mango_annotations
            if a.field_label == MangoProductAnnotation.METRIC_NAME
        ]
        slice_names = [
            a.field_value
            for a in mango_annotations
            if a.field_label == MangoProductAnnotation.SLICE_NAME
        ]
        context.update(
            {
                "section_header_1": first_datapoint.section_header_1,
                "section_header_2": first_datapoint.section_header_2,
                "raw_analysis_name": first_datapoint.raw_analysis_name,
                "slice_value": first_datapoint.slice_value,
                "dates": date_strings,
                "values": values,
                "metric_names": metric_names,
                "slice_names": slice_names,
                "mango_product_id": mango_product_id,
                "mango_product_file_id": mango_product_file_id,
                "timeseries_id": next_timeseries_id_to_annotate,
            }
        )

        return context


class AnnotateDataFileUpdateView(UpdateView):
    model = ProcessedPitData
    template_name = "annotate_data_file.html"
    form_class = AnnotationForm


class AnnotateDataFileDeleteView(DeleteView):
    model = ProcessedPitData
    success_url = reverse_lazy("create_annotate_data_file")
    template_name = "annotate_data_file.html"
    form_class = AnnotationForm


def skip_annotation(
    request,
    mango_product_id,
    mango_product_file_id,
    timeseries_id,
):
    ExtractedPitData.objects.filter(
        mango_product_file_id=mango_product_file_id,
        timeseries_id=timeseries_id,
    ).update(annotated=ExtractedPitData.SKIPPED)
    return redirect(
        "create_annotate_data_file",
        mango_product_id=mango_product_id,
        mango_product_file_id=mango_product_file_id,
    )
