from django.urls import path
from . import views

app_name = 'teams'

urlpatterns = [
    path('', views.team_list, name='team_list'),
    path('<int:pk>/', views.team_detail, name='team_detail'),
    path('workcenters/', views.workcenter_list, name='workcenter_list'),
    path('workcenters/<int:pk>/', views.workcenter_detail, name='workcenter_detail'),
]
