from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from links import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.create_link, name='create_link'),
    path('access/<uuid:pk>/', views.access_link, name='access_link'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
