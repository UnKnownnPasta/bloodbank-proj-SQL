from __main__ import app, globalImages
from tkinter import *
from helper import create_button

root, con, cur = app.root, app.connection, app.cursor


# ------------------------------------ Main User Page (from user login) -----------------------------------
class UserApp:
    def __init__(self, username, hospitalname):
        root.configure(bg='#710302')
        self.user_name = username
        self.hosp_name = hospitalname

        self.titleFrame = Frame(root, width=920, height=45, bg='#c85038')
        self.titleFrame.place(x=10, y=10)

        home_logo = Label(self.titleFrame, image=globalImages[2], bg='#c85038')
        home_logo.place(x=10, y=0)

        logout_button = Button(self.titleFrame, image=globalImages[9],
            bg='#c85038', relief=FLAT, bd=0, activebackground='#c85038', command= lambda: (
                app.authenticate(), self.titleFrame.destroy()
            )
        )
        logout_button.place(x=870, y=4)

        Name = Label(self.titleFrame, text=self.hosp_name, bg='#c85038', font=('Calibri Light', 24), fg='white')
        Name.place(x=55)

        self.mainFrame = Frame(root, bg='#7B1818', width=920, height=425)
        self.mainFrame.place(x=10, y=65)



# ------------------------------- Adding A User to Database (Admin Panel) ---------------------------------
class AdminAddUser:
    def __init__(self):
        pass