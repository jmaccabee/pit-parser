# Generated by Django 4.2 on 2023-05-05 18:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "mango",
            "0013_rename_mango_product_id_yipitreportcampaigndatafile_mango_product",
        ),
    ]

    operations = [
        migrations.AlterField(
            model_name="yipitreportcampaigndatafile",
            name="id",
            field=models.CharField(max_length=512, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name="yipitreportcampaigndatafile",
            name="report_url",
            field=models.URLField(max_length=1024),
        ),
        migrations.AlterField(
            model_name="yipitreportcampaigndatafile",
            name="subject_line",
            field=models.CharField(max_length=512),
        ),
    ]
