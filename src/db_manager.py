
import psycopg2

from config import config


class DBManager:
    def __init__(self):
        params = config()
        self.conn = psycopg2.connect(**params)
        self.conn.autocommit = True

    def get_companies_and_vacancies_count(self):
        """Список всех компаний и количество вакансий у каждой"""
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT c.name, COUNT(v.id)
                FROM companies c
                LEFT JOIN vacancies v ON c.id = v.company_id
                GROUP BY c.name;
            """)
            return cur.fetchall()

    def get_all_vacancies(self):
        """Все вакансии: компания, вакансия, зарплата, ссылка"""
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT c.name, v.title, v.salary_from, v.url
                FROM vacancies v
                JOIN companies c ON v.company_id = c.id;
            """)
            return cur.fetchall()

    def get_avg_salary(self):
        """Средняя зарплата по всем вакансиям"""
        with self.conn.cursor() as cur:
            cur.execute("SELECT AVG(salary_from) FROM vacancies WHERE salary_from IS NOT NULL;")
            return cur.fetchone()[0]

    def get_vacancies_with_higher_salary(self):
        """Вакансии с зарплатой выше средней"""
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT c.name, v.title, v.salary_from, v.url
                FROM vacancies v
                JOIN companies c ON v.company_id = c.id
                WHERE v.salary_from > (SELECT AVG(salary_from) FROM vacancies WHERE salary_from IS NOT NULL);
            """)
            return cur.fetchall()

    def get_vacancies_with_keyword(self, keyword: str):
        """Вакансии, где в названии есть слово (например Python)"""
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT c.name, v.title, v.salary_from, v.url
                FROM vacancies v
                JOIN companies c ON v.company_id = c.id
                WHERE v.title ILIKE %s;
            """, (f"%{keyword}%",))
            return cur.fetchall()

    def close(self):
        self.conn.close()