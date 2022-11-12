# Модуль работы с SQL
import sqlite3 as sql


def sql_run(sql_request: str):
    """ Выполняет все SQL запросы. Принимает строку с запросом. """
    with sql.connect('bali_cinema.db') as connect_db:
        cursor_db = connect_db.cursor()
        cursor_db.execute(sql_request)
        return cursor_db.fetchall()


def sql_User_contained(name: str):
    """ Проверяет есть ли такой пользователь в базе. """
    sql_result = sql_run(f"SELECT * FROM users;")    

    for i in sql_result:
        id = i[0]
        if id == name:
            print(id + ' - содержится в базе')    
            return False # пользователь не новый
    return True


def sql_add_NewUser(id: str):
    """ Добавляет нового пользователя в БД. """
    sql_run(f"INSERT INTO users (id) VALUES('{id}');")
    # print ('Добавлен новый Юзер: ' + id)
    # logging.info('Текушие данный пользователя:')


def sql_change_userData(id: str, column: str, values: str):
    """ Изменяет данные пользователя в БД.
    id - id пользователя, column - колонка в таблице, values - значение. """
    sql_run(f"UPDATE users SET {column} = '{values}' WHERE id = {id};")
    

# тестирование
if __name__ == '__main__':

    # user = str(input('userID: '))
    # if sql_User_contained(user):
    #     sql_add_NewUser(user)

    sql_change_userData('5461985809', 'status', None)