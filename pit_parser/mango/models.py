import uuid
from django.db import models


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    create_datetime = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class MangoProduct(BaseModel):
    mango_product_id = models.CharField(max_length=36)
    mango_product_name = models.CharField(max_length=128)
