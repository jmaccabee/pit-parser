# Generated by Django 4.2 on 2023-05-05 18:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("mango", "0011_mangoannotationsourcefile_mangoproductsourcefile_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="mangoproductsourcefile",
            name="model_key",
            field=models.CharField(
                choices=[
                    ("YipitReportCampaignDataFile", "YipitReportCampaignDataFile"),
                    ("MangoProduct", "MangoProduct"),
                ],
                max_length=128,
            ),
        ),
    ]