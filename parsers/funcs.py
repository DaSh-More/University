import json
from time import sleep

import requests as req
from bs4 import BeautifulSoup as BS

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)\
AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.51 Safari/537.36'
}


def get_html(*url):
    while True:
        try:
            text = req.get(*url, headers=headers).text
            return BS(text, 'lxml')
        except req.ConnectionError:
            sleep(1)


def get_json(url):

    while True:
        try:
            text = req.get(url).json()
            return text
        except req.ConnectionError:
            sleep(1)


def json_save(obj, path):
    """
    Сохраняет словарь или список по указанному пути

    Args:
        obj (dict | list): Сохраняемая объект
        path (str): Путь к файлу
    """
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(obj, f, indent=4, ensure_ascii=False)


def snils_format(snils):
    """
    Форматирует снилс

    Args:
        snils (str): Снилс

    Returns:
        str: Отфармотированный снилс
    """
    return ''.join(i for i in snils if i.isdigit())
