import mysql.connector as sql
from tkinter import messagebox

def create_tables():
    _MYSQL_PASSWORD = "root"

    try:
        connection = sql.connect(host='localhost', user='root', password=_MYSQL_PASSWORD)
        cursor = connection.cursor()
    except sql.errors.ProgrammingError:
        messagebox.showerror('Error', 'MYSQL failed to start; Invalid SQL Password')
        exit()

    cursor.execute('create database if not exists bloodbank24')
    cursor.execute('use bloodbank24')

    cursor.execute('show tables')

    if len(cursor.fetchall()) == 0:
        with open('./Assets/commands.sql') as fp:
            for statement in fp.readlines():
                if statement.startswith('create') or statement.startswith('insert'):
                    print(statement)
                    cursor.execute(statement)

    connection.commit()

    return connection, cursor
