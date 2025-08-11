from decimal import Decimal
from django.utils import timezone
from django.conf import settings
import requests

from forexservice.models import RateSnapshot
from forexservice.utils import API_REFRESH_INTERVAL, SUPPORTED_CURRENCIES


class ExchangeService:
    @staticmethod
    def update_rates():
        """Fetch and save exchange rates from external API."""
        url = settings.EXCHANGE_API_URL
        key = settings.EXCHANGE_API_KEY

        try:
            response = requests.get(url, params={
                "symbols": ",".join(SUPPORTED_CURRENCIES),
                "access_key": key
            })
            data = response.json()

            if response.status_code != 200 or "error" in data:
                raise ValueError("Error fetching exchange rates.")

            RateSnapshot.objects.create(response_data=data)
            return "Exchange rates updated."

        except Exception as e:
            raise RuntimeError(f"Rate update failed: {str(e)}")

    @staticmethod
    def convert_amount(amount, src, tgt, fee_pct):
        """Convert amount from src to tgt currency, applying platform fee."""
        try:
            record = RateSnapshot.objects.latest('created_at')
            now = timezone.now().astimezone(timezone.get_current_timezone())

            if now - record.created_at > API_REFRESH_INTERVAL:
                ExchangeService.update_rates()
                record.refresh_from_db()

            rates = record.response_data['rates']

            if src not in rates or tgt not in rates:
                raise ValueError(f"Missing rate for {src} or {tgt}.")

            src_to_eur = Decimal(rates[src])
            tgt_to_eur = Decimal(rates[tgt])
            base_rate = tgt_to_eur / src_to_eur

            charged_fee = amount * (fee_pct / 100)
            net_amount = amount - charged_fee
            net_converted = (net_amount / src_to_eur) * tgt_to_eur
            platform_rate = (net_converted / amount) if amount > 0 else 0

            return base_rate, platform_rate, charged_fee, net_converted

        except RateSnapshot.DoesNotExist:
            ExchangeService.update_rates()
            return ExchangeService.convert_amount(amount, src, tgt, fee_pct)
