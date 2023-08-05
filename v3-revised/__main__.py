from tkinter import *
from tkinter import messagebox
import mysql.connector as sql
import os



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

globalImages = None      # Dictionary storing bunch of images


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
    except:
        messagebox.showerror('Info', 'Failed to connect to SQL. Login will fail')
    else:
        cursor.execute('show databases;')

        # any() return True if there is atleast 1 database named bloodbank
        res = any(db[0] == 'bloodbank' for db in cursor.fetchall())
        if res == False:
            cursor.execute('create database bloodbank')

        cursor.execute('use bloodbank')

    try:

        # "commands.sql" has a bunch of sql commands to create required tables
        # that includes bloodrecords, donor, recipient, donor, hospital

        with open(pathLoad('commands.sql'), 'r') as sql_file:
            sql_command = sql_file.readlines()
            for command in sql_command:
                cursor.execute(command)
    except:
        messagebox.showerror('Error', 'Failed to initialize tables.')
    finally:
        connection.commit()





# -------- Function to store images --------

def initializeImages():
    global globalImages
    # Defining a bunch of images to preload so that it loads instantly
    
    arrow = PhotoImage(file=pathLoad('src/arrow.png'))
    arrow_unblur = PhotoImage(file=pathLoad('src/arrow_2.png'))
    blob = PhotoImage(file=pathLoad('src/box.png'))
    
    bg_image_1 = PhotoImage(file=pathLoad('bg/bg-blur-v2.png'))
    bg_image_2 = PhotoImage(file=pathLoad('bg/bg-unblur.png'))
    logo_80 = PhotoImage(file=pathLoad('src/logo-80.png'))
    logo_120 = PhotoImage(file=pathLoad('src/logo-120.png'))
    profileImage = PhotoImage(file=pathLoad('src/profile.png'))
    bg_image_3 = PhotoImage(file=pathLoad('bg/bg-auth.png'))        
    btn = PhotoImage(file=pathLoad('bg/button.png'))
    logout = PhotoImage(file=pathLoad('src/lg.png'))

    # Makes the images accessible globally -- used as globalImages[n], n being item index
    globalImages = {
        0: bg_image_1,    1: bg_image_2,
        2: logo_80,       3: logo_120,
        4: profileImage,  5: [arrow, arrow_unblur],
        6: blob,          7: bg_image_3,
        8: btn,           9: logout,
    }




# ----------- Admin Functions -----------

# def doLogin():
#     from authenticate import AdminLogin
#     login = AdminLogin() # Show login Page

#     # Initialize a variable with all login page widgets for future usage
#     self.login_var = list(login.__dict__.values())

# def doSignup():
#     from authenticate import AdminSignUp
#     signup = AdminSignUp()

#     # Initialize a variable with all signup page widgets for future usage
#     self.signup_var = list(signup.__dict__.values())




# ----------- User functions -----------

# def launchUserApp(x, y):
#     from userpages import UserApp
#     UserApp(x, y)

# def launchAdminApp(x, y, z, w):
#     for i in self.login_var:
#         i.destroy()

#     from adminpages import AdminApp
#     AdminApp(x, y, z, w)




# --------- --------- --------- ---------
if __name__ == "__main__":
    # Start the program
    main()

    # Then create required welcome screen widgets
    from authenticate import WelcomeWindow
    WelcomeWindow(root_low, globalImages)

    root_low.mainloop()