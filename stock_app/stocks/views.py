from django.shortcuts import render, get_object_or_404
from .models import Company, StockData


def dashboard(request):
    companies = Company.objects.all()
    return render(request, 'stocks/dashboard.html', {'companies': companies})

def stock_chart(request, ticker):
    # No need to unquote since path converter handles it
    company = get_object_or_404(Company, ticker=ticker)

    # Your chart rendering logic here
    return render(request, 'stocks/chart.html', {
        'company': company,
        'ticker': ticker
    })