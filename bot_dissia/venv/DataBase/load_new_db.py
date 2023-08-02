if __name__ == '__main__':
    import psycopg2
    from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

    # Устанавливаем соединение с postgres

    connection = psycopg2.connect(user="postgres", password="admin", port="4444")
    connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

    # Создаем курсор для выполнения операций с базой данных
    cursor = connection.cursor()
    # Создаем базу данных
    cursor.execute('create database mydatabase')
    # Закрываем соединение
    cursor.close()
    connection.close()