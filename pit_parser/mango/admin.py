from django.apps import apps
from django.contrib import admin

from .models import (
    MangoAnnotationSourceFile,
    MangoProduct,
    MangoProductAnnotation,
    MangoProductFile,
    MangoProductSourceFile,
    YipitReportCampaignDataFile,
)
from .utils import create_objects_from_source_file


@admin.action(description="Update model from source")
def update_mangoproduct_model_from_source_file(modeladmin, request, queryset):
    for obj in queryset:
        model_name = obj.model_key

        model = apps.get_model("mango", model_name=model_name)
        for row in create_objects_from_source_file(
            obj.source_file.name,
        ):
            record_id = row.pop("id")
            obj, created = model.objects.update_or_create(
                id=record_id,
                defaults=row,
            )


@admin.action(description="Update model from source")
def update_mangoproductannotation_model_from_source_file(modeladmin, request, queryset):
    for obj in queryset:
        (
            MangoProductAnnotation.objects.filter(
                mango_product_id=obj.mango_product_id
            ).delete()
        )
        for row in create_objects_from_source_file(obj.source_file.name):
            # remove "product_name" key if it exists
            _ = row.pop("product_name")
            row["mango_product_id"] = obj.mango_product_id.id
            print(row)
            annotation_obj = MangoProductAnnotation(**row)
            annotation_obj.save()


class MangoProductSourceFileAdmin(admin.ModelAdmin):
    actions = [update_mangoproduct_model_from_source_file]


class MangoAnnotationSourceFileAdmin(admin.ModelAdmin):
    actions = [update_mangoproductannotation_model_from_source_file]


class MangoProductFileAdmin(admin.ModelAdmin):
    pass


class MangoProductAdmin(admin.ModelAdmin):
    ordering = ["name"]


class MangoProductAnnotationAdmin(admin.ModelAdmin):
    list_display = ["mango_product", "field_label", "field_value"]
    ordering = ["mango_product", "field_label", "field_value"]


class YipitReportCampaignDataFileAdmin(admin.ModelAdmin):
    list_display = ["id", "mango_product", "sent_date", "subject_line"]


admin.site.register(MangoProductFile, MangoProductFileAdmin)
admin.site.register(MangoProduct, MangoProductAdmin)
admin.site.register(MangoProductAnnotation, MangoProductAnnotationAdmin)
admin.site.register(MangoAnnotationSourceFile, MangoAnnotationSourceFileAdmin)
admin.site.register(MangoProductSourceFile, MangoProductSourceFileAdmin)
admin.site.register(YipitReportCampaignDataFile, YipitReportCampaignDataFileAdmin)
