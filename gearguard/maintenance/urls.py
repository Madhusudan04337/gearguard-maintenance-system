from django.urls import path
from . import views

urlpatterns = [
    path('', views.maintenance_list, name='maintenance_list'),
    path('new/', views.maintenance_create, name='maintenance_create'),
    path('<int:pk>/edit/', views.maintenance_edit, name='maintenance_edit'),
]
