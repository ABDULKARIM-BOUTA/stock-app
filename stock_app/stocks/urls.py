from django.urls import path
from stocks import views

app_name = 'stocks'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('chart/<path:ticker>/', views.stock_chart, name='stock_chart'),
]