from src.database import create_database_if_not_exists, create_tables, populate_database, add_employee, add_vacancy, get_employees, get_vacancies
from src.api import APIManager
from src.db_manager import DBManager

def data_menu():
    while True:
        print("\nМеню работы с данными:")
        print("1. Добавить компанию")
        print("2. Добавить вакансию")
        print("3. Показать все компании")
        print("4. Показать все вакансии")
        print("5. Вернуться в главное меню")

        choice = input("Введите номер действия: ")

        if choice == "1":
            name = input("Название компании: ")
            add_employee(name)
            print("Компания добавлена!")

        elif choice == "2":
            title = input("Название вакансии: ")
            salary = int(input("Зарплата: "))
            companies = get_employees()
            if not companies:
                print("Компаний нет. Сначала добавьте компанию.")
                continue
            print("\nВыберите компанию для вакансии:")
            for c in companies:
                print(f"{c[0]}. {c[1]}")
            company_id = int(input("ID компании: "))
            add_vacancy(title, salary, company_id)
            print("Вакансия добавлена!")

        elif choice == "3":
            companies = get_employees()
            if companies:
                print("\nКомпании:")
                for c in companies:
                    print(f"ID: {c[0]}, Название: {c[1]}")
            else:
                print("Компаний нет.")

        elif choice == "4":
            vacancies = get_vacancies()
            if vacancies:
                print("\nВакансии:")
                for v in vacancies:
                    print(f"ID: {v[0]}, Название: {v[1]}, Зарплата: {v[2]}, Компания: {v[3]}")
            else:
                print("Вакансий нет.")

        elif choice == "5":
            break
        else:
            print("Неверный номер. Попробуйте снова.")

def main():
    print("Добро пожаловать в систему вакансий!\n")
    create_database_if_not_exists()

    while True:
        print("\nВыберите действие:")
        print("1. Создать таблицы и загрузить тестовые данные")
        print("2. Работа с данными")
        print("3. Вывести статистику (DBManager)")
        print("4. Получить компании и вакансии с hh.ru (APIManager)")
        print("5. Выйти")

        user_choice = input("Введите номер действия: ")

        if user_choice == "1":
            create_tables()
            populate_database()
            print("База и таблицы созданы, данные загружены.")
        elif user_choice == "2":
            data_menu()
        elif user_choice == "3":
            db = DBManager()
            print("\nКомпании и количество вакансий:")
            for row in db.get_companies_and_vacancies_count():
                print(row)
            print("\nВсе вакансии:")
            for row in db.get_all_vacancies():
                print(row)
            print("\nСредняя зарплата по всем вакансиям:")
            print(db.get_avg_salary())
            db.close()
        elif user_choice == "4":
            ids = input("Введите ID компаний через запятую: ")
            ids_list = [int(i.strip()) for i in ids.split(",") if i.strip().isdigit()]
            companies = APIManager.get_companies(ids_list)
            print(companies)
            if ids_list:
                for company_id in ids_list:
                    vacancies = APIManager.get_vacancies(company_id)
                    print(f"Вакансии компании {company_id}:")
                    for v in vacancies:
                        print(v)
        elif user_choice == "5":
            print("Выход из программы")
            break
        else:
            print("Неверный номер. Введите снова.")

if __name__ == "__main__":
    main()