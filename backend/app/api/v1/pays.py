from fastapi import APIRouter, Depends, HTTPException
from ..services.payment_service import PaymentService, PaymentProvider
from ..core.security import get_current_user

router = APIRouter()
payment_service = PaymentService()

@router.post("/create")
async def create_payment(amount: float, currency: str, provider: PaymentProvider, current_user=Depends(get_current_user)):
    """Инициировать платеж. Возвращает ссылку для оплаты или сведения."""
    if not current_user:
        raise HTTPException(status_code=401, detail="Auth required")
    try:
        redirect_url = payment_service.initiate_payment(provider, amount, currency, current_user.id)
        return {"pay_url": redirect_url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/webhook/{provider}")
async def payment_webhook(provider: PaymentProvider, data: dict):
    """Вебхук для приема уведомлений от платежного провайдера."""
    success = payment_service.handle_callback(provider, data)
    if not success:
        raise HTTPException(status_code=400, detail="Invalid callback")
    return {"status": "ok"}
