# Teste Automatizado do módulo Database
# Atualizado: 12/11/2020
# Autor: Bruno Messeder dos Anjos

from mysql.connector import connect, Error

__all__ = ['execute', 'fetchall', 'close']

connection = None


def init():
    """
    Inicializa a conexão com o banco de dados.
    """
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
    """
    Executa um comando sql.

    :param sql: comando sql
    :return: True caso o comando tenha sido executado sem erros.
     False caso contrário.
    """
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
    """
    Executa um comando sql com fetchall.

    :param sql: comando sql
    :return: o resultado de fetchall, caso o comando sql tenha sido executado sem erros.
     None caso contrário.
    """
    try:
        cursor = connection.cursor()
        cursor.execute(sql)
        data = cursor.fetchall()
        cursor.close()
        return data
    except Error as e:
        print(f'Erro ao executar o comando \'{sql}\': {e.msg}')


def close():
    """
    Termina a conexão com o bando de dados.
    """
    global connection
    if connection:
        connection.close()
    connection = None


init()
