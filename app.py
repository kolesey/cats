import sys
from operator import truediv

from classes import Cats
from classes import YaDisk
import requests
import json

FOLDER = 'PD-137'

token = input('Введите токен Яндекс Диска: ')
disk = YaDisk(token)

# Проверяем, есть ли папка на диске, если нет, создаем ее
try:
    if disk.create_folder(FOLDER) == False:
        print('Ошибка при создании папки на Яндекс Диске.')
        sys.exit()
    else:
        print('Папка успешно создана на Яндекс Диске.')
except requests.ConnectionError:
    print('Нет связи с Яндекс Диском')
    sys.exit()
except requests.Timeout:
    print(f'Превышено время ожидания ответа от Яндекс Диска')
    sys.exit()


while True:
    text = input('Введите текст: ')

    if text == '':
        print('Вы не ввели текст')
        text = input('Введите текст: ')

    # Создаем кота с подписью
    try:
        cat = Cats(text)
        print ('Создали кота.')
    except requests.ConnectionError:
        print(f'Нет связи с сервером cataas.com')
        break
    except requests.Timeout:
        print(f'Превышено время ожидания ответа от cataas.com')
        break

    # Получаем путь к изображению
    cat_url = cat.get_cat_url()

    # Формируем json c размером файла
    data = {
        'filesize': cat.get_cat_size()
    }

    # Загружаем json на диск, проверяя не существует ли такой файл уже на диске
    try:
        resp = disk.upload_file(f'/{FOLDER}/{text}.json', json.dumps(data))
        if resp == True:
            print('json загружен на Яндекс Диск')
        elif resp == 'FileExist':
            print('Кот с таким текстом уже существует.')
            continue
        else:
            print('Неизвестная ошибка при загрузке json файла на диск')
            break
    except requests.ConnectionError:
        print('Нет связи с Яндекс Диском')
        break
    except requests.Timeout:
        print(f'Превышено время ожидания ответа от Яндекс Диска')
        break


    # Формируем путь к файлу
    filename = f'/{FOLDER}/{text}.{cat.get_cat_extension()}'

    # Загружаем изображение кота с текстом на диск
    try:
        if disk.upload_file_by_url(filename, cat_url) == False:
            print('Ошибка при загрузке кота на Яндекс Диск.')
            break
        else:
            print('Кот успешно загружен на Яндекс Диск')
    except requests.ConnectionError:
        print('Нет связи с Яндекс Диском')
        break
    except requests.Timeout:
        print(f'Превышено время ожидания ответа от Яндекс Диска')
        break
    question = input('Продолжаем? y/n: ')
    if question == 'y':
        continue
    elif question == 'n':
        break
    else:
        question = input('Продолжаем? y/n: ')






