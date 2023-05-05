from django.db import models

from base.models import BaseModel


class MangoProduct(BaseModel):
    id = models.CharField(max_length=36, primary_key=True)
    name = models.CharField(max_length=128)
    report_product_name = models.CharField(max_length=128, null=True, blank=True)
    report_product_id = models.UUIDField(null=True, blank=True)

    def __str__(self):
        return self.name


class MangoProductFile(BaseModel):
    UNPROCESSED = 1
    PROCESSING = 2
    PROCESSED = 3
    PROCESSING_STATUSES = (
        (UNPROCESSED, "UNPROCESSED"),
        (PROCESSING, "PROCESSING"),
        (PROCESSED, "PROCESSED"),
    )

    mango_product = models.ForeignKey(MangoProduct, on_delete=models.CASCADE)
    data_file = models.FileField(upload_to="datafiles")
    status = models.SmallIntegerField(choices=PROCESSING_STATUSES)

    @property
    def filename(self):
        return self.data_file.name.split("/")[1]

    def __str__(self):
        return self.filename


class MangoProductAnnotation(BaseModel):
    METRIC_NAME = "metric_name"
    SLICE_NAME = "slice_name"
    FIELD_LABELS = [
        (METRIC_NAME, "metric_name"),
        (SLICE_NAME, "slice_name"),
    ]

    POINT_CALC = "point"
    CALCULATION_TYPES = [
        (POINT_CALC, "point"),
    ]

    mango_product = models.ForeignKey(MangoProduct, on_delete=models.CASCADE)
    field_label = models.CharField(choices=FIELD_LABELS, max_length=128)
    field_value = models.CharField(max_length=1024)
    calculation_type = models.CharField(choices=CALCULATION_TYPES, max_length=128)


class YipitReportCampaignDataFile(BaseModel):
    # id is data file name
    id = models.CharField(max_length=512, primary_key=True)
    product_id = models.UUIDField()
    report_url = models.URLField(max_length=1024)
    campaign_id = models.UUIDField()
    sent_date = models.DateTimeField()
    subject_line = models.CharField(max_length=512)
    mango_product = models.ForeignKey(MangoProduct, on_delete=models.CASCADE)


class MangoProductSourceFile(BaseModel):
    YipitReportCampaignDataFile = "YipitReportCampaignDataFile"
    MangoProduct = "MangoProduct"
    MODEL_CHOICES = (
        (YipitReportCampaignDataFile, "YipitReportCampaignDataFile"),
        (MangoProduct, "MangoProduct"),
    )
    model_key = models.CharField(max_length=128, choices=MODEL_CHOICES)
    source_file = models.FileField(upload_to="mango_data/mango_products")

    def __str__(self):
        return self.source_file.name


class MangoAnnotationSourceFile(BaseModel):
    mango_product_id = models.ForeignKey(MangoProduct, on_delete=models.CASCADE)
    source_file = models.FileField(upload_to="mango_data/mango_metrics")

    def __str__(self):
        return self.source_file.name
