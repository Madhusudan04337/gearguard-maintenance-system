from django.urls import path
from . import views

urlpatterns = [
    path('', views.equipment_list, name='equipment_list'),
    path('<int:pk>/', views.equipment_detail, name='equipment_detail'),
]
