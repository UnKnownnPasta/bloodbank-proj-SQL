import os
from tkinter import *
from tkinter import messagebox

import mysql.connector as sql

# -------------------------------------------- Some functions ---------------------------------------------

#   SQL Password
#   Change this to your MySQL Password
MYSQL_PASSWORD = 'root'

def pathLoad(path):
    return os.path.join(os.path.dirname(__file__), path)



# ----------------------------------- Main Parts that run the program -------------------------------------

global root_low, connection, cursor, login_var, signup_var, adduser_var
root_low = None          # Holds our tkinter instance
connection = None        # Connection to SQL database
cursor = None            # Cursor of SQL conenction

login_var = None         # Stores login page widgets
signup_var = None        # Stores signup page widgets

# adduser_var = None     # Stores Add user page widgets

globalImages = {}        # Dictionary storing bunch of images


# --------- Starting point of program ---------

def main():
    global root_low
    root_low = Tk()
    root_low.title('Blood Bank System')
    root_low.title('Blood Bank Mng')
    root_low.iconphoto(False, PhotoImage(file=pathLoad('src/logo-120.png')))
    root_low.resizable(False, False)

    window_xCoord = (root_low.winfo_screenwidth() - 940) // 2
    window_yCoord = (root_low.winfo_screenheight() - 500) // 2
    root_low.geometry(f"{940}x{500}+{window_xCoord}+{window_yCoord}")

    initializeDatabase()
    initializeImages()


# -------- Create Database connection --------

def initializeDatabase():
    global connection, cursor
    try:
        connection = sql.connect(host='localhost', user='root', password=MYSQL_PASSWORD)
        cursor = connection.cursor()
        cursor.execute('create database if not exists bloodbank')
        cursor.execute('use bloodbank')
    except:
        messagebox.showerror('Info', 'Failed to connect to SQL.')

    cursor.execute('show tables')
    if len(cursor.fetchall()) == 0:

        with open('commands.sql') as f:
            for line in f.readlines():
                if f not in ['', '\n'] and f[0] != '-':
                    cursor.execute(line)



# -------- Function to store images --------

# def initializeImages():
#     global globalImages
#     # Creating a bunch of images so that it loads instantly later on
    
#     arrow = PhotoImage(file=pathLoad('src/arrow.png'))
#     arrow_unblur = PhotoImage(file=pathLoad('src/arrow_2.png'))
#     blob = PhotoImage(file=pathLoad('src/box.png'))
    
#     bg_image_1 = PhotoImage(file=pathLoad('bg/bg-blur-v2.png'))
#     bg_image_2 = PhotoImage(file=pathLoad('bg/bg-unblur.png'))
#     logo_80 = PhotoImage(file=pathLoad('src/logo-80.png'))
#     logo_120 = PhotoImage(file=pathLoad('src/logo-120.png'))
#     profileImage = PhotoImage(file=pathLoad('src/profile.png'))
#     bg_image_3 = PhotoImage(file=pathLoad('bg/bg-auth.png'))        
#     btn = PhotoImage(file=pathLoad('bg/button.png'))
#     logout = PhotoImage(file=pathLoad('src/lg.png'))

#     # Makes the images accessible globally -- used as globalImages[n], n being item index
#     globalImages = {
#         0: bg_image_1,    1: bg_image_2,
#         2: logo_80,       3: logo_120,
#         4: profileImage,  5: [arrow, arrow_unblur],
#         6: blob,          7: bg_image_3,
#         8: btn,           9: logout,
#     }


def initializeImages():
    image_paths = [
        'bg/bg-blur-v2.png',   'bg/bg-unblur.png',
        'src/logo-80.png',     'src/logo-120.png',
        'src/profile.png',     'src/arrow.png',    # 'src/arrow_2.png',
        'src/box.png',         'bg/bg-auth.png',
        'bg/button.png',       'src/lg.png'
    ]
    
    for index, path in enumerate(image_paths):
        globalImages[index] = PhotoImage(pathLoad(path))
    
    return globalImages
    # print(globalImages)

# --------- --------- --------- ---------
if __name__ == "__main__":
    # Start the program
    main()

    # Then create required welcome screen widgets
    from authenticate import WelcomeWindow
    # print(globalImages)
    WelcomeWindow(root_low, globalImages, cursor)

    root_low.mainloop()