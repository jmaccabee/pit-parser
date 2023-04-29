from django.contrib import admin

from .models import MangoProduct, MangoProductFile


class MangoProductAdmin(admin.ModelAdmin):
    pass


class MangoProductFileAdmin(admin.ModelAdmin):
    pass


admin.site.register(MangoProduct, MangoProductAdmin)
admin.site.register(MangoProductFile, MangoProductFileAdmin)
