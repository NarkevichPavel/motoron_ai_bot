import datetime
import re

import requests
import fake_useragent
from bs4 import BeautifulSoup


class ParsingIDriver:
    login_link = 'https://idriver.by/ajax/forms/formLogin.php'
    user = fake_useragent.UserAgent().random

    headers = {
        'user-agent': user
    }

    data_for_login = {
        'login': '+375255416902',
        'pswrd1': '435091d'
    }

    def __init__(self):
        self.session = requests.Session()
        self.session.post(self.login_link, data=self.data_for_login, headers=self.headers)

    def requesting_data_for_updating_the_notes(self, article):
        scl = self.session.post(f'https://idriver.by/mylist/addpart?postID={article}')

        soup = BeautifulSoup(scl.text, 'lxml')

        form_data = {
            "ajaxDiv": "",
            "addPart": "",
            "carID": "",
            "clubID": "",
            "clubRowID": "",
            "carList": "",
            "number": "",
            "partCode": "",
            "brand": "",
            "model": "",
            "year": "",
            "body": "",
            "driveV": "",
            "kpp": "",
            "gas": "",
            "driveType": "",
            "cat": "",
            "D2": "",
            "J": "",
            "ET": "",
            "DIA": "",
            "hole": "",
            "PCD": "",
            "brandDisc": "",
            "serieID2": "",
            "D": "",
            "w": "",
            "h": "",
            "tireYear": "",
            "loadIndex": "",
            "type": "",
            "brandTyres": "",
            "serieID": "",
            "season": "",
            "remains": "",
            "notation": "",
            "txt": "",
            "price": "",
            "prop22": "",
            "sale": "",
            "currency": "",
            "quantity": "",
            "newPart": "",
            "video": "",
            "undOrder": "",
            "phones": "",
            "dop": "",
            "postID": ""
        }

        element = soup.find('div', 'leftCol')

        for key in form_data.keys():
            if key == 'txt':
                form_data[key] = element.find('textarea').text
                continue

            if key == 'dop':
                form_data[key] = f'Есть {datetime.date.today().strftime("%d.%m.%Y")}'
                continue

            value = element.find('input', {'name': key})

            if value:
                form_data[key] = value.get('value')
                continue

            values = element.find('select', {'name': key})

            if values:
                list_options = values.find_all('option')

                for value_option in list_options:
                    if value_option.get('selected') == '':
                        form_data[key] = value_option.get('value')
                        break

        update_data_request = self.session.post(f'https://idriver.by/mylist/addpart?postID={article}', data=form_data)
        return update_data_request

    def get_note(self, article):
        try:
            scl = self.session.post(f'https://idriver.by/mylist/addpart?postID={article}')

            soup = BeautifulSoup(scl.text, 'lxml')

            element = soup.find('div', 'leftCol')
            text = element.find('input', {'name': 'dop'}).get('value')
            return text

        except:
            return ''

    def get_last_action(self, article, date_find):
        try:
            url = f'https://idriver.by/ajax/clubsAdmin/quantity.php?params={article}ф&div=modal_content&url=https:/idriver.by/mylist?partFind={article}'

            response = self.session.get(url)
            soup = BeautifulSoup(response.text, 'lxml')
            div = (soup.find('div', 'tabelScroll'))
            data = div.find_all('tr')[1]

            id_row: str = data.attrs.get('id')

            id_span = id_row.replace('Row', '')
            action = data.find('span', id=id_span).text
            if 'Продажа:' in action:
                date_sale = data.find_all('td')[1].text
                date_pattern = r'\b\d{2}\.\d{2}\.\d{4}\b'

                # Поиск всех совпадений в строке
                matches = re.findall(date_pattern, date_find)
                date_find_formatted = datetime.datetime.strptime(matches[0], '%d.%m.%Y').strftime('%Y-%m-%d')

                if date_sale >= date_find_formatted:
                    date_object = datetime.datetime.strptime(date_sale.strip(), '%Y-%m-%d')
                    formatted_date = date_object.strftime('%d.%m.%Y')

                    return f'{formatted_date}'

            return ''

        except:
            return ''
