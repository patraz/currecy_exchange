from django.db import models


class Currency(models.Model):
    code = models.CharField(max_length=3, unique=True)
    name = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.code} ({self.name})"

    class Meta:
        verbose_name_plural = "currencies"


class CurrencyExchangeRate(models.Model):
    base_currency = models.ForeignKey(
        Currency,
        on_delete=models.CASCADE,
        related_name='base_rates'
    )
    target_currency = models.ForeignKey(
        Currency,
        on_delete=models.CASCADE,
        related_name='target_rates'
    )
    rate = models.DecimalField(max_digits=10, decimal_places=6)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.base_currency}/{self.target_currency}: {self.rate}"

    class Meta:
        indexes = [
            models.Index(
                fields=['base_currency', 'target_currency', 'timestamp']),
        ]
