from .funcs import get_html, get_json, json_save


def get_directions(url: str) -> dict:
    """
    Собирает все направления

    Args:
        url (str): Страница со всеми направлениями

    Returns:
        list: Список ссылок на направления
    """
    data_json = get_json(url)
    links = data_json['competitions']
    return {link['title']: {'link': str(link['common']['listId'][0]),
                            'places': link['common']['plan']}
            for link in links if link.get('common')}


def get_table(dir_url: str, directions: dict) -> dict:
    """
    Собирает таблицу со всех направлений

    Args:
        dir_url (str): Основа url
        directions (dict): Список направлений

    Returns:
        dict: Таблица абитурьентов
    """
    data = {}
    for title, direction in directions.items():
        url = dir_url + direction['link']
        students = get_dir(url)
        data[title] = {"submitted": len(students),
                       "places": int(direction['places']),
                       "students": students}
    return data


def get_dir(url: str) -> tuple[str, dict]:
    """
    Возвращает абитурьентов с одного направления

    Args:
        url (str): Ссылка на направление

    Returns:
        dict: Словарь со студентами
    """

    def snils_format(snils):
        return ''.join(i for i in snils if i.isdigit())

    data = {}
    html = get_html(url)
    students = html.select('tr[id]')
    for student in students:
        snils = snils_format(student.select_one('td.fio').text)
        points = int(student.select('td.sum')[1].text)
        true_points = int(student.select('td.sum')[0].text)
        status = student.select_one('td.accepted').text == 'да'

        data[snils] = {'points': points,
                       'status': status,
                       'true_points': true_points}
    return data


def main(path):
    main_url = "https://priem.mirea.ru/accepted-entrants-list/"
    main_page = "getAllCompetitionsRates_p.php?place=moscow&form=och&level=bach"  # noqa: E501
    dir_url = "personal_code_rating.php?competition="
    directions = get_directions(main_url + main_page)
    table = get_table(main_url + dir_url, directions)
    json_save(table, path)


if __name__ == "__main__":
    main("../data_bases/MIREA.json")
