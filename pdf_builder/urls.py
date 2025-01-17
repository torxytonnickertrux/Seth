# pdf_builder/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.painel, name='painel'),  # Página principal do painel
    path('gerar_pdf/', views.gerar_pdf, name='gerar_pdf'),
]
