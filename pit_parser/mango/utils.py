import csv
import os

from django.conf import settings

from mango.models import MangoProduct, MangoProductAnnotation


def create_mango_annotations(mango_metrics_filename):
    with open(
        os.path.join(
            settings.MEDIA_ROOT,
            "mango_data",
            "mango_metrics",
            mango_metrics_filename,
        )
    ) as csvfile:
        reader = csv.DictReader(csvfile)
        first_row = next(reader)
        mango_product = MangoProduct.objects.get(name=first_row["product_name"])
        MangoProductAnnotation.objects.create(
            mango_product=mango_product,
            field_label=first_row["field_label"],
            field_value=first_row["field_value"],
            calculation_type=first_row["calculation_type"],
        )
        for row in reader:
            MangoProductAnnotation.objects.create(
                mango_product=mango_product,
                field_label=row["field_label"],
                field_value=row["field_value"],
                calculation_type=row["calculation_type"],
            )
