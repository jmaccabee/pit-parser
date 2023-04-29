from django.db import models

from base.models import BaseModel
from mango.models import MangoProductFile


# Create your models here.
class ExtractedPitData(BaseModel):
    mango_product_file = models.ForeignKey(MangoProductFile, on_delete=models.CASCADE)
    raw_analysis_name = models.CharField(max_length=1024)
    slice_value = models.CharField(max_length=1024)
    section_header_1 = models.CharField(max_length=1024)
    section_header_2 = models.CharField(max_length=1024)
    source_sheet_name = models.CharField(max_length=1024)
    source_data_file_name = models.CharField(max_length=1024)
    date = models.DateField()
    value = models.DecimalField(max_digits=36, decimal_places=10)
    timeseries_id = models.UUIDField()
