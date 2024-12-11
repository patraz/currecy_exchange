
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import CurrencyExchangeRate
from .serializers import CurrencyExchangeRateSerializer


class CurrencyExchangeRateView(APIView):
    def get(self, request, base_currency, target_currency):
        try:
            latest_rate = CurrencyExchangeRate.objects.filter(
                base_currency__code=base_currency.upper(),
                target_currency__code=target_currency.upper()
            ).latest('timestamp')

            serializer = CurrencyExchangeRateSerializer(latest_rate)
            return Response(serializer.data)
        except CurrencyExchangeRate.DoesNotExist:
            return Response(
                {"error": "Exchange rate not found"},
                status=status.HTTP_404_NOT_FOUND
            )
