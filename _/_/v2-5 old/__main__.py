from tkinter import *
from tkinter import messagebox
import mysql.connector as sql
import os

# -------------------------------------- Some Ease-Of-Use functions --------------------------------------

#   SQL Password
#       Change this to your MySQL Password (host system)
MYSQL_PASSWORD = 'root'
current_dir = os.path.dirname(__file__)

def pathLoad(path):
    return os.path.join(current_dir, path)

# ----------------------------------- Main Class that runs the program ------------------------------------

class BloodBankApp:

    # __init__ starts the function - it's like calling a function with the stuff defined below, but automatic
    # self allows the variables defined with it, to be called ANYWHERE
    def __init__(self):
        self.root = Tk()
        self.root.title('Blood Bank System')
        self.root.title('Blood Bank Mng')
        self.root.iconphoto(False, PhotoImage(file=pathLoad('src/logo-120.png')))
        self.root.resizable(False, False)
        self.loading_label = Label(self.root, text='Loading...')

        window_xCoord = (self.root.winfo_screenwidth() - 940) // 2
        window_yCoord = (self.root.winfo_screenheight() - 500) // 2
        self.root.geometry(f"{940}x{500}+{window_xCoord}+{window_yCoord}")

        self.connection = None
        self.cursor = None

        self.login_var = None     # Stores login page widgets
        self.signup_var = None    # Stores signup page widgets
        self.adduser_var = None   # Stores Add user page widgets

        self.initializeDatabase()
        self.initializeImages()

    def initializeDatabase(self):
        try:
            self.connection = sql.connect(host='localhost', user='root', password=MYSQL_PASSWORD)
            self.cursor = self.connection.cursor()
        except:
            messagebox.showerror('Info', 'Failed to connect to SQL. Login will fail')
        else: # Runs if there is no error
            self.cursor.execute('show databases;')

            # any() return True if there is atleast 1 result that is returned by .fetchall()
            res = any(db[0] == 'bloodbank' for db in self.cursor.fetchall())
            if res == False:
                self.cursor.execute('create database bloodbank')
            self.cursor.execute('use bloodbank')

        try:
            with open(pathLoad('commands.sql'), 'r') as sql_file:
                sql_command = sql_file.readlines()
                for command in sql_command:
                    self.cursor.execute(command)
        except:
            messagebox.showerror('Error', 'Failed to initialize tables.')
        finally:
            self.connection.commit()

    def initializeImages(self):
        global globalImages
        # Defining a bunch of images to preload so that it loads instantly
        
        arrow = PhotoImage(file=pathLoad('src/arrow.png'))
        arrow_unblur = PhotoImage(file=pathLoad('src/arrow_2.png'))
        blob = PhotoImage(file=pathLoad('src/box.png'))
        
        bg_image_1 = PhotoImage(file=pathLoad('bg/bg-blur-v2.png'))
        bg_image_2 = PhotoImage(file=pathLoad('bg/bg-unblur.png'))    # If PIL was there, we can save file space by resizing images instead of loading new ones
        logo_80 = PhotoImage(file=pathLoad('src/logo-80.png'))        # ImageTk.PhotoImage(logo_img.resize([int(0.13 * s) for s in logo_img.size]))
        logo_120 = PhotoImage(file=pathLoad('src/logo-120.png'))      # ImageTk.PhotoImage(logo_img.resize([int(0.25 * s) for s in logo_img.size]))
        profileImage = PhotoImage(file=pathLoad('src/profile.png'))
        bg_image_3 = PhotoImage(file=pathLoad('bg/bg-auth.png'))        
        btn = PhotoImage(file=pathLoad('bg/button.png'))
        logout = PhotoImage(file=pathLoad('src/lg.png'))

        # Makes the images accessible globally -- called as globalImg[n], n being item index
        globalImages = {
            0: bg_image_1,    1: bg_image_2,
            2: logo_80,       3: logo_120,
            4: profileImage,  5: [arrow, arrow_unblur],
            6: blob,          7: bg_image_3,
            8: btn,           9: logout,
        }
    
    def authenticate(self):
        self.loading_label.destroy()
        from authenticate import SelectAuthType
        SelectAuthType()

    def doLogin(self):
        from authenticate import AdminLogin
        login = AdminLogin() # Show login Page

        # Initialize a variable with all login page widgets for future usage
        self.login_var = list(login.__dict__.values())

    def doSignup(self):
        from authenticate import AdminSignUp
        signup = AdminSignUp()

        # Initialize a variable with all login page widgets for future usage
        self.signup_var = list(signup.__dict__.values())

    def launchUserApp(self, x, y):
        from userpages import UserApp
        UserApp(x, y)
    
    def launchAdminApp(self, x, y, z, w):
        for i in self.login_var:
            i.destroy()

        from adminpages import AdminApp
        AdminApp(x, y, z, w)

if __name__ == "__main__":
    app = BloodBankApp()

    # Run login page
    app.authenticate()
    app.root.mainloop()