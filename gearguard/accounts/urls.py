from django.urls import path, include
from . import views

app_name = 'accounts'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('logout/', views.logout_view, name='logout'),
    # include django auth URLs under the accounts namespace (login, password reset, etc.)
    path('', include('django.contrib.auth.urls')),
]
