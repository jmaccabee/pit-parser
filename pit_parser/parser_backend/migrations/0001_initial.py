# Generated by Django 4.2 on 2023-04-29 19:03

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("mango", "0004_mangoproductfile_is_processed"),
    ]

    operations = [
        migrations.CreateModel(
            name="ExtractedPitData",
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
                ("raw_analysis_name", models.CharField(max_length=1024)),
                ("slice_value", models.CharField(max_length=1024)),
                ("section_header_1", models.CharField(max_length=1024)),
                ("section_header_2", models.CharField(max_length=1024)),
                ("source_sheet_name", models.CharField(max_length=1024)),
                ("source_data_file_name", models.CharField(max_length=1024)),
                ("date", models.DateField()),
                ("value", models.DecimalField(decimal_places=10, max_digits=36)),
                ("timeseries_id", models.UUIDField()),
                (
                    "mango_product_file",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="mango.mangoproductfile",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]