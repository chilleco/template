from enum import Enum

# Единый интерфейс/стратегия для платёжных провайдеров
class PaymentProvider(str, Enum):
    STRIPE = "stripe"
    BYBIT = "bybit"
    # ... другие по необходимости

class PaymentService:
    def __init__(self):
        # Инициализация провайдеров (например, API ключи берём из настроек)
        from .payment_providers import stripe_provider, bybit_provider
        self.providers = {
            PaymentProvider.STRIPE: stripe_provider.StripeProvider(),
            PaymentProvider.BYBIT: bybit_provider.ByBitProvider()
        }
    def initiate_payment(self, provider: PaymentProvider, amount: float, currency: str, user_id: int) -> str:
        """Инициировать платеж через указанный провайдер. Возвращает URL для переадресации или идентификатор транзакции."""
        return self.providers[provider].initiate_payment(amount, currency, user_id)
    def handle_callback(self, provider: PaymentProvider, data: dict) -> bool:
        """Обработать callback/вебхук от платежной системы."""
        return self.providers[provider].process_callback(data)
