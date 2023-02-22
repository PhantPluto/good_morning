from datetime import date, datetime
import math
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
import os
import random

today = datetime.now()
start_date = os.environ['START_DATE']
city = os.environ['CITY']
birthday = os.environ['BIRTHDAY']

app_id = os.environ["APP_ID"]
app_secret = os.environ["APP_SECRET"]

user_id = os.environ["USER_ID"]
template_id = os.environ["TEMPLATE_ID"]


def get_weather():
    url = "https://v0.yiketianqi.com/free/day?appid=85485457&appsecret=ymW8hxiD&city=杭州"
    weather = requests.get(url).json()
    return weather['wea'],weather['tem'],weather['tem_night'],weather['tem_day']


def get_count():
    delta = today - datetime.strptime(start_date, "%Y-%m-%d")
    return delta.days+1


def get_birthday():
    next = datetime.strptime(str(date.today().year) + "-" + birthday, "%Y-%m-%d")
    if next < datetime.now():
        next = next.replace(year=next.year + 1)
    return (next - today).days-1


def get_words():
    words = requests.get("https://api.1314.cool/words/api.php").text.replace("<br>","\n")
    return words


def get_random_color():
    return "#%06x" % random.randint(0, 0xFFFFFF)


client = WeChatClient(app_id, app_secret)

wm = WeChatMessage(client)
//wea, temperature, low, high = get_weather()
data = {/*"weather": {"value": wea,"color":"#FFFF00"},
        "temperature": {"value": temperature,"color":"#FFFF00"},
        "low": {"value": low,"color":"#87CEFA"},
        "high": {"value": high,"color":"#FF0000"},*/
        "love_days": {"value": get_count()},
        "birthday_left": {"value": get_birthday()},
        "words": {"value": get_words(), "color": get_random_color()}}
res = wm.send_template(user_id, template_id, data)
print(res)
