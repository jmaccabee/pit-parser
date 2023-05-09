import re

from django import forms
from django.db.models import Q, Count
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.urls import reverse, reverse_lazy

from mango.models import MangoProduct, MangoProductFile, MangoProductAnnotation
from parser_backend.models import ExtractedPitData, ProcessedPitData
from parser_backend.forms import AnnotationForm

import pandas as pd


def index(request):
    mango_products = MangoProduct.objects.all()
    return render(request, "index.html", {"products": mango_products})


def remaining_view(request):
    remaining_annotations = (
        ExtractedPitData.objects.values(
            "mango_product_file__mango_product__name",
            "mango_product_file__mango_product_id",
            "annotated",
        )
        .annotate(distinct_timeseries=Count("timeseries_id", distinct=True))
        .order_by("mango_product_file__mango_product__name", "annotated")
    )
    return render(request, "remaining.html", {"annotations": remaining_annotations})


def view_product_data_files(request, id):
    files = MangoProductFile.objects.filter(mango_product_id=id).order_by("id")
    file_ids = [f.id for f in files]
    timeseries_annotations = (
        ExtractedPitData.objects.filter(mango_product_file_id__in=file_ids)
        .values("mango_product_file_id", "annotated")
        .annotate(distinct_timeseries=Count("timeseries_id", distinct=True))
        .order_by("mango_product_file_id", "annotated")
    )
    annotation_display_names = {
        choice[0]: choice[1]
        for choice in ExtractedPitData.annotated.field.get_choices()[1:]
    }
    data_file_context = {}
    for status in timeseries_annotations:
        if not status["mango_product_file_id"] in data_file_context.keys():
            data_file_context[status["mango_product_file_id"]] = []
        context = data_file_context[status["mango_product_file_id"]]
        context.append(
            (
                annotation_display_names[status["annotated"]],
                status["distinct_timeseries"],
            )
        )
    return render(
        request,
        "view_product.html",
        {
            "files": files,
            "data_file_context": data_file_context,
            "product_id": id,
        },
    )


class AnnotateDataFileCreateView(CreateView):
    template_name = "annotate_data_file.html"
    form_class = AnnotationForm
    model = ProcessedPitData

    def post(self, request, *args, **kwargs):
        mango_product_file_id = self.kwargs["mango_product_file_id"]
        timeseries_id = self.request.POST["timeseries_id"]
        ExtractedPitData.objects.filter(
            mango_product_file_id=mango_product_file_id,
            timeseries_id=timeseries_id,
        ).update(annotated=ExtractedPitData.ANNOTATED)
        return super().post(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        mango_product_file_id = context["view"].kwargs["mango_product_file_id"]
        mango_product_id = context["view"].kwargs["mango_product_id"]

        next_timeseries_id_to_annotate = (
            ExtractedPitData.objects.filter(
                mango_product_file__id=mango_product_file_id
            )
            .exclude(annotated=ExtractedPitData.ANNOTATED)
            .order_by("annotated")
            .values("timeseries_id")
            .distinct()
            .first()
        )
        if not next_timeseries_id_to_annotate:
            return redirect(
                "annotation_complete",
                mango_product_id=mango_product_id,
                mango_product_file_id=mango_product_file_id,
            )

        timeseries_id = next_timeseries_id_to_annotate["timeseries_id"]

        timeseries_to_annotate = (
            ExtractedPitData.objects.filter(
                mango_product_file__id=mango_product_file_id
            )
            .filter(timeseries_id=timeseries_id)
            .exclude(Q(raw_value="-") | Q(raw_value="nan"))
        )[:5:-1]

        first_datapoint = timeseries_to_annotate[0]
        raw_analysis_name = first_datapoint.raw_analysis_name
        slice_value = first_datapoint.slice_value
        section_header_1 = first_datapoint.section_header_1
        section_header_2 = first_datapoint.section_header_2

        date_strings = [
            datapoint.date.strftime("%Y-%m-%d") for datapoint in timeseries_to_annotate
        ]
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
        empty_choice = [("", "---------")]
        metric_choices = empty_choice + [(metric, metric) for metric in metric_names]
        slice_choices = empty_choice + [
            (slice_name, slice_name) for slice_name in slice_names
        ]
        context.update(
            {
                "section_header_1": section_header_1,
                "section_header_2": section_header_2,
                "raw_analysis_name": raw_analysis_name,
                "slice_value": slice_value,
                "dates": date_strings,
                "values": values,
                "metric_names": metric_names,
                "slice_names": slice_names,
                "mango_product_id": mango_product_id,
                "mango_product_file_id": mango_product_file_id,
                "timeseries_id": timeseries_id,
            }
        )
        context["form"].fields["metric_label"] = forms.ChoiceField(
            choices=metric_choices,
            widget=forms.Select(
                attrs={
                    "class": (
                        "bg-gray-50 border border-gray-300 text-gray-900 "
                        "text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 "
                        "block w-full p-2.5 dark:bg-gray-600 dark:border-gray-500 "
                        "dark:placeholder-gray-400 dark:text-white"
                    )
                }
            ),
        )
        context["form"].fields["slice_label"] = forms.ChoiceField(
            choices=slice_choices,
            widget=forms.Select(
                attrs={
                    "class": (
                        "bg-gray-50 border border-gray-300 text-gray-900 "
                        "text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 "
                        "block w-full p-2.5 dark:bg-gray-600 dark:border-gray-500 "
                        "dark:placeholder-gray-400 dark:text-white"
                    )
                }
            ),
        )

        # move to helper functions
        value_scaler = 0
        if re.search("\\(\\$?mm\\)", slice_value.lower()) or re.search(
            "\\(\\$?mm\\)", raw_analysis_name.lower()
        ):
            value_scaler = 1000000
        elif re.search("thousand", slice_value.lower()) or re.search(
            "thousand", raw_analysis_name.lower()
        ):
            value_scaler = 1000

        # move to helper functions
        first_date_obj = timeseries_to_annotate[0]
        second_date_obj = timeseries_to_annotate[1]
        if "q" in first_date_obj.raw_date.lower():
            periodicity = ProcessedPitData.QUARTERLY
        else:
            first_date = first_date_obj.date
            second_date = second_date_obj.date
            delta = abs(second_date - first_date).days
            if delta > 30:
                periodicity = ProcessedPitData.YEARLY
            elif delta > 7:
                periodicity = ProcessedPitData.MONTHLY
            elif delta > 1:
                periodicity = ProcessedPitData.WEEKLY
            else:
                periodicity = ProcessedPitData.DAILY
        context["form"].initial.update(
            {
                "metric_field": "raw_analysis_name",
                "slice_field": "slice_value",
                "periodicity": periodicity,
                "mango_product_file": mango_product_file_id,
                "timeseries_id": timeseries_id,
                "value_scaler": value_scaler,
            }
        )
        return context

    def get_success_url(self):
        return reverse(
            "create_annotate_data_file",
            kwargs={
                "mango_product_id": self.object.mango_product_file.mango_product_id,
                "mango_product_file_id": self.object.mango_product_file_id,
            },
        )


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


def annotation_complete(request, mango_product_id, mango_product_file_id):
    return render(request, "labels_complete.html")
