"""
URL configuration for pit_parser project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from .views import index, AnnotateDataFileView, view_product_data_files
from parser_backend.views import process_data_file

urlpatterns = [
    path("admin/", admin.site.urls),
    path("__reload__/", include("django_browser_reload.urls")),
    path("", index, name="index"),
    path(
        "products/<uuid:id>",
        view_product_data_files,
        name="view_product_data_files",
    ),
    path(
        "products/<uuid:mango_product_id>/datafiles/<uuid:mango_product_file_id>/annotate",
        AnnotateDataFileView.as_view(),
        name="annotate_data_file",
    ),
    path(
        "products/<uuid:mango_product_id>/datafiles/<uuid:mango_product_file_id>/process",
        process_data_file,
        name="process_data_file",
    ),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
