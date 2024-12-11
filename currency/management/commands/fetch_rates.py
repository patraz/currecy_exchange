from django.core.management.base import BaseCommand
import yfinance as yf
from currency.models import Currency, CurrencyExchangeRate


class Command(BaseCommand):
    help = 'Fetch currency exchange rates from Yahoo Finance'

    def handle(self, *args, **kwargs):
        currency_pairs = [
            ('EUR', 'USD', 'Euro', 'US Dollar'),
            ('USD', 'JPY', 'US Dollar', 'Japanese Yen'),
            ('PLN', 'USD', 'Polish Złoty', 'US Dollar')
        ]

        for base_code, target_code, base_name, target_name in currency_pairs:
            base_curr, _ = Currency.objects.get_or_create(
                code=base_code,
                defaults={'name': base_name}
            )
            target_curr, _ = Currency.objects.get_or_create(
                code=target_code,
                defaults={'name': target_name}
            )

            try:
                # Pobieramy kurs z Yahoo Finance
                symbol = f"{base_code}{target_code}=X"
                ticker = yf.Ticker(symbol)
                # Pobieramy historię za ostatni dzień
                history = ticker.history(period="1d")

                if not history.empty:
                    # Bierzemy ostatnią cenę zamknięcia
                    rate = history['Close'].iloc[-1]

                    # Zapisujemy kurs do bazy
                    CurrencyExchangeRate.objects.create(
                        base_currency=base_curr,
                        target_currency=target_curr,
                        rate=rate
                    )

                    self.stdout.write(
                        self.style.SUCCESS(
                            f'Successfully fetched rate for {base_code}/{target_code}: {rate}'
                        )
                    )
                else:
                    self.stdout.write(
                        self.style.ERROR(
                            f'No data available for {base_code}/{target_code}'
                        )
                    )

            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(
                        f'Failed to fetch rate for {base_code}/{target_code}: {str(e)}'
                    )
                )
