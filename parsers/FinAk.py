from funcs import get_json, json_save, snils_format


def get_directions(api: str):
    data = get_json(api, {'act': 'search',
                          'method': 'getFaculties',
                          'form_id': 1})['data']

    data = get_json(api, {'act': 'search',
                          'method': 'getGroups',
                          'form_id': data[0]['form_id'],
                          'facid': data[0]['facid']})['data']

    return {direction['speciality_name']:
            {'places': direction['amount'],
             'data': {'id_con': direction['id_con'],
                      'quaid': direction['quaid']}} for direction in data}


def get_table(api: str, directions):
    table = {}
    for title, direction in directions.items():
        students = get_students(api, direction['data'])
        table[title] = {'submitted': len(students),
                        'places': direction['places'],
                        'students': students}
    return table


def get_students(api: str, direction):
    students = {}
    data = get_json(api, {'act': 'search', 'type': 0} | direction)
    for student in data['data']['data']:
        students[snils_format(student['name'])] = {
            "points": student['sum'],
            "true_points": student['sum_vstup_ball'],
            "status": student['consent_to_enrollment'] == 'Согл'
        }
    return students


def main():
    api = "https://lk.priem.gubkin.ru/abiturients_list/api/api.php"
    directions = get_directions(api)
    table = get_table(api, directions)
    json_save(table, "../data_bases/FinAk.json")


if __name__ == "__main__":
    main()
