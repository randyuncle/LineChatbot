import bs4
import requests

from bs4 import BeautifulSoup
from abc import ABC, abstractmethod

"""
the abstract type of the restaurant finder
"""
class Options(ABC):
    
    def __init__(self, area):
        self.area = area

    @abstractmethod
    def options(self):
        pass


class Restaurant_popular(Options):

    def options(self):
        res = requests.get("https://ifoodie.tw/explore/" + self.area + "/list?sortby=popular&opening=true")
        soup = BeautifulSoup(res.content, "html.parser")
        tables = soup.find_all('div', {'class': 'jsx-3292609844 restaurant-info'}, limit=10)

        contents = ""
        for table in tables:
            title = table.find("a", {"class": "jsx-3292609844 title-text"}).getText()
            stars = table.find("div", {"class": "jsx-3292609844 text"}).getText()
            address = table.find("div", {"class": "jsx-3292609844 address-row"}).getText()
            contents += f"{title} \n此餐廳有{stars}顆星 \n地址: {address}\n\n"

        return contents



class Restaurant_rating(Options):

    def options(self):
        res = requests.get("https://ifoodie.tw/explore/" + self.area + "/list?sortby=rating&opening=true")
        soup = BeautifulSoup(res.content, "html.parser")
        tables = soup.find_all('div', {'class': 'jsx-3292609844 restaurant-info'}, limit=10)

        contents = ""
        for table in tables:
            title = table.find("a", {"class": "jsx-3292609844 title-text"}).getText()
            stars = table.find("div", {"class": "jsx-3292609844 text"}).getText()
            address = table.find("div", {"class": "jsx-3292609844 address-row"}).getText()
            contents += f"{title} \n此餐廳有{stars}顆星 \n地址: {address}\n\n"

        return contents