from typing import List, Tuple
import psycopg2
from typing import Optional


class DBManager:
    def __init__(self, database: str, user: str, password: str, host: str, port: int = 5432,
                 table_name: str = 'company_and_vacancy'):
        """
        Конструктор класса для управления соединением с БД.
        """
        self.table_name = table_name
        self.conn = psycopg2.connect(
            dbname=database,
            user=user,
            password=password,
            host=host,
            port=port
        )

        self.cur = self.conn.cursor()
        print("Соединение успешно установлено.")
        self.create_table()

    def get_companies_and_vacancies_count(self) -> List[Tuple]:
        """Возвращает список всех компаний и количество вакансий у каждой компании."""
        self.cur.execute("""
            SELECT company_name, COUNT(*) AS vacancies_count
            FROM employers JOIN vacancies USING (employer_id)
            GROUP BY company_id;
        """)
        return self.cur.fetchall()

    def get_all_vacancies(self) -> List[Tuple]:
        """Возвращает список всех вакансий с названием компании, названием вакансии, зарплатой и ссылкой на вакансию."""
        self.cur.execute("""
            SELECT company_name, title, CONCAT(salary_from, '-', salary_to) AS salary_range, link_vacancy
            FROM employers JOIN vacancies USING (employer_id);
        """)
        return self.cur.fetchall()

    def get_avg_salary(self) -> float:
        """Возвращает среднюю зарплату по всем вакансиям."""
        self.cur.execute("""
            SELECT AVG((salary_from + salary_to)/2) 
            FROM vacancies 
            WHERE salary_from IS NOT NULL AND salary_to IS NOT NULL;
        """)
        result = self.cur.fetchone()[0]
        return round(result, 2) if result is not None else 0

    def get_vacancies_with_higher_salary(self) -> List[Tuple]:
        """Возвращает список вакансий с зарплатой выше средней."""
        avg_salary = self.get_avg_salary()
        self.cur.execute(f"""
            SELECT * 
            FROM vacancies 
            WHERE ((salary_from + salary_to)/2 > %s) OR (salary_from > %s);
        """, (avg_salary, avg_salary))
        return self.cur.fetchall()

    def get_vacancies_with_keyword(self, keyword: str) -> List[Tuple]:
        """Возвращает список вакансий, содержащих указанное ключевое слово в названии."""
        self.cur.execute(f"""
            SELECT * 
            FROM vacancies 
            WHERE LOWER(title) LIKE %s;
        """, ('%' + keyword.lower() + '%',))
        return self.cur.fetchall()

