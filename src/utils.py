import os
from typing import List, Dict, Any
from config import config
import psycopg2
import requests

param = config()

def get_companies(companies: list[str]) -> List[Dict[str, Any]]:
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

def create_database(database_name: str, params: dict) -> None:
        '''Создание базы данных и таблиц для сохранения данных о компаниях и вакансиях'''

    try:
        # Подключаемся к PostgreSQL
        conn = psycopg2.connect()

        # Используем отдельный курсор для выполнения запросов
        with conn.cursor() as cur:

            # Устанавливаем autocommit режим для команды CREATE DATABASE
            conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)

            # Проверка наличия существующей базы данных
            cur.execute("SELECT 1 FROM pg_database WHERE datname=%s", (os.getenv('DB_NAME'),))
            exists = bool(cur.fetchone())

            if not exists:
                # Создаем базу данных, если её ещё нет
                cur.execute(f"CREATE DATABASE {os.getenv('DB_NAME')}")
                print(f"База данных {os.getenv('DB_NAME')} успешно создана.")
            else:
                print(f"База данных {os.getenv('DB_NAME')} уже существует.")

            # Возвращаем нормальный режим изоляции
            conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_READ_COMMITTED)

    except Exception as e:
        print("Ошибка:", str(e))
    finally:
        if 'conn' in locals():
            conn.close()


def get_vacancies(companies:list[str]) -> List[Dict[str, Any]]:
    '''
    Получение списка вакансий компании по ID
    :return: список вакансий
    '''
    for company_name in companies:
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

def create_tables():
    '''Создает таблицы в базе данных'''
    try:
        conn = psycopg2.connect()
        with conn.cursor() as cur:
            # Таблица работодателей
            cur.execute('''
                CREATE TABLE IF NOT EXISTS employers (
                    employer_id SERIAL PRIMARY KEY,
                    company_name TEXT NOT NULL UNIQUE,
                    industry TEXT,
                    website TEXT,
                    description TEXT
                );
            ''')

            # Таблица вакансий
            cur.execute('''
                CREATE TABLE IF NOT EXISTS vacancies (
                    vacancy_id SERIAL PRIMARY KEY,
                    title TEXT NOT NULL,
                    salary_from FLOAT,
                    salary_to FLOAT,
                    currency TEXT,
                    area TEXT,
                    experience_required BOOLEAN,
                    created_at TIMESTAMPTZ,
                    employer_id INT REFERENCES employers(employer_id)
                );
            ''')
        conn.commit()
    except Exception as e:
        print("Ошибка при создании таблиц:", str(e))
    finally:
        if 'conn' in locals():
            conn.close()


def insert_employer(cursor, data):
    """Вставляет запись о работодателе"""
    try:
        cursor.execute(
            """
            INSERT INTO employers(company_name, description, website)
            VALUES (%s, %s, %s)
            ON CONFLICT DO NOTHING;
            """,
            (data['name'], data.get('description', '')[:100], data.get('website'))
        )
    except Exception as e:
        print(f"Ошибка при вставке работодателя: {e}")


def insert_vacancy(cursor, vacancy, employer_id):
    """Вставляет запись о вакансии"""
    try:
        cursor.execute(
            """
            INSERT INTO vacancies(title, salary_from, salary_to, currency, area, experience_required, created_at, employer_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT DO NOTHING;
            """,
            (
                vacancy['name'],
                vacancy.get('salary', {}).get('from'),
                vacancy.get('salary', {}).get('to'),
                vacancy.get('salary', {}).get('currency'),
                vacancy.get('area', {}).get('name'),
                vacancy.get('experience', {}).get('id') != 'noExperience',
                vacancy.get('created_at'),
                employer_id
            )
        )
    except Exception as e:
        print(f"Ошибка при вставке вакансии: {e}")

