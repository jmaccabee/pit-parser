# Generated by Django 4.2 on 2023-05-02 00:27
from mango.utils import create_objects_from_source_file

from django.db import migrations


def annotate(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ("mango", "0008_auto_20230430_1708"),
    ]

    operations = [migrations.RunPython(annotate)]
