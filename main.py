import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties

from Routers import (
    weather_routers, main_routers,
    # prikol_router,
    joke_router, yoomoney_router
)
from config import config

# We turn on logging so as not to miss important messages
logging.basicConfig(level=logging.INFO)
bot = Bot(
    token=config.bot_token.get_secret_value(),
    default=DefaultBotProperties(parse_mode="HTML")
)
dp = Dispatcher()


# start polling and new updates
async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    dp.include_routers(
        weather_routers.router,
        main_routers.router,
        # prikol_router.router,
        joke_router.router,
        yoomoney_router.router
    )
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
