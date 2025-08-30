import json
import requests

class Cats:
    CAT_URL = 'https://cataas.com'

    def __init__(self, text):
        self.text = text
        self.json = self._get_image_json()

    def get_cat_id(self):
        """
        Метод возвращает ID созданного изображения
        :return: ID созданного изображения
        """
        return self.json['id']

    def get_cat_extension(self):
        """
        Метод возвращает расширение созданного изображения
        :return: расширение созданного изображения
        """
        mimetype = self.json['mimetype']
        return mimetype.split('/')[-1]

    def get_cat_size(self):
        """
        Метод получает размер созданного изображения
        :return: размер созданного изображения в байтах
        """
        response = requests.get(self.get_cat_url())
        return response.headers.get('Content-Length')

    def get_cat_url(self):
        """
        Метод возвращает url созданного изображения
        :return: url созданного изображения
        """
        return f'{self.CAT_URL}/cat/{self.get_cat_id()}/says/{self.text}'
        # return self.json['url']


    def _get_image_json(self):
        url = f'{self.CAT_URL}/cat/says/{self.text}'
        params = {
            'json': 'true'
        }

        response = requests.get(url, params=params)
        return response.json()



class YaDisk:
    YD_URL = 'https://cloud-api.yandex.net/v1/disk/resources'

    def __init__(self, token):
        self.token = token
        self.headers = {
            'Authorization': 'OAuth ' + self.token
        }

    def check_folder(self, folder_name):
        """
        Метод проверяет наличие папки на Яндекс диске
        :param folder_name: имя папки
        :return: True если папка есть. False если папки нет
        """

        params = {
            'path': folder_name
        }

        response = requests.get(self.YD_URL, params=params, headers=self.headers)

        if response.status_code == 200:
            return True
        else:
            return False


    def save_file_info(self, disk_path, output_file):
        """
        Метод записывает информацию по запрашиваемому на яндекс диске файлу
        :param disk_path: путь к файлу на яндекс диске
        :param output_file: имя файла для записи результата
        :return: HTTP код ответа Яндекс Диска
        """
        params = {
            'path': disk_path
        }

        response = requests.get(self.YD_URL, params=params, headers=self.headers)

        if response.status_code == 200:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(response.json(), f)
                f.flush()
            return response.status_code
        else:
            return response.status_code



    def create_folder(self, folder_name):
        """
        Метод создает папку на яндекс диске
        :param folder_name: Имя папки
        :return: True если папка создана или уже существовала на диске. False если возникли проблемы
        """

        params = {
            'path': folder_name
        }

        # Если такой папки не существует, то создаем ее
        if self.check_folder(folder_name) == False:
            response = requests.put(self.YD_URL, params=params, headers=self.headers)
            if response.status_code == 201:
                return True
            else:
                return False
        # Если папка существует, то ничего не делаем
        else:
            return True

    def upload_file_by_url(self, filename, file_url):
        """
        Метод загружает файл на диск по переданному url изображения
        :param filename: путь и имя файла который загружается на диск
        :param file_url: url изображения
        :return: True если файл загружен.
        """
        url = self.YD_URL + '/upload'
        params = {
            'path': filename,
            'url': file_url
        }
        response = requests.post(url, params=params, headers=self.headers)
        if response.status_code == 202:
            return True
        else:
            return False

    def get_upload_url(self, path):
        """
        Метод создает ссылку для загрузки файла на диск
        :param path: путь с именем файла на диске
        :return: json ответ сервера
        """
        url = self.YD_URL + '/upload'
        params = {
            'path': path,

        }
        response = requests.get(url, params=params, headers=self.headers)

        return response.json()

    def upload_file(self, path, file):
        """
        Метод загружает файл на диск
        :param path: путь с именем файла на диске
        :param file: файл для загрузки
        :return: 'FileExist' если файл уже существует. True если файл загрузился
        """
        upload_url_dict = self.get_upload_url(path)
        if upload_url_dict.get('error') == 'DiskResourceAlreadyExistsError':
            return 'FileExist'
        elif upload_url_dict.get('href', '') == '':
            return False
        else:
            upload_url = upload_url_dict.get('href')
        response = requests.put(upload_url, files={'file': file})
        if response.status_code == 201:
            return True
        else:
            return False
