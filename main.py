from src.db_manager import DBManager
from src.utils import get_companies_info, create_database, save_data_to_database
from config import get_config



def main():

    params = get_config()

    create_database('companies_vacancy', **params)

    db_manager = DBManager(database="companies_vacancy", **params)
    companies = ['Яндекс', 'Сбербанк', 'VK', 'Газпром Нефть', 'Роснефть', 'Ростелеком', 'Mail.Ru Group', 'Wildberries',
                 'Аэрофлот', 'Rambler&Co']
    data = get_companies_info(companies)
    save_data_to_database(data, **params)




    while True:
        print('Добро пожаловать в систему вакансий!\n')

        print("Выберите пункт меню:\n"
              "1. Получить список всех компаний и количество вакансий у каждой компании.\n"
              "2. Получить список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию"
              "3. Узнать среднюю зарплату по всем вакансиям\n"
              "4. Получить список вакансий с зарплатой выше среднего уровня\n"
              "5. Поиск вакансий по ключевому слову\n"
              "6. Выйти")

        menu_item = input('Введите пункт меню: ')


        if menu_item == '1':
            #список всех компаний и количество вакансий у каждой компании
            companies_and_counts = db_manager.get_companies_and_vacancies_count()
            print(companies_and_counts)

        elif menu_item == '2':
            #список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию
            vacancies_and_companies = db_manager.get_all_vacancies()
            print(vacancies_and_companies)

        elif menu_item == '3':
            # Средняя зарплата по всем вакансиям
            average_salary = db_manager.get_avg_salary()
            print(f"Средняя зарплата: {average_salary}")

        elif menu_item == '4':
            # Вакансии с зарплатой выше среднего уровня
            higher_salary_vacancies = db_manager.get_vacancies_with_higher_salary()
            print(higher_salary_vacancies)

        elif menu_item == '5':
            # Поиск вакансий по ключевому слову
            keyword = input("Введите ключевое слово: ")
            python_vacancies = db_manager.get_vacancies_with_keyword(keyword)
            print(python_vacancies)

        elif menu_item == '6':
            # Выход из программы
            print("Выход из программы")
            db_manager.close()
            break
        else:
            print("Несуществующий пункт меню. Введите пункт меню из списка.")
if __name__ == '__main__':
    main()