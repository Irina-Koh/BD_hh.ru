from configparser import ConfigParser


def get_config(filename='database.ini', section='postgresql'):
    """Читает конфигурацию и преобразует типы данных."""
    parser = ConfigParser()
    parser.read(filename, encoding='utf-8')

    if not parser.has_section(section):
        raise Exception(f'Секция {section} не найдена в файле {filename}')

    # Получаем все параметры как словарь строк
    db_config = dict(parser.items(section))

    # --- НАЧАЛО БЛОКА ПРЕОБРАЗОВАНИЯ ---
    # Список параметров, которые должны быть числами
    int_params = ['port']

    for param in int_params:
        if param in db_config and db_config[param]:
            try:
                db_config[param] = int(db_config[param])
            except ValueError:
                raise ValueError(f"Параметр '{param}' должен быть целым числом.")

    # Если есть другие параметры (например, timeout), их можно добавить сюда
    # float_params = ['timeout']
    # for param in float_params:
    #     if param in db_config and db_config[param]:
    #         db_config[param] = float(db_config[param])
    # --- КОНЕЦ БЛОКА ПРЕОБРАЗОВАНИЯ ---

    return db_config