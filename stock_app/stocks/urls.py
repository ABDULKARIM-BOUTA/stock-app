from django.urls import path
from stocks import views

app_name = 'stocks'

urlpatterns = [
    path('', views.stock_dashboard, name='stock_dashboard'),
    path('<int:company_id>/', views.stock_dashboard, name='stock_dashboard_company'),
]