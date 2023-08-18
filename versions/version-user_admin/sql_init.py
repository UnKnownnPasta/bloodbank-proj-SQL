import mysql.connector as sql
from tkinter import messagebox
from utils import pathLoad

def init():    
    #    important variable, change to yours
    MYSQL_PASSWORD = "root"

    try:
        con = sql.connect(
            host='localhost', user='root', password=MYSQL_PASSWORD)
        cur = con.cursor()
    except:
        messagebox.showerror('Error', 'MYSQL failed to start')
        exit()


    #    verify "bloodbank" database exists and use it
    cur.execute('create database if not exists bloodbank')
    cur.execute('use bloodbank')


    #    and also make all the tables
    cur.execute('show tables')

    # ...executed if no tables exist
    if len(cur.fetchall()) == 0:
        with open(pathLoad('resources/commands.sql')) as f:
            for l in f.readlines():
                if l.startswith('create') or l.startswith('insert'):
                    print(l)
                    cur.execute(l.strip())

    con.commit()

    return con, cur