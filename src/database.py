import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from config import DB_NAME, DB_USER, DB_PORT, DB_HOST, DB_PASSWORD


def create_database_if_not_exists():
    # Выводим их для проверки
    print("--- Параметры подключения к БД ---")
    print(f"DB_NAME: {DB_NAME}")
    print(f"DB_USER: {DB_USER}")
    print(f"DB_PASSWORD: {{'*' * len(DB_PASSWORD) if DB_PASSWORD else 'ПУСТО'}}")  # Скрываем пароль при выводе
    print(f"DB_HOST: {DB_HOST}")
    print(f"DB_PORT: {DB_PORT}")
    print("---------------------------------")

    # Если пароль пустой, лучше сразу вызвать ошибку
    if not DB_PASSWORD:
        raise ValueError("Переменная окружения DB_PASSWORD не установлена или пуста.")




    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            database="postgres",
            user=DB_USER,
            password=DB_PASSWORD,
            port=DB_PORT
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        with conn.cursor() as cur:
            cur.execute("SELECT 1 FROM pg_database WHERE datname=%s", (DB_NAME,))
            exists = cur.fetchone()
            if not exists:
                cur.execute(f"CREATE DATABASE {DB_NAME}")
                print(f"Создана база данных: {DB_NAME}")
            else:
                print(f"База данных {DB_NAME} уже существует")
    except Exception as e:
        print("Ошибка подключения к PostgreSQL:", e)
    finally:
        if 'conn' in locals():
            conn.close()


def get_db_connection():
    create_database_if_not_exists()
    return psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )


def create_tables():
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            # Удаляем старые таблицы
            cur.execute("DROP TABLE IF EXISTS vacancies CASCADE;")
            cur.execute("DROP TABLE IF EXISTS employees CASCADE;")

            # Создаем таблицу компаний
            cur.execute("""
                CREATE TABLE employees (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(255) NOT NULL
                )
            """)

            # Создаем таблицу вакансий
            cur.execute("""
                CREATE TABLE vacancies (
                    id SERIAL PRIMARY KEY,
                    title VARCHAR(255) NOT NULL,
                    salary INTEGER,
                    company_id INT REFERENCES employees(id)
                )
            """)
    print("Таблицы созданы")


def add_employee(name: str):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO employees (name) VALUES (%s)",
                (name,)
            )
            conn.commit()


def add_vacancy(title: str, salary: int, company_id: int):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO vacancies (title, salary, company_id) VALUES (%s, %s, %s)",
                (title, salary, company_id)
            )
            conn.commit()


def get_employees():
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM employees")
            return cur.fetchall()


def get_vacancies():
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT v.id, v.title, v.salary, e.name AS company
                    FROM vacancies v
                    JOIN employees e ON v.company_id = e.id
                """)
                return cur.fetchall()
    except Exception as e:
        print("Ошибка при получении вакансий:", e)
        return []


def populate_database():
    # Добавляем 10 компаний
    for i in range(1, 11):
        add_employee(f"Компания {i}")

    # Добавляем 10 вакансий для каждой компании
    for i in range(1, 11):
        add_vacancy(f"Вакансия {i}", 50000 + i*1000, i)

    print("База данных заполнена 10 компаниями и 10 вакансиями")