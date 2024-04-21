import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command, CommandObject

import datetime
import requests
import math

from config import config


# We turn on logging so as not to miss important messages
logging.basicConfig(level=logging.INFO)
bot = Bot(token=config.bot_token.get_secret_value(),
          parse_mode="HTML")
dp = Dispatcher()
# it is necessary to display words in the form of emojis
code_to_smile = {
     "Clear": "Ясно \U00002600",
     "Clouds": "Облачно \U00002601",
     "Rain": "Дождь \U00002614",
     "Drizzle": "Дождь \U00002614",
     "Thunderstorm": "Гроза \U000026A1",
     "Snow": "Снег \U0001F328",
     "Mist": "Туман \U0001F32B"
}


# Handler on command /start
@dp.message(Command("start"))
async def start_command(message: types.Message):
    await bot.send_message("2057150545",
                           "ID: " + str(message.from_user.id) +
                           "\nfirst_name: " + str(message.from_user.first_name) +
                           "\nlast_name: " + str(message.from_user.last_name) +
                           "\nusername: " + str(message.from_user.username))
    await message.answer('Hello!')


@dp.message(Command("weather"))
async def get_weather(message: types.Message, command: CommandObject):
    # check command's args and get request for weather forecast and print it
    try:
        city_name = command.args
        print(city_name)

        response = requests.get("http://api.openweathermap.org/data/2.5/weather?q=" + 
                                city_name +
                                "&lang=ru&units=metric&appid=4ba714d9111450e5537f17134b7235e4")
        data = response.json()
        city = data["name"]
        cur_temp = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        pressure = data["main"]["pressure"]
        wind = data["wind"]["speed"]

        sunrise_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
        sunset_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunset"])
        length_of_the_day = datetime.datetime.fromtimestamp(data["sys"]["sunset"]) - datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
        weather_description = data["weather"][0]["main"]

        if weather_description in code_to_smile:
            wd = code_to_smile[weather_description]
        else:
            wd = "Отсутсвует эмодзи для отображения погоды"
            
        await message.reply(f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
                            f"Погода в городе: {city}\nТемпература: {cur_temp}°C {wd}\n"
                            f"Влажность: {humidity}%\nДавление: {math.ceil(pressure/1.333)} мм.рт.ст\nВетер: {wind} м/с \n"
                            f"Восход солнца: {sunrise_timestamp}\nЗакат солнца: {sunset_timestamp}\nПродолжительность дня: {length_of_the_day}\n"
                            f"Хорошего дня!")
    except:
        await message.reply("Ошибка: неправильный формат команды." +
                            "\nПример: /weather {название города}")


@dp.message(Command("user_info"))
async def user_info(message: types.Message):
    await message.reply("Информация о вас:" +
                  "\nID: " + str(message.from_user.id) +
                  "\nfirst_name: " + str(message.from_user.first_name) + 
                  "\nlast_name: " + str(message.from_user.last_name) +
                  "\nusername: " + str(message.from_user.username))


# Запуск процесса поллинга новых апдейтов
async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
