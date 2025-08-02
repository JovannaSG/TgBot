from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from yoomoney import Quickpay
from config import config

router = Router()


class PaymentStates(StatesGroup):
    waiting_for_amount = State()


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


@router.message(Command("donate", prefix="/"))
async def donate_command(message: types.Message):
    """Handle /donate command"""
    keyboard = [
        [InlineKeyboardButton(text="💰 100 ₽", callback_data="donate_100")],
        [InlineKeyboardButton(text="💰 300 ₽", callback_data="donate_300")],
        [InlineKeyboardButton(text="💰 500 ₽", callback_data="donate_500")],
        [InlineKeyboardButton(text="💰 1000 ₽", callback_data="donate_1000")],
        [InlineKeyboardButton(text="💳 Другая сумма", callback_data="custom_amount")]
    ]
    
    await message.answer(
        "💝 Поддержите проект!\n\n"
        "Выберите сумму для пожертвования:",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=keyboard)
    )


@router.callback_query(F.data.startswith("donate_"))
async def handle_donate_amount(callback: types.CallbackQuery):
    """Handle donation amount selection"""
    amount_str = callback.data.split("_")[1]
    
    if amount_str == "custom":
        await callback.message.answer("Введите сумму для пожертвования (в рублях):")
        # Here you could set a state to wait for custom amount
        await callback.answer()
        return
    
    try:
        amount = int(amount_str)
        label = f"donate_{callback.from_user.id}_{amount}"
        
        keyboard = get_payment_keyboard(amount, label)
        
        await callback.message.edit_text(
            f"💳 Оплата {amount} ₽\n\n"
            "Нажмите кнопку 'Оплатить' для перехода к оплате.\n"
            "После оплаты нажмите 'Проверить оплату'.",
            reply_markup=keyboard
        )
        await callback.answer()
        
    except ValueError:
        await callback.answer("Ошибка: неверная сумма", show_alert=True)


@router.callback_query(F.data.startswith("check_payment_"))
async def check_payment(callback: types.CallbackQuery):
    """Check payment status"""
    label = callback.data.split("check_payment_")[1]
    
    # In a real implementation, you would check the payment status
    # using YooMoney API with your token
    await callback.answer(
        "🔍 Проверка платежа...\n\n"
        "В MVP версии проверка платежей не реализована.\n"
        "В реальном проекте здесь будет интеграция с API YooMoney.",
        show_alert=True
    )


@router.callback_query(F.data == "cancel_payment")
async def cancel_payment(callback: types.CallbackQuery):
    """Cancel payment"""
    await callback.message.edit_text("❌ Оплата отменена")
    await callback.answer()


@router.message(Command("payment_info", prefix="/"))
async def payment_info(message: types.Message):
    """Show payment information"""
    info_text = (
        "💳 Информация о платежах:\n\n"
        f"Получатель: {config.yoomoney_receiver}\n"
        "Способ оплаты: ЮMoney\n\n"
        "Для пожертвования используйте /donate"
    )
    await message.answer(info_text)
