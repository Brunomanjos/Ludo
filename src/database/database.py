# Teste Automatizado do módulo Database
# Atualizado: 11/11/2020
# Autor: Bruno Messeder dos Anjos

from mysql.connector import connect, Error

__all__ = ['execute', 'fetchall', 'fetchone', 'close']

connection = None


def init():
    global connection
    try:
        connection = connect(host='localhost', user='root', password='root')
        cursor = connection.cursor()
        cursor.execute('CREATE DATABASE IF NOT EXISTS Modular')
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
        cursor.close()
        return True
    except Error as e:
        print(f'Erro ao executar o comando \'{sql}\': {e.msg}')
        return False


def fetchall(sql):
    try:
        cursor = connection.cursor()
        cursor.execute(sql)
        data = cursor.fetchall()
        cursor.close()
        return data
    except Error as e:
        print(f'Erro ao executar o comando \'{sql}\': {e.msg}')


def fetchone(sql):
    try:
        cursor = connection.cursor()
        cursor.execute(sql)
        data = cursor.fetchone()
        cursor.close()
        return data
    except Error as e:
        print(f'Erro ao executar o comando \'{sql}\': {e.msg}')


def close():
    global connection
    if connection:
        connection.close()
    connection = None


init()
