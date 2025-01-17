from django.urls import path
from . import views

app_name = 'bhcabines'

urlpatterns = [
    path('', views.home, name='home'),
    path('capture_request_data/', views.capture_request_data, name='capture_request_data'),
]
