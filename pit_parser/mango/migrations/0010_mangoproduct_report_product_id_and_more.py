# Generated by Django 4.2 on 2023-05-05 15:19

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ("mango", "0009_auto_20230502_0027"),
    ]

    operations = [
        migrations.AddField(
            model_name="mangoproduct",
            name="report_product_id",
            field=models.UUIDField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="mangoproduct",
            name="report_product_name",
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
        migrations.CreateModel(
            name="YipitReportCampaign",
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
                ("product_id", models.UUIDField()),
                ("report_url", models.URLField()),
                ("campaign_id", models.UUIDField()),
                ("sent_date", models.DateTimeField()),
                ("subject_line", models.CharField(max_length=256)),
                ("data_file_name", models.CharField(max_length=128)),
                (
                    "mango_product_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="mango.mangoproduct",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
