
from tkinter import Tk, messagebox, PhotoImage
import mysql.connector as sql
import threading

# Not a module, but the utils folder
from utils import pathLoad

# Main Entry File
#     Stores the tkinter instance (root)
root = Tk()

#     and intialises its basic features
root.title('Blood Bank System')
root.iconphoto(False, PhotoImage( file=pathLoad('resources/icons/logo-120.png') ))
root.resizable(False, False)

#     also, sets the position of window on the screen
x_coordinate = str((root.winfo_screenwidth() - 940) // 2)
y_coordinate = str((root.winfo_screenheight() - 500) // 2)
root.geometry(f"940x500+" + x_coordinate + "+" + y_coordinate)

#    then initialise SQL
from sql_init import init
connection, cursor = init()


#    finally, start the program
if __name__ == "__main__":
    from views.admin_login import admin_login
    admin_login(root)

    root.mainloop()
