from rest_framework import serializers
from .models import CurrencyExchangeRate


class CurrencyExchangeRateSerializer(serializers.ModelSerializer):
    currency_pair = serializers.SerializerMethodField()
    exchange_rate = serializers.DecimalField(
        source='rate', max_digits=10, decimal_places=6)

    class Meta:
        model = CurrencyExchangeRate
        fields = ['currency_pair', 'exchange_rate']

    def get_currency_pair(self, obj):
        return f"{obj.base_currency.code}{obj.target_currency.code}"
