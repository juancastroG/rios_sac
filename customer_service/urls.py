from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    path('', views.search_view, name='search'),
    path('api/customer/<str:document_number>/', views.CustomerDetailAPI.as_view(), name='customer-detail'),
    path('api/export-customer/<str:document_number>/', views.export_customer_data, name='export-customer'),
    path('api/loyalty-report/', views.generate_loyalty_report, name='loyalty-report'),
    path('reports/loyalty/', login_required(views.generate_loyalty_report), name='loyalty-report'),
]