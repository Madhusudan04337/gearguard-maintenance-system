from django.urls import path
from . import views

app_name = 'equipment'   
urlpatterns = [
    path('', views.equipment_list, name='equipment_list'),
    path('create/', views.equipment_create, name='equipment_create'),  # New route for creating equipment
    path('<int:pk>/', views.equipment_detail, name='equipment_detail'),
    path('<int:pk>/edit/', views.equipment_edit, name='equipment_edit'),  # New route for editing equipment
    path('<int:pk>/scrap/', views.equipment_scrap, name='equipment_scrap'),
]
