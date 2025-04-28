from django.urls import path
from stocks import views

urlpatterns = [
    path('stocks/', views.stock_dashboard, name='stock_dashboard'),  # <-- name this one
    path('stocks/<int:company_id>/', views.stock_dashboard, name='stock_dashboard_company'),  # <-- name this one
]