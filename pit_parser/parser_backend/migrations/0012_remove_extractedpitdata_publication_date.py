# Generated by Django 4.2 on 2023-05-05 19:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("parser_backend", "0011_extractedpitdata_publication_date"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="extractedpitdata",
            name="publication_date",
        ),
    ]
