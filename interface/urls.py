from django.contrib import admin
from django.urls import path, include
from web import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('admin/import_users', views.import_users),
    path('', views.index, name='index'),
    path('accounts/', include('django.contrib.auth.urls')),
]
