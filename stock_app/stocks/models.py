from django.db import models

class Company(models.Model):
    ticker = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.name} ({self.ticker})'


class StockData(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    date = models.DateField()
    open = models.FloatField()
    high = models.FloatField()
    low = models.FloatField()
    close = models.FloatField()
    volume = models.IntegerField()
    points_change = models.FloatField(null=True, blank=True)
    change_percent = models.FloatField(null=True, blank=True)
    turnover = models.FloatField(null=True, blank=True)
    pe_ratio = models.FloatField(null=True, blank=True)
    pb_ratio = models.FloatField(null=True, blank=True)
    div_yield = models.FloatField(null=True, blank=True)

    class Meta:
        ordering = ['date']