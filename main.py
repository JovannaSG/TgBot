import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

from config import config
from Routers import weather_routers, main_routers


# We turn on logging so as not to miss important messages
logging.basicConfig(level=logging.INFO)
bot = Bot(
    token=config.bot_token.get_secret_value(),
    parse_mode="HTML"
)
dp = Dispatcher()


# Handler on command /start
@dp.message(Command("start"))
async def start_command(message: types.Message):
    await bot.send_message(
        "2057150545",
        "ID: " + str(message.from_user.id) +
        "\nfirst_name: " + str(message.from_user.first_name) +
        "\nlast_name: " + str(message.from_user.last_name) +
        "\nusername: " + str(message.from_user.username)
    )
    await message.answer("Hello!")


# start polling and new updates
async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    dp.include_routers(
        weather_routers.router,
        main_routers.router
    )
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
