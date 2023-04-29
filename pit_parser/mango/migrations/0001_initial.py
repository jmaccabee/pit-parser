# Generated by Django 4.2 on 2023-04-29 14:10

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="MangoProduct",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("create_datetime", models.DateTimeField(auto_now_add=True)),
                ("last_updated", models.DateTimeField(auto_now=True)),
                ("mango_product_id", models.CharField(max_length=36)),
                ("mango_product_name", models.CharField(max_length=128)),
            ],
            options={
                "abstract": False,
            },
        ),
    ]