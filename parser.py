import requests
from bs4 import BeautifulSoup
import os
import sqlite3


class Item:
    def __init__(self):
        self.title = ""
        self.text = ""

    def set_title(self, title):
        self.title = title

    def set_text(self, text):
        self.text = text

    def get_title(self):
        return self.title

    def get_text(self):
        return self.text

    def __str__(self):
        return f"New:\nTitle: {self.title};\nText: {self.text}"


class Parser:
    def __init__(self):
        self.items = []
        self.URL = "https://regnum.ru/news"
        self.HEADERS = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36"
        }

    def load_html(self):
        if os.path.exists("index.html"):
            return True
        response = requests.get(self.URL, headers=self.HEADERS)
        if response.status_code == 200:
            with open("index.html", "w", encoding="UTF-8") as f:
                f.write(response.text)
            return True
        return False

    @staticmethod
    def get_html():
        if os.path.exists("index.html"):
            with open("index.html", encoding="UTF-8") as f:
                return f.read()
        else:
            print("Load html")

    def get_items(self):
        soup = BeautifulSoup(self.get_html(), "lxml")
        items_list = soup.findAll("div", class_="news-item")
        for item in items_list:
            new_item = Item()
            title = item.find("div", class_="news-item_content").find("div", class_="news-header").find("a", class_="title").text
            text = item.find("div", class_="news-item_content").find("div", class_="news-anons").find("a", class_="anons").text
            new_item.set_title(title)
            new_item.set_text(text)
            self.items.append(new_item)

    def load_db(self):
        conn = sqlite3.connect('newsdb.db')
        cursor = conn.cursor()
        for item in self.items:
            cursor.execute('INSERT INTO news (title, text) VALUES (?, ?)', (item.get_title(), item.get_text()))
        conn.commit()
        conn.close()

    def __str__(self):
        result = ""
        for item in self.items:
            result += f"{item}\n"
        return result


def main():
    parser = Parser()
    parser.load_html()
    parser.get_items()
    parser.load_db()
    print(parser)


main()

