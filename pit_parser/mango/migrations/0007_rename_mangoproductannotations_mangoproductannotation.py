# Generated by Django 4.2 on 2023-04-30 17:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("mango", "0006_mangoproductannotations"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="MangoProductAnnotations",
            new_name="MangoProductAnnotation",
        ),
    ]