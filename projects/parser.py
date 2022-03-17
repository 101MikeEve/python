from datetime import date
import math
import requests
import fake_useragent
import re
import xlsxwriter

from bs4 import BeautifulSoup
from requests.sessions import Session
from xlsxwriter.worksheet import Worksheet


BASE_URL = f'https://search.kodeks.ru/monitoring'
USER_EMAIL = f'hr5@bravosoft.nnov.ru'
USER_PASSWORD = f'alenas1996'
USER_AGENT = fake_useragent.UserAgent().random
LOG_FILE = '{}.log'.format(date.today())

# Writing headers to output spreadsheet
def writeHeaders(worksheet: Worksheet):
    worksheet.write(0, 0, 'Название')
    worksheet.write(0, 1, 'ИНН')
    worksheet.write(0, 2, 'Статус')
    worksheet.write(0, 3, 'Закрепление')
    worksheet.write(0, 4, 'Дата стоп-листа')
    worksheet.write(0, 5, 'Штат')
    worksheet.write(0, 6, 'Выручка')
    worksheet.write(0, 7, 'Сегмент')
    return worksheet


# Authorization in Search
def auth(user_email: str = USER_EMAIL, user_password: str = USER_PASSWORD) -> Session:
    s = requests.Session()
    payload = {
        'email': user_email,
        'password': user_password
    }

    s.post(url=f'https://my.kodeks.ru/cas/auth',
           headers={'user-agent': USER_AGENT}, data=payload)
    return s


# Getting maximum organization count in Search
def getTotal(s: Session) -> int:
    res = s.get(url=BASE_URL,
                params={'query': f'стоп-лист'}, headers={'user-agent': USER_AGENT})

    soup = BeautifulSoup(res.text, 'lxml')
    main = soup.find('main', id="content")

    total = re.findall(
        r'\d+', main.select_one('.client-groups-font').findChild('b').text)[0]

    return int(total)


# helping handler from clear string
def __clearStr(str: str) -> str:
    return str.replace("\s+", '').replace("\n", '')


# main
def main() -> None:
    workbook = xlsxwriter.Workbook('{} стоп-лист.xlsx'.format(date.today()))
    worksheet = writeHeaders(workbook.add_worksheet())
    row = 1
    s = auth()

    limit: int = int(200)
    total: int = getTotal(s)

    for offset in range(0, total, limit):
        params = {
            'query': f'стоп-лист',
            'limit': limit,
            'offset': offset
        }

        res = s.get(url=BASE_URL, params=params,
                    headers={'user-agent': USER_AGENT})

        soup = BeautifulSoup(res.text, 'lxml')
        companyList = soup.find_all(
            'div', attrs={'class': 'row company-card item card-shadow'})

        for company in companyList:
            name = __clearStr(company.find('full-name').text)
            inn = __clearStr(company.find('inn').text)
            stopList = __clearStr(re.findall(r'\d\d.\d\d.\d\d\d\d', company.find(
                'div', attrs={'class': 'row'}).text)[0])
            statusAndPin = __clearStr(company.find(
                'div', attrs={'class': 'col-sm-12 col-md-4'}).text).split('\xa0')

            status = statusAndPin[0].replace(' ', '')

            try:
                pin = statusAndPin[1]
            except IndexError:
                pin = 'нет'

            worksheet.write(row, 0, name)
            worksheet.write(row, 1, inn)
            worksheet.write(row, 2, status)
            worksheet.write(row, 3, pin)
            worksheet.write(row, 4, stopList)

            row += 1

    workbook.close()

if __name__ == "__main__":
    main()
