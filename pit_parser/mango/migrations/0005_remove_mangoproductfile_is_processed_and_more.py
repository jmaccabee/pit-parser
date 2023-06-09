# Generated by Django 4.2 on 2023-04-29 21:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("mango", "0004_mangoproductfile_is_processed"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="mangoproductfile",
            name="is_processed",
        ),
        migrations.AddField(
            model_name="mangoproductfile",
            name="status",
            field=models.SmallIntegerField(
                choices=[(1, "UNPROCESSED"), (2, "PROCESSING"), (3, "PROCESSED")],
                default=1,
            ),
            preserve_default=False,
        ),
    ]
