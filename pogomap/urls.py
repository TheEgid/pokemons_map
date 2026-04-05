from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from pokemon_entities import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.index, name="index"),
    path("pokemon/<int:pokemon_id>/", views.pokemon_detail, name="pokemon_detail"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
