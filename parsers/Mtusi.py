from funcs import get_html, json_save,snils_format
import pyperclip


def get_directions():
    html = get_html(
        "https://lk.abitur.mtuci.ru/staticPage.php?page_name=spiski")
    budget = html.select_one('div.tabbed').select('a.lists-direction')
    return {direction.text:
            direction.get('data-direction-id') for direction in budget}


def get_table(directions):
    table = {}
    for title, index in directions.items():
        students = get_students(index)
        submitted = len(students)
        places = 0
        table[title] = {'submitted': submitted,
                        'places': places,
                        'students': students}
    return table


def get_students(dir_id):
    data = {'function': 'get_direction_list',
            'direction_id': dir_id,
            'type': 'uch'}
    # FIXME надо ещё получить neuch
    html = get_html("https://lk.abitur.mtuci.ru/ajax.php", data)
    data['type'] = 'neuch'
    html2 = get_html("https://lk.abitur.mtuci.ru/ajax.php", data)
    students = html.find_all('tr', class_='passed') + \
        html2.find_all('tr')[1:]
    all_students = {}
    for i in students:
        snils = snils_format(i.find_all('td')[2].text) 
        true_points = 0
        points = int(i.find_all('td')[8].text or 0)
        status = i.find_all('td')[10].text != 'Нет'
        all_students[snils] = {'points':points,'true_points':true_points,'status':status}
    return all_students


def main():
    directions = get_directions()
    table = get_table(directions)
    json_save(table, "../data_bases/MTUSI.json")


if __name__ == "__main__":
    main()
