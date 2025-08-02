from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

donate_keyboard = [
    [InlineKeyboardButton(text="💰 100 ₽", callback_data="donate_100")],
    [InlineKeyboardButton(text="💰 300 ₽", callback_data="donate_300")],
    [InlineKeyboardButton(text="💰 500 ₽", callback_data="donate_500")],
    [InlineKeyboardButton(text="💰 1000 ₽", callback_data="donate_1000")],
    [InlineKeyboardButton(text="💳 Другая сумма", callback_data="custom_amount")]
]


# Create payment keyboard
def get_payment_keyboard(amount: int, label: str) -> InlineKeyboardMarkup:
    quickpay = Quickpay(
        receiver=config.yoomoney_receiver,
        quickpay_form="shop",
        targets="Поддержка проекта",
        paymentType="SB",
        sum=amount,
        label=label
    )
    
    keyboard = [
        [InlineKeyboardButton(text="💳 Оплатить", url=quickpay.base_url)],
        [InlineKeyboardButton(text="✅ Проверить оплату", callback_data=f"check_payment_{label}")],
        [InlineKeyboardButton(text="❌ Отмена", callback_data="cancel_payment")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)
