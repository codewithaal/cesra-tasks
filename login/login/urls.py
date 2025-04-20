from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from base import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include(("base.urls", "base"), "base")),
    path('profile/', views.profilePicture, name='profile'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)