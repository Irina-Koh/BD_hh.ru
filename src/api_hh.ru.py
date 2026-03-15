from typing import List, Dict, Any

import requests

companies = ['Яндекс', 'Сбербанк', 'VK', 'Газпром Нефть', 'Роснефть', 'Ростелеком', 'Mail.Ru Group', 'Wildberries', 'Аэрофлот', 'Rambler&Co']
def get_companies() -> List[Dict[Any]]:
    '''
    Получение списка всех компаний
    :return: список компаний или пустой список
    '''
    for company_name in companies:
    # Отправляем запрос к API
        response = requests.get(f"https://api.hh.ru/employers?text={company_name}&per_page=1")

        if response.status_code == 200:
            data = response.json()
            items = data.get('items', [])

            if len(items) > 0:
                employer_data = items[0]
                print(f"Получены данные о работодателе: {employer_data['name']}")
            else:
                print(f"Работодатель '{company_name}' не найден.")
                return []
        else:
            print(f"Ошибка при запросе данных о работодателе: статус {response.status_code}.")
            return []

def get_vacancies(company_name: str) -> List[Dict[Any]]:
    '''
    Получение списка вакансий компании по ID
    :return: список вакансий
    '''

    vacancies_response = requests.get(f"https://api.hh.ru/vacancies?text={company_name}")
    if vacancies_response.status_code == 200:
        vacancies = vacancies_response.json()['items']
        if len(vacancies) > 0:
            print(f"Получено {len(vacancies)} вакансий {company_name}.")
        else:
            print(f"Вакансий {company_name} не найдено.")
            return []
    if vacancies_response.status_code != 200:
        print(f"Ошибка при запросе данных о вакансиях")
        return []