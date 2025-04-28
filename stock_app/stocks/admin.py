from django.contrib import admin
from stocks.models import Company, StockData

# Register your models here.
admin.site.register(Company)
admin.site.register(StockData)