import datetime

from django.db import models

from base.models import BaseModel
from mango.models import MangoProductFile


class ExtractedPitData(BaseModel):
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
    annotated = models.BooleanField(default=False)

    @property
    def date(self):
        try:
            return datetime.datetime.strptime(self.raw_date, "%m/%d/%y")
        except Exception:
            return self.raw_date


# class ProcessedPitData(BaseModel):
#     extracted_pit_datapoint = models.ForeignKey(ExtractedPitData, on_delete=models.CASCADE)
