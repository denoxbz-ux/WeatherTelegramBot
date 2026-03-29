import telebot
import requests
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

API_KEY=''
URL_WEATHER_API='https://api.openweathermap.org/data/2.5/weather'
TOKEN=''

bot=telebot.TeleBot(TOKEN)
keyboard=ReplyKeyboardMarkup(resize_keyboard=True)
keyboard.add(KeyboardButton('Получить погоду', request_location=True))
keyboard.add(KeyboardButton('О проекте'))

EMOJI_CODE={200:'⛈',300:'🌧',500:'🌦',600:'❄️',700:'🌫',800:'☀',801:'🌤',802:'☁',803:'☁',804:'☁'}
def get_weater(lat,lon):
    params={'lat':lat,
            'lon':lon,
            'lang':'ru',
            'units':'metric',
            'appid':API_KEY}
    response=requests.get(url=URL_WEATHER_API,params=params).json()
    print(response)
    city_name = response['name']
    description = response['weather'][0]['description']
    code = response['weather'][0]['id']
    temp = response['main']['temp']
    temp_feels_like = response['main']['feels_like']
    humidity = response['main']['humidity']
    emoji = EMOJI_CODE[code]
    message = f'🏙 Погода B: {city_name}\n'
    message += f'{emoji} {description.capitalize()}. \n'
    message += f'🌡 Tемпература {temp}C.\n'
    message += f'🌡 Ощущается {temp_feels_like}C.\n'
    message += f'💧 Влажность {humidity}%. \n'
    return message


@bot.message_handler(commands=['start'])
def senf_welcome(message):
    text='Отправь мне своё местоположение и я отправлю тебе погоду.'
    bot.send_message(message.chat.id,text,reply_markup=keyboard)


@bot.message_handler(content_types=['location'])
def send_weather(message):
    lon=message.location.longitude
    lat=message.location.latitude
    result=get_weater(lat,lon)
    if result:
        bot.send_message(message.chat.id,result,reply_markup=keyboard)


@bot.message_handler(regexp='О проекте')
def senf_about(message):
    text='Проект "Телерам бот" отправляет текущую погоду по вашему местоположению \n \nСделал Никитин Илья'
    bot.send_message(message.chat.id,text,reply_markup=keyboard)


bot.infinity_polling()
