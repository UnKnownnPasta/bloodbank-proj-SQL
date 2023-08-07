
from tkinter import Tk, messagebox, PhotoImage
import mysql.connector as sql

# Not a module, but the utils folder
from utils import pathLoad


#    important variable, change to yours
MYSQL_PASSWORD = "root"


# Main Entry File
#     Stores the tkinter instance (root)
root = Tk()

#     and intialises its basic features
root.title('Blood Bank Manager')
root.iconphoto(False, PhotoImage( file=pathLoad('resources/icons/logo-120.png') ))
root.resizable(False, False)

#     also, sets the position of window on the screen
x_coordinate = str((root.winfo_screenwidth() - 940) // 2)
y_coordinate = str((root.winfo_screenheight() - 500) // 2)
root.geometry(f"940x500+" + x_coordinate + "+" + y_coordinate)


#    then initialise SQL
try:
    connection = sql.connect(
        host='localhost', user='root', password=MYSQL_PASSWORD)
    cursor = connection.cursor()
except:
    messagebox.showerror('Error', 'MYSQL failed to start')
    exit()


#    verify "bloodbank" database exists and use it
cursor.execute('create database if not exists bloodbank')
cursor.execute('use bloodbank')


#    and also make all the tables
cursor.execute('show tables')

  # ...executed if no tables exist
if len(cursor.fetchall()) == 0:
    with open('resources/commands.sql') as f:
        for f in commands.readlines():
            if f.split()[0] == 'create':
                cursor.execute(line)


#    finally, start the program
if __name__ == "__main__":
    from views.welcome import welcome_screen
    welcome_screen(root)

    root.mainloop()