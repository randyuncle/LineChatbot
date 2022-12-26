from transitions.extensions import GraphMachine

from bs4 import BeautifulSoup
import requests
from linebot.models import ImageCarouselColumn, URITemplateAction, MessageTemplateAction

from utils import send_text_message, send_button_message

#global variable
area = ''

class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(model=self, **machine_configs)

    def is_going_to_information(self, event):
        text = event.message.text
        return text.lower() == "information"

    def on_enter_information(self, event):
        print("I'm entering information")

        reply_token = event.reply_token

        send_text_message(reply_token, "")
        self.go_back()

    def is_going_to_find_rating_ten(self, event):
        text = event.message.text
        return text.lower() == "rating"

    def on_enter_find_rating_ten(self, event):
        print("I'm entering find_rating_ten")

        reply_token = event.reply_token
        send_text_message(reply_token, "請輸入您想探索的縣市\n(注意:本搜尋不支援連江縣)")

    def is_going_to_print_rating_list(self, event):
        global area
        text = event.message.text
        if text == '基隆市' | text == '台北市' | text == '新北市' | text == '桃園市' | text == '新竹市' | text == '新竹縣' | text == '苗栗縣' | text == '台中市' | text == '彰化縣' | text == '雲林縣' | text == '嘉義市' | text == '嘉義縣' | text == '南投縣' | text == '台南市' | text == '高雄市' | text == '屏東縣' | text == '宜蘭縣' | text == '花蓮縣' | text == '台東縣' | text == '金門縣' | text == '澎湖縣':
            area = text
            return True
        return False

    def on_enter_print_rating_list(self, event):
        print("I'm entering print_best_list")

        global area
        res = requests.get("https://ifoodie.tw/explore/" + area + "/list?sortby=rating&opening=true")
        soup = BeautifulSoup(res.content, "html.parser")
        tables = soup.find_all('div', {'class': 'jsx-3292609844 restaurant-info'}, limit=10)

        contents = ""
        for table in tables:
            title = table.find("a", {"class": "jsx-3292609844 title-text"}).getText()
            stars = table.find("div", {"class": "jsx-3292609844 text"}).getText()
            address = table.find("div", {"class": "jsx-3292609844 address-row"}).getText()
            contents += f"{title} \n此餐廳有{stars}顆星 \n地址: {address}\n\n"

        reply_token = event.reply_token
        send_text_message(reply_token, contents)
        self.go_back()

    def is_going_to_find_popular_ten(self, event):
        text = event.message.text
        return text.lower() == "popular"

    def on_enter_find_popular_ten(self, event):
        print("I'm entering find_newest_ten")

        reply_token = event.reply_token
        send_text_message(reply_token, "請輸入您想探索的縣市\n(注意:本搜尋不支援連江縣)")
    
    def is_going_to_print_popular_list(self, event):
        global area
        text = event.message.text
        if text == '基隆市' | text == '台北市' | text == '新北市' | text == '桃園市' | text == '新竹市' | text == '新竹縣' | text == '苗栗縣' | text == '台中市' | text == '彰化縣' | text == '雲林縣' | text == '嘉義市' | text == '嘉義縣' | text == '南投縣' | text == '台南市' | text == '高雄市' | text == '屏東縣' | text == '宜蘭縣' | text == '花蓮縣' | text == '台東縣' | text == '金門縣' | text == '澎湖縣':
            area = text
            return True
        return False

    def on_enter_print_popular_list(self, event):
        print("I'm entering print_popular_list")

        global area
        res = requests.get("https://ifoodie.tw/explore/" + area + "/list?sortby=popular&opening=true")
        soup = BeautifulSoup(res.content, "html.parser")
        tables = soup.find_all('div', {'class': 'jsx-3292609844 restaurant-info'}, limit=10)

        contents = ""
        for table in tables:
            title = table.find("a", {"class": "jsx-3292609844 title-text"}).getText()
            stars = table.find("div", {"class": "jsx-3292609844 text"}).getText()
            address = table.find("div", {"class": "jsx-3292609844 address-row"}).getText()
            contents += f"{title} \n此餐廳有{stars}顆星 \n地址: {address}\n\n"

        reply_token = event.reply_token
        send_text_message(reply_token, contents)
        self.go_back()



