from django.db import models

from base.models import BaseModel


class MangoProduct(BaseModel):
    id = models.CharField(max_length=36, primary_key=True)
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name


class MangoProductFile(BaseModel):
    mango_product = models.ForeignKey(MangoProduct, on_delete=models.CASCADE)
    data_file = models.FileField(upload_to="datafiles")
    is_processed = models.BooleanField(default=False)

    @property
    def filename(self):
        return self.data_file.name.split("/")[1]

    def __str__(self):
        return self.filename
