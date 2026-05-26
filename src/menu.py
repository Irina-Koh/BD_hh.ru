from src.database import add_employee, add_vacancy, get_employees, get_vacancies


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
            name = input("Введите название компании: ")
            add_employee(name)

        elif choice == "2":
            title = input("Введите название вакансии: ")
            salary = int(input("Введите зарплату: "))

            companies = get_employees()
            if not companies:
                print("Нет компаний. Сначала добавьте компанию.")
                continue

            print("\nВыберите компанию для вакансии:")
            for emp in companies:
                print(f"{emp[0]}. {emp[1]}")

            company_id = int(input("Введите ID компании: "))
            add_vacancy(title, salary, company_id)

        elif choice == "3":
            employees = get_employees()
            if employees:
                print("\nКомпании:")
                for emp in employees:
                    print(f"ID: {emp[0]}, Название: {emp[1]}")
            else:
                print("Компаний нет.")

        elif choice == "4":
            vacancies = get_vacancies()
            if vacancies:
                print("\nВакансии:")
                for vac in vacancies:
                    print(f"ID: {vac[0]}, Должность: {vac[1]}, Зарплата: {vac[2]}, Компания: {vac[3]}")
            else:
                print("Вакансий нет.")

        elif choice == "5":
            break
        else:
            print("Неверный ввод, попробуйте снова.")