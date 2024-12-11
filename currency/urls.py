from django.urls import path
from .views import CurrencyExchangeRateView

urlpatterns = [
    path('currency/<str:base_currency>/<str:target_currency>/',
         CurrencyExchangeRateView.as_view(),
         name='currency-exchange-rate'),
]
