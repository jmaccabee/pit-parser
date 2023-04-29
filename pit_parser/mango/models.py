import uuid
from django.db import models


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    create_datetime = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class MangoProduct(BaseModel):
    id = models.CharField(max_length=36, primary_key=True)
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name


class MangoProductFile(BaseModel):
    mango_product_id = models.ForeignKey(MangoProduct, on_delete=models.CASCADE)
    data_file = models.FileField(upload_to="datafiles")

    def __str__(self):
        return self.data_file.name.split("/")[1]
