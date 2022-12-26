import os
import sys

import bs4
import requests

from bs4 import BeautifulSoup

from linebot import LineBotApi, WebhookParser
from linebot.models import MessageEvent, TextMessage, TextSendMessage, TemplateSendMessage, ButtonsTemplate 


channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", None)


def send_text_message(reply_token, text):
    line_bot_api = LineBotApi(channel_access_token)
    line_bot_api.reply_message(reply_token, TextSendMessage(text=text))

    return "OK"

def send_button_message(reply_token, title, text, btn, url):
    line_bot_api = LineBotApi(channel_access_token)
    message = TemplateSendMessage(
        alt_text='button template',
        template = ButtonsTemplate(
            title = title,
            text = text,
            thumbnail_image_url = url,
            actions = btn
        )
    )
    line_bot_api.reply_message(reply_token, message)

    return "OK"

"""
失敗的作品(不會拿東西)
def get_curr_commodity():
    res = requests.get('https://hk.investing.com/commodities/real-time-futures')
    res.encoding = 'utf-8'

    soup = BeautifulSoup(res.text, 'lxml')
    table = soup.find('table', {'class': 'genTbl closedTbl crossRatesTbl'})
    table = table.find_all('tr')

    col = ["商品", "月", "最新", "高", "低", "升跌幅", "升跌率"]

    table = table[18:]
    data = []

    for row in table
        row_d = []
        data = row.find('td', {'align': 'left'}).text
        buyinAndUad = row.find_all('td', {'class': 'changeup'})
        date = row.find('td', )


    return output
"""

"""
def send_image_url(id, img_url):
    pass
"""
