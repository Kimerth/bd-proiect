from django.contrib import admin
from django.urls import path, include
from web import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('admin/import_users', views.import_users),
    path('', views.index, name='index'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('tools', views.display_tools),
    path('researchers', views.display_researchers),
    path('experiments', views.display_experiments),
    path('results', views.display_results),
    path('about', views.display_about),
    path('tools/add', views.add_tool),
    path('researchers/add', views.add_researcher),
    path('experiments/add', views.add_experiment),
    path('results/add', views.add_result),
    path('about/add', views.add_basic),
]
