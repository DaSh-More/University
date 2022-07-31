from funcs import get_html, json_save
import json


def get_directions(url: str) -> list:
    """
    Собирает все направления

    Args:
        url (str): Страница со всеми направлениями

    Returns:
        list: Список ссылок на направления
    """
    html = get_html(url)
    links = html.select('table')[2].select('tr a')
    pattern = 'конкурсный список поступающих на основные места в рамках КЦП (бюджет, зачислениe'
    return [link.get('href') for link in links if pattern in link.text]


def get_table(main_url: str, directions: list) -> dict:
    """
    Собирает таблицу со всех направлений

    Args:
        main_url (str): Основа url
        directions (list): Список направлений

    Returns:
        dict: Табдила абитурьентов
    """
    data = {}
    for direction in directions:
        url = main_url + direction
        title, table = get_dir(url)
        data[title] = table
    return data


def get_dir(url: str) -> tuple[str, dict]:
    """
    Возвращает абитурьентов с одного направления

    Args:
        url (str): Ссылка на направление

    Returns:
        tuple[str, dict]: [
            Название направления
            Словарь со студентами
        ]
    """
    data = {}
    html = get_html(url)
    title = html.select_one('div.competitive-group').text
    students = html.select('tr.accepted')
    for student in students:
        snils = student.select_one('td[id]').get('id')[1:]
        points = int(student.find('td').text)
        true_points = int(student.select('td')[1].text)
        status = student.select('td[id]~td')[1].text == 'подано'
        data[snils] = {'points': points,
                       'status': status,
                       'true_points': true_points}
    return title, data


def save_table(table: dict | list, path: str):
    """
    Сохраняет таблицу по указанному путий

    Args:
        table (dict | list): Сохраняемая таблица
        path (str): Путь к файлу
    """
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(table, f, indent=4, ensure_ascii=False)


def main():
    main_url = "https://pk.mpei.ru"
    directions = get_directions(main_url + "/inform/list.html")
    table = get_table(main_url, directions)
    json_save(table, "../data_bases/MEI.json")


if __name__ == "__main__":
    main()
