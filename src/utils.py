import os
from typing import List, Dict, Any
from config import get_config
import psycopg2
import requests

param = get_config()

company_names = ['Почта России', 'Сбербанк', 'VK', 'Газпром Нефть', 'Роснефть', 'Ростелеком', 'Mail.Ru Group', 'Wildberries',
                   'Аэрофлот', 'Rambler&Co']

def get_companies_info(company_names: List[str]) -> List[Dict[str, Any]]:
    data = []
    for company_name in company_names:
        # Поиск компании по названию
        search_response = requests.get(f"https://api.hh.ru/employers?text={company_name}&per_page=1")
        if search_response.status_code != 200:
            continue  # Пропускаем, если не удалось получить данные

        search_data = search_response.json()
        items = search_data.get('items', [])
        if not items:
            continue  # Пропускаем, если компания не найдена
        print(items)
        company_id = items[0]['id']
        vacancies_response = requests.get(f"https://api.hh.ru/vacancies?employer_id={company_id}&per_page=1")
        if vacancies_response.status_code == 200:
            vacancies_data = vacancies_response.json()
            print(vacancies_data)
            vacancies = vacancies_data.get('items', [])
            print(vacancies)


            data.append({
                'company': {
                'id': company_id,
                'name': company_name
                },
                'vacancies': vacancies
                })


    return data

def create_database(database_name: str, params: dict) -> None:
    """
    Создание базы данных и таблиц для сохранения данных о компаниях и вакансиях
    """
    conn = psycopg2.connect(**params)
    conn.autocommit = True
    cur = conn.cursor()
    cur.execute(f"DROP DATABASE IF EXISTS {database_name}")
    cur.execute(f'CREATE DATABASE {database_name}')
    cur.close()
    conn.close()
    conn = psycopg2.connect(**params)
    with conn.cursor() as cur:
        # Таблица компаний
        cur.execute('''
            CREATE TABLE IF NOT EXISTS employers (
                employer_id SERIAL PRIMARY KEY,
                );
        ''')

        # Таблица вакансий
        cur.execute('''
            CREATE TABLE IF NOT EXISTS vacancies (
                vacancy_id SERIAL PRIMARY KEY,
                company_name TEXT NOT NULL,
                title TEXT NOT NULL,
                salary_from FLOAT,
                salary_to FLOAT,
                currency TEXT,
                link_vacancy TEXT,
                employer_id INT REFERENCES employers(employer_id)
            );
        ''')
    conn.commit()
    conn.close()


def save_data_to_database(data: list[dict[str, Any]], database_name: str, params: dict) -> None:
    """Сохранение данных о компаниях и вакансиях в базу данных"""
    conn = psycopg2.connect(**params)
    with conn.cursor() as cur:
        for company in data:
            company_id = company['company']['id']
            company_name = company['company']['name']
            vacancy_list = company['vacancy']
            cur.execute(
                """
                INSERT INTO employers(company_id, company_name, vacancy_list)
                VALUES (%s, %s, %s)
                RETURNING employer_id
                """,
                (company_id, company_name, vacancy_list)
            )
            for vacancy in vacancy_list:
                vacansy_name = vacancy['name']
                vacansy_salary_from = vacancy['salary']['from']
                vacansy_salary_to = vacancy['salary']['to']
                vacansy_salary_currency = vacancy['salary']['currency']
                url_vacancy = vacancy['alternate_url']

            cur.execute(
                """
                INSERT INTO vacancies(vacancy_id, company_name, title, salary_from, salary_to, currency, link_vacancy, employer_id)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s
                """,
                (
                    company_name,
                    vacansy_name,
                    vacansy_salary_from,
                    vacansy_salary_to,
                    vacansy_salary_currency,
                    url_vacancy,
                    company_id
                )
            )

    conn.commit()
    conn.close()