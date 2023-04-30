from django import forms
from django.db.models import Q
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
    model = ProcessedPitData

    # def get(self, request, *args, **kwargs):
    #     mango_product_id = kwargs['mango_product_id']
    #     metrics = [
    #         (record, record)
    #         for record in (
    #             MangoProductAnnotation.objects
    #                 .filter(mango_product=mango_product_id)
    #                 .filter(field_label=MangoProductAnnotation.METRIC_NAME)
    #                 .values_list("field_value")
    #                 .distinct()
    #         )
    #     ]
    #     slices = [
    #         (record, record)
    #         for record in (
    #             MangoProductAnnotation.objects
    #                 .filter(mango_product=mango_product_id)
    #                 .filter(field_label=MangoProductAnnotation.SLICE_NAME)
    #                 .values_list("field_value")
    #                 .distinct()
    #         )
    #     ]
    #     import pdb; pdb.set_trace()
    #     form = self.get_form()
    #     form.fields['metric_label'] = forms.ChoiceField(choices=metrics)
    #     form.fields['slice_label'] = forms.ChoiceField(choices=slices)
    #     return super(AnnotateDataFileCreateView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        mango_product_file_id = self.kwargs["mango_product_file_id"]
        timeseries_id = self.request.POST["timeseries_id"]
        ExtractedPitData.objects.filter(
            mango_product_file_id=mango_product_file_id,
            timeseries_id=timeseries_id,
        ).update(annotated=ExtractedPitData.ANNOTATED)
        return super(AnnotateDataFileCreateView, self).post(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(AnnotateDataFileCreateView, self).get_context_data(**kwargs)
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
                "timeseries_id": timeseries_id,
            }
        )
        return context

    def get_initial(self):
        mango_product_file_id = self.kwargs["mango_product_file_id"]
        mango_product_id = self.kwargs["mango_product_id"]
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

        self.initial.update(
            {
                "mango_product_file": mango_product_file_id,
                "timeseries_id": timeseries_id,
                "value_scaler": 0,
            }
        )
        return self.initial

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
