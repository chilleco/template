import stripe
from ...config import settings

class StripeProvider:
    def __init__(self):
        stripe.api_key = settings.stripe_secret_key
    def initiate_payment(self, amount, currency, user_id):
        # Создание Stripe Checkout Session
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[{"price_data": {"currency": currency, "product_data": {"name": "Deposit"}, "unit_amount": int(amount*100)}, "quantity": 1}],
            mode="payment",
            success_url="https://ourapp.com/payments/success?session_id={CHECKOUT_SESSION_ID}",
            cancel_url="https://ourapp.com/payments/cancel"
        )
        return session.url  # клиент будет перенаправлен на этот URL
    def process_callback(self, data):
        # Обработка webhook от Stripe (в data будет event)
        event = data  # в реальности нужно извлечь и проверить подпись webhook
        if event["type"] == "checkout.session.completed":
            session = event["data"]["object"]
            # Логика подтверждения платежа, обновление статуса в базе
            payment_id = session["id"]
            # ... отметить платеж payment_id как успешный
            return True
        return False
