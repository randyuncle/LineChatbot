from transitions.extensions import GraphMachine

from bs4 import BeautifulSoup
import requests
from linebot.models import ImageCarouselColumn, URITemplateAction, MessageTemplateAction

from utils import send_text_message, send_button_message

#global variable
area = ''
item = ''

class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(model=self, **machine_configs)

    def is_going_to_information(self, event):
        text = event.message.text
        return text.lower() == "information"

    def on_enter_information(self, event):
        print("I'm entering information")

        reply_token = event.reply_token

        send_text_message(reply_token, "歡迎來到資訊頁面！\n\n＊本機器人的餐廳資料來源 - 愛食記\n＊本機器人的搜查到的所有餐廳皆是已營業的部分\n\n技術方面: \n1. 本機器人是以 finite state machine 來運作的，用來保障使用者輸入的資料都是符合本機器人的要求，才會繼續進行下去。\n2. 此機器人是以 python 來建置的，其中以 pipenv 來運行 flask server，防止本地環境遭到變動。\n3. 網路爬蟲技術是用 beautifulsoup4 模組來完成的\n4. 本程式只能由 ngrok 本地端來運行，沒有做 serverless 上的架設（主因是沒錢，但有免費的平台也沒看動怎麼架）\n\n指令詳細說明:\n1. rating: 在輸入\"rating\"後，本機器人會要您再額外輸入您所要查找的縣市(必填)，以及您想尋找的品類項目(可不填)，以可從該縣市中尋找愛食記中評分前10的店家\n2. popular: 在輸入\"popular\"後，本機器人會要您再額外輸入您所要查找的縣市(必填)，以及您想尋找的品類項目(可不填)，以可從該縣市中尋找愛食記中人氣前10的店家\n3. information: 顯示本訊息\n4. reset: 可在任何狀態使用，只要觸發就會回到初始狀態\n")
        self.go_back()

    def is_going_to_input_rating_area(self, event):
        text = event.message.text
        return text.lower() == "rating"

    def on_enter_input_rating_area(self, event):
        print("I'm entering input_rating_area")

        reply_token = event.reply_token
        send_text_message(reply_token, "請輸入您想探索的縣市\n(注意:本搜尋不支援連江縣)")
    
    def is_going_to_input_rating_item(self, event):
        global area
        text = event.message.text
        if text == '基隆市' or text == '台北市' or text == '新北市' or text == '桃園市' or text == '新竹市' or text == '新竹縣' or text == '苗栗縣' or text == '台中市' or text == '彰化縣' or text == '雲林縣' or text == '嘉義市' or text == '嘉義縣' or text == '南投縣' or text == '台南市' or text == '高雄市' or text == '屏東縣' or text == '宜蘭縣' or text == '花蓮縣' or text == '台東縣' or text == '金門縣' or text == '澎湖縣':
            area = text
            return True
        return False

    def on_enter_input_rating_item(self, event):
        print("I'm entering input_rating_item")

        reply_token = event.reply_token
        send_text_message(reply_token, "請輸入您想吃的美食種類\n若不要的話則輸入\"無\"\n\n本欄支援的種類:\n火鍋、\n日式、\n燒肉、\n精緻高級、\n早午餐、\n甜點類、\n約會餐廳類、\n韓式、\n餐酒館/酒吧、\n居酒屋")


    def is_going_to_print_rating_list(self, event):
        global item
        text = event.message.text
        if text == '火鍋' or text == '日式' or text == '燒肉' or text == '精緻高級' or text == '早午餐' or text == '甜點類' or text == '約會餐廳類' or text == '韓式' or text == '餐酒館/酒吧' or text == '居酒屋':
            item = text
            return True
        elif text == '無':
            item = ''
            return True
        return False

    def on_enter_print_rating_list(self, event):
        print("I'm entering print_best_list")

        global area, item
        res = ''
        if item == '':
            res = requests.get("https://ifoodie.tw/explore/" + area + "/list?sortby=rating&opening=true")
        else:
            res = requests.get("https://ifoodie.tw/explore/" + area + "/list/" + item + "?sortby=rating&opening=true")
        soup = BeautifulSoup(res.content, "html.parser")
        tables = soup.find_all('div', {'class': 'jsx-3292609844 restaurant-info'}, limit=10)

        contents = ""
        for table in tables:
            title = table.find("a", {"class": "jsx-3292609844 title-text"}).getText()
            stars = table.find("div", {"class": "jsx-1207467136 text"}).getText()
            #costs = table.find("div", {"class": "jsx-3292609844 avg-price"}).getText()
            address = table.find("div", {"class": "jsx-3292609844 address-row"}).getText()
            contents += f"{title} \n此餐廳有{stars}顆星\n地址: {address}\n\n"

        reply_token = event.reply_token
        send_text_message(reply_token, contents)
        self.go_back()

    def is_going_to_input_popular_area(self, event):
        text = event.message.text
        return text.lower() == "popular"

    def on_enter_input_popular_area(self, event):
        print("I'm entering input_popular_area")

        reply_token = event.reply_token
        send_text_message(reply_token, "請輸入您想探索的縣市\n(注意:本搜尋不支援連江縣)")

    def is_going_to_input_popular_item(self, event):
        global area
        text = event.message.text
        if text == '基隆市' or text == '台北市' or text == '新北市' or text == '桃園市' or text == '新竹市' or text == '新竹縣' or text == '苗栗縣' or text == '台中市' or text == '彰化縣' or text == '雲林縣' or text == '嘉義市' or text == '嘉義縣' or text == '南投縣' or text == '台南市' or text == '高雄市' or text == '屏東縣' or text == '宜蘭縣' or text == '花蓮縣' or text == '台東縣' or text == '金門縣' or text == '澎湖縣':
            area = text
            return True
        return False

    def on_enter_input_popular_item(self, event):
        print("I'm entering input_popular_item")

        reply_token = event.reply_token
        send_text_message(reply_token, "請輸入您想吃的美食種類\n若不要的話則輸入\"無\"\n\n本欄支援的種類:\n火鍋、\n日式、\n燒肉、\n精緻高級、\n早午餐、\n甜點類、\n約會餐廳類、\n韓式、\n餐酒館/酒吧、\n居酒屋")

    
    def is_going_to_print_popular_list(self, event):
        global item
        text = event.message.text
        if text == '火鍋' or text == '日式' or text == '燒肉' or text == '精緻高級' or text == '早午餐' or text == '甜點類' or text == '約會餐廳類' or text == '韓式' or text == '餐酒館/酒吧' or text == '居酒屋':
            item = text
            return True
        elif text == '無':
            item = ''
            return True
        return False

    def on_enter_print_popular_list(self, event):
        print("I'm entering print_popular_list")

        global area, item
        res = ''
        if item == '':
            res = requests.get("https://ifoodie.tw/explore/" + area + "/list?sortby=popular&opening=true")
        else:
            res = requests.get("https://ifoodie.tw/explore/" + area + "/list/" + item + "?sortby=popular&opening=true")
        soup = BeautifulSoup(res.content, "html.parser")
        tables = soup.find_all('div', {'class': 'jsx-3292609844 restaurant-info'}, limit=10)

        contents = ""
        for table in tables:
            title = table.find("a", {"class": "jsx-3292609844 title-text"}).getText()
            stars = table.find("div", {"class": "jsx-1207467136 text"}).getText()
            #costs = table.find("div", {"class": "jsx-3292609844 avg-price"}).getText()
            address = table.find("div", {"class": "jsx-3292609844 address-row"}).getText()
            contents += f"{title} \n此餐廳有{stars}顆星\n地址: {address}\n\n"

        reply_token = event.reply_token
        send_text_message(reply_token, contents)
        self.go_back()



