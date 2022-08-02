import json
from pathlib import Path

from rich.console import Console
from rich.table import Table
from parsers.funcs import snils_format
from analysis import rating as student_rating


def get_universityies():
    universities_path = Path("./data_bases/").glob("*.json")

    universities = {}
    for university in universities_path:
        with open(university, encoding='utf-8') as f:
            univ = json.load(f)
        for direction in univ:
            students = []
            for key, value in univ[direction]['students'].items():
                students.append({'snils': key} | value)
            univ[direction]['students'] = students
            univ[direction]['title'] = direction
        universities[university.stem] = univ
    return universities


class UniversityAnalysis:

    console = Console()
    universities = {}

    def __init__(self, snils):
        snils = snils_format(snils)
        self.me = {'points': 268,
                   'snils': snils}

    def get_table(self, direction: dict, rating: int) -> Table:

        table = Table(title=direction['title'], show_lines=True)

        table.add_column("Описание", justify="center")
        table.add_column("Баллы", justify="center")
        table.add_column("Количество", justify="center")
        table.add_column("Примечание", justify="center")

        # HACK Указать рейтинг
        data_table = self.analysis(direction, rating)
        colors = ['#ff8800', 'red', 'green', 'yellow', None]
        for n, raw in enumerate(data_table):
            table.add_row(*raw, style=colors[n])

        return table

    def analysis(self, direction: dict, rating: int) -> list:
        data_table = [['Лучше и не подали согласие'],
                      ['Лучше и подали согласие'],
                      ['Хуже и подали согласие'],
                      ['Хуже и не подали согласие']]

        # more: accepted: [min, max], !accepted: [min, max], less [...]
        students = [[], [], [], []]

        for student in direction['students'].values():
            # 1 - less, 0 - more
            more_or_less = str(int(self.me['points'] > student['points']))
            status = str(int(not student['status']))
            students[int(more_or_less + status, 2)].append(student['points'])
        students[0], students[1] = students[1], students[0]
        for n, i in enumerate(students):
            i.sort()
            if not i:
                i.append(0)
            data_table[n].append(f'{i[0]} - {i[-1]}')
            data_table[n].append(str(len(i)))
        add_students = student_rating(students[0], rating) or 0
        accepted_best = int(data_table[1][-1])
        text = f'+{add_students} ({add_students + accepted_best}/{direction["places"]})'  # noqa
        data_table[0].append(text)
        data_table[1].append(f'{accepted_best}/{direction["places"]}')
        vacant = direction["places"] - accepted_best - add_students
        data_table[2].append(str(vacant))
        indexes = [10, 15, 20]
        if len(students[0]) + accepted_best < direction["places"]:
            chance = '✔️'
        else:
            score = sum(vacant > i for i in indexes)
            chance = '❌❓❔✅'[score]
        data_table[3].append(chance)
        return data_table

    def open_university(self, path):
        path = Path(path)
        with open(path, encoding='utf-8') as f:
            univ = json.load(f)
        for direction in univ:
            if direction == 'rating':
                continue
            students = {}
            for key, value in univ[direction]['students'].items():
                students[key] = {'snils': key} | value
            univ[direction]['students'] = students
            univ[direction]['title'] = direction
        self.universities[path.stem] = univ

    def print_universities(self):
        for title, unv in self.universities.items():
            rating = unv['rating']
            print(rating)
            del unv['rating']
            self.console.rule(title)
            for direction in unv.values():
                if snils in direction['students']:
                    table = self.get_table(direction, rating)
                    self.console.print(table)
                    print()


snils = input('СНИЛС: ')
# snils = '18727017893'
university = UniversityAnalysis(snils)
for path in Path("./data_bases/").glob("*.json"):
    university.open_university(path)
university.print_universities()
