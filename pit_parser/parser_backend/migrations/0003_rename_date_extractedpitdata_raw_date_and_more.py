# Generated by Django 4.2 on 2023-04-30 04:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("parser_backend", "0002_alter_extractedpitdata_date"),
    ]

    operations = [
        migrations.RenameField(
            model_name="extractedpitdata",
            old_name="date",
            new_name="raw_date",
        ),
        migrations.RemoveField(
            model_name="extractedpitdata",
            name="value",
        ),
        migrations.AddField(
            model_name="extractedpitdata",
            name="raw_value",
            field=models.CharField(default=0, max_length=32),
            preserve_default=False,
        ),
    ]