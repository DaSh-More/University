import json
from time import sleep
import pandas as pd

import requests as req
from bs4 import BeautifulSoup as BS

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)\
AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.51 Safari/537.36'
}


def get_html(*args, **kwargs):
    for _ in range(5):
        try:
            text = req.get(*args, **kwargs, headers=headers).text
            return BS(text, 'lxml')
        except req.ConnectionError:
            sleep(1)


def get_json(*args, **kwargs):

    for _ in range(5):
        try:
            text = req.get(*args, **kwargs).json()
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


def json2xlsx(path_to_json, path_to_xlsx):
    document = pd.ExcelWriter(path_to_xlsx)

    with open(path_to_json, encoding='utf-8') as f:
        json_table = json.load(f)

    for direction, data in json_table.items():
        students = data['students'].items()
        table = [{'Снилс': snils,
                  'Баллы': raw['points'],
                  'Согласие': raw['status'],
                  'Места': ''} for snils, raw in students]
        pd_table = pd.DataFrame(table, columns=['Снилс',
                                                'Баллы',
                                                'Согласие',
                                                'Места'])

        pd_table.loc[0, 'Места'] = data['places']
        pd_table.to_excel(document, sheet_name=direction, index=False)
    document.save()


def main():
    json2xlsx("../data_bases/MIREA.json", "../Excel/MIREA.xlsx")


if __name__ == "__main__":
    main()
