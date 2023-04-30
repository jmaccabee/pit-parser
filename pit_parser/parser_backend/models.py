import datetime

from django.db import models

from base.models import BaseModel
from mango.models import MangoProductFile


class ExtractedPitData(BaseModel):
    UNANNOTATED = 1
    SKIPPED = 2
    ANNOTATED = 3
    ANNOTATION_CHOICES = [
        (UNANNOTATED, "Unannotated"),
        (SKIPPED, "Skipped"),
        (ANNOTATED, "Annotated"),
    ]

    mango_product_file = models.ForeignKey(MangoProductFile, on_delete=models.CASCADE)
    raw_analysis_name = models.CharField(max_length=1024)
    slice_value = models.CharField(max_length=1024)
    section_header_1 = models.CharField(max_length=1024)
    section_header_2 = models.CharField(max_length=1024)
    source_sheet_name = models.CharField(max_length=1024)
    source_data_file_name = models.CharField(max_length=1024)
    raw_date = models.CharField(max_length=32)
    raw_value = models.CharField(max_length=32)
    timeseries_id = models.UUIDField()
    annotated = models.IntegerField(choices=ANNOTATION_CHOICES, default=1)

    @property
    def date(self):
        try:
            return datetime.datetime.strptime(self.raw_date, "%m/%d/%y")
        except Exception:
            return self.raw_date


class ProcessedPitData(BaseModel):
    RAW_ANALYSIS_NAME = "raw_analysis_name"
    SLICE_VALUE = "slice_value"
    SECTION_HEADER_1 = "section_header_1"
    SECTION_HEADER_2 = "section_header_2"

    FIELD_CHOICES = [
        (RAW_ANALYSIS_NAME, "raw_analysis_name"),
        (SLICE_VALUE, "slice_value"),
        (SECTION_HEADER_1, "section_header_1"),
        (SECTION_HEADER_2, "section_header_2"),
    ]

    DAILY = "daily"
    WEEKLY = "week"
    MONTHLY = "month"
    QUARTERLY = "quarter"
    YEARLY = "year"

    PERIODICITY_CHOICES = [
        (DAILY, "daily"),
        (WEEKLY, "week"),
        (MONTHLY, "month"),
        (QUARTERLY, "quarter"),
        (YEARLY, "year"),
    ]

    metric_field = models.CharField(max_length=32, choices=FIELD_CHOICES)
    metric_label = models.CharField(max_length=1024)
    value_scaler = models.DecimalField(max_digits=20, decimal_places=2)
    slice_field = models.CharField(max_length=32, choices=FIELD_CHOICES)
    slice_label = models.CharField(max_length=1024)
    periodicity = models.CharField(max_length=32, choices=PERIODICITY_CHOICES)
    period_end_time_delta = models.SmallIntegerField()
    dates_start_period = models.BooleanField(default=False)

    mango_product_file = models.ForeignKey(MangoProductFile, on_delete=models.CASCADE)
    timeseries_id = models.UUIDField(unique=True)
