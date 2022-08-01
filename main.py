from parsers import funcs, MIREA, MEI, Gubkin
from pathlib import Path


def wrap(name, func, path):
    print(f'Получение {name} ... ', end='')
    try:
        func(path)
        print('✔️')
    except Exception:
        print('❌')


universities = [[MIREA.main, './data_bases/MIREA.json', 'МИРЭА'],
                [MEI.main, './data_bases/MEI.json', 'МЭИ'],
                [Gubkin.main, './data_bases/Gubkin.json', 'Губкина']]

for func, path, name in universities:
    wrap(name, func, path)

for path in Path("./data_bases/").glob("*.json"):
    try:
        funcs.json2xlsx(
            path, (Path("./Excel/") / path.stem).with_suffix('.xlsx'))
    except:
        ...
