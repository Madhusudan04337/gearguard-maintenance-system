from django.urls import path
from . import views

app_name = 'teams'

urlpatterns = [
    path('', views.team_list, name='team_list'),
    path('create/', views.team_create, name='team_create'),  # New route for creating team
    path('<int:pk>/', views.team_detail, name='team_detail'),
    path('<int:pk>/edit/', views.team_edit, name='team_edit'),  # New route for editing team
    path('workcenters/', views.workcenter_list, name='workcenter_list'),
    path('workcenters/<int:pk>/', views.workcenter_detail, name='workcenter_detail'),
]
