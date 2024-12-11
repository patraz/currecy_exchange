from rest_framework.test import APITestCase
from rest_framework import status
from .models import Currency, CurrencyExchangeRate
from decimal import Decimal


class CurrencyExchangeRateTests(APITestCase):
    def setUp(self):

        self.eur = Currency.objects.create(
            code='EUR',
            name='Euro'
        )
        self.usd = Currency.objects.create(
            code='USD',
            name='US Dollar'
        )

        self.rate = CurrencyExchangeRate.objects.create(
            base_currency=self.eur,
            target_currency=self.usd,
            rate=Decimal('1.034')
        )

    def test_get_exchange_rate(self):

        url = '/currency/EUR/USD/'
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data['currency_pair'], 'EURUSD')
        self.assertEqual(float(response.data['exchange_rate']), 1.034)

    def test_get_nonexistent_rate(self):

        url = '/currency/GBP/JPY/'
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_invalid_currency_code(self):

        url = '/currency/INVALID/USD/'
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
