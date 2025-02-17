from aiogram import Router
from aiogram.filters import Command, CommandObject
from aiogram.types import Message

from datetime import datetime
import requests
import math


router = Router()
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


@router.message(Command("weather", prefix="/"))
async def get_weather(message: Message, command: CommandObject):
    # check command's args
    city_name = command.args
    if city_name is None or not city_name.isalpha():
        print(type(city_name))
        await message.reply(
            "Ошибка: неправильный формат команды." +
            "\nПример: /weather {название города}"
        )
    else:
        print(type(city_name))
        # get request for weather forecast
        response = requests.get(
            "http://api.openweathermap.org/data/2.5/weather?q={}&lang=ru&units=metric&appid=4ba714d9111450e5537f17134b7235e4"
            .format(city_name)
        )
        data = response.json()
        city = data["name"]
        cur_temp = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        pressure = data["main"]["pressure"]
        wind = data["wind"]["speed"]

        sunrise_timestamp = datetime.fromtimestamp(data["sys"]["sunrise"])
        sunset_timestamp = datetime.fromtimestamp(data["sys"]["sunset"])
        length_of_the_day = datetime.fromtimestamp(data["sys"]["sunset"]) - \
            datetime.fromtimestamp(data["sys"]["sunrise"])
        weather_description = data["weather"][0]["main"]

        if weather_description in code_to_smile:
            wd = code_to_smile[weather_description]
        else:
            wd = "Don't have emojies for forecast display"

        # Send weather forecast to user
        await message.reply(
            f"{datetime.now().strftime('%Y-%m-%d %H:%M')}\n" +
            f"Погода в городе: {city}\nТемпература: {cur_temp}°C {wd}\n" +
            f"Влажность: {humidity}%\n" +
            f"Давление: {math.ceil(pressure/1.333)} мм.рт.ст\n" +
            f"Ветер: {wind} м/с \n" +
            f"Восход солнца: {sunrise_timestamp}\n" +
            f"Закат солнца: {sunset_timestamp}\n" +
            f"Продолжительность дня: {length_of_the_day}\n" +
            f"Хорошего дня!"
        )
