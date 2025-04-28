from django.shortcuts import render, get_object_or_404
from stocks.models import Company, StockData

def stock_dashboard(request, company_id=None):
    companies = Company.objects.all().order_by('name')

    selected_company = None
    stock_data = []

    if company_id:
        selected_company = get_object_or_404(Company, id=company_id)
        stock_data = StockData.objects.filter(company=selected_company).order_by('date')

    return render(request, 'stocks/dashboard.html', {
        'companies': companies,
        'selected_company': selected_company,
        'stock_data': stock_data,
    })
