from mysql.connector import connect, Error

__all__ = ['execute', 'execute_and_close']

connection = None


def init():
    global connection
    try:
        connection = connect(host='localhost', user='root', password='root')
        cursor = connection.cursor()
        cursor.execute('create database if not exists Modular')
        cursor.close()
        connection.close()
        connection = connect(host='localhost', database='Modular', user='root', password='root')
    except Error as e:
        print(f'Erro ao se conectar ao banco de dados: {e.msg}')


def execute(sql):
    try:
        cursor = connection.cursor()
        cursor.execute(sql)
        connection.commit()
        return cursor
    except Error as e:
        print(f'Erro ao executar o comando sql: {e.msg}')


def execute_and_close(sql):
    cursor = execute(sql)

    if not cursor:
        return False

    cursor.close()
    return True


def close():
    global connection
    if connection:
        connection.close()
    connection = None


init()
