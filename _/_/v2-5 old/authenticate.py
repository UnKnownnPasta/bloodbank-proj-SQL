from __main__ import app, globalImages
from tkinter import *
from tkinter import messagebox
from helper import *

root, con, cur = app.root, app.connection, app.cursor


# ------------------------ Define function for the text disappear-reappear effect -------------------------

def setText(entry, defaultText):
    entry.delete(0, END) if entry.get().strip() == defaultText else None

def restoreText(entry, defaultText):
    entry.insert(0, defaultText) if entry.get().strip() == "" else None


# ------------------------------ Main Classes for welcome/login/signup pages ------------------------------

class SelectAuthType:
    def __init__(self):
        self.auth_canvas = Canvas(root, width='940', height='500', highlightthickness=0)
        self.auth_canvas.create_image(0, 0, image=globalImages[7], anchor='nw')
        self.auth_canvas.pack(side = "top", fill = "both", expand = True)

        self.count = 0

        standard_look = {"anchor": "nw", "fill":"#D22B2B"}

        self.auth_canvas.create_text(377, 85, text='Welcome!!', font=('Hello Sunday', 56), anchor=NW, fill='#303030')
        self.auth_canvas.create_text(380, 85, text='Welcome!!', font=('Hello Sunday', 55), **standard_look)
        self.auth_canvas.create_image(290, 70, image=globalImages[3], anchor='nw')

        self.tempStartupButton = Button(root, command= lambda: remove(self),
            bd=0, activebackground='#D22B2B', bg='#EE4B2B', relief=FLAT, image=globalImages[8]
        )
        self.tempStartupButton.place(x=310, y=250)

        self.switch_label = Button(root, text='Or, Login as a Admin'.upper(),
            padx=30, pady=0, relief=SOLID, activebackground='#D22B2B', bg='#D22B2B',
            command=lambda: self.LogOut(), borderwidth=2, highlightcolor='black', fg='white',
            font=('Calibri Light', 12), activeforeground='white', height=1
        )
        self.switch_label.place(x=350, y=450)

        def remove(self):
            self.tempStartupButton.destroy()
            self.mainPage()

    
    def mainPage(self):
        # Placeholder text for errors
        self.errorText = self.auth_canvas.create_text(250, 200, text='', font=('Josefin Sans', 16), fill='', anchor=NW)

        self.hospital_name = create_entry(root, 240, 240, 'Hospital Name', width=70)
        self.hospital_name.bind('<FocusIn>', lambda event: setText(self.hospital_name, 'Hospital Name'))
        self.hospital_name.bind('<FocusOut>', lambda event: restoreText(self.hospital_name, 'Hospital Name'))

        self.user_name = create_entry(root, 240, 300, 'Your Name', width=70)
        self.user_name.bind('<FocusIn>', lambda event: setText(self.user_name, 'Your Name'))
        self.user_name.bind('<FocusOut>', lambda event: restoreText(self.user_name, 'Your Name'))

        self.submit = create_button(root, 'Login', 405, 360, command= lambda: self.validate(self.hospital_name.get(), self.user_name.get()))

    def displayError(self):
        self.count += 1
        self.auth_canvas.itemconfigure(self.errorText, fill='white')
        self.auth_canvas.itemconfigure(self.errorText, text=f'Invalid Login Details. Check it again. [{self.count}]')

    def validate(self, hn, un):
        for i in [hn, un]:
            if len(i.strip()) == 0 or i in ['Hospital Name', 'Your Name']:
                self.displayError()
                return
            elif i.isdigit():
                self.displayError()
                return
        
        for widget in self.__dict__.values():

            # isinstance(thing, type) checks if the "thing" is of the same data type as "type"
            if not isinstance(widget, int):
                widget.destroy()

        app.launchUserApp(un, hn)

    def LogOut(self, x=None):
        for widget in self.__dict__.values():
            if not isinstance(widget, int):
                widget.destroy()
        app.doLogin()



# -------------------------------------- Admin Login and Signup Pages -------------------------------------

class AdminLogin:
    def __init__(self):
        self.login_canvas = Canvas(root, width='940', height='500', highlightthickness=0)
        self.login_canvas.create_image(0, 0, image=globalImages[1], anchor='nw')
        self.login_canvas.pack(side = "top", fill = "both", expand = True)
        self.mainPage()

    def mainPage(self):
        standard_look = {"anchor": "nw", "fill":"white"}
        titleLabel1 = self.login_canvas.create_text(355, 58, text='ADMIN', font=('Franklin Gothic', 25, 'bold'), **standard_look)
        titleLabel2 = self.login_canvas.create_text(470, 46, text='Login', font=('Josefin Sans', 25), **standard_look)

        topText = self.login_canvas.create_text(240, 180, text='Sign In', font=('Franklin Gothic', 16, 'bold'), **standard_look)
        altText = self.login_canvas.create_text(240, 200, text='Fill in details to gain access', font=('Josefin Sans', 14), **standard_look)

        self.user_name = create_entry(root, 240, 260, 'User Name', width=70)
        self.user_name.bind('<FocusIn>', lambda event: setText(self.user_name, 'User Name'))
        self.user_name.bind('<FocusOut>', lambda event: restoreText(self.user_name, 'User Name'))

        self.user_pass = create_entry(root, 240, 320, 'Password', width=70)
        self.user_pass.bind('<FocusIn>', lambda event: setText(self.user_pass, 'Password'))
        self.user_pass.bind('<FocusOut>', lambda event: restoreText(self.user_pass, 'Password'))
        self.user_pass.bind('<Return>',  lambda event: AdminAccess(self.user_name.get(), self.user_pass.get()))

        self.switchBtn = Button(root, command= lambda: (self.destroy(), app.authenticate()), image=globalImages[5][1],
            relief=FLAT, bd=0, highlightthickness=0, activebackground='#ad1e1e'
        )
        self.switchBtn.place(x=770, y=30)

        self.submit_button = create_button(root, 'Login', 300, 380, command= lambda: AdminAccess(self.user_name.get(), self.user_pass.get()))
        self.signin_button = create_button(root, 'Make a account', 428, 380, command=switchL_S)

    def destroy(self):
        for i in list(self.__dict__.values()): i.destroy()

class AdminSignUp:
    def __init__(self):
        self.signup_canvas  = Canvas(root, width='940', height='500', highlightthickness=0)
        self.signup_canvas.create_image(0, 0, image=globalImages[0], anchor='nw')
        self.signup_canvas.pack(side = "top", fill = "both", expand = True)
        self.mainPage()

    def mainPage(self):
        titleText = self.signup_canvas.create_text(240, 180, text='Enter Details to Create A Account..', anchor=NW, font=('Josefin Sans', 17), fill='white')
        altText = self.signup_canvas.create_text(320, 48, text='BLOOD BANK MANAGEMENT', anchor=NW, font=('Josefin Sans', 20, 'bold'), fill='white')
        self.signup_canvas.create_image(230, 30, image=globalImages[3], anchor=NW)

        self.hospName = create_entry(root, 240, 250, 'Hospital Name', width=70)
        self.hospName.bind('<FocusIn>', lambda event: setText(self.hospName, 'Hospital Name'))
        self.hospName.bind('<FocusOut>', lambda event: restoreText(self.hospName, 'Hospital Name'))

        self.pinCode = create_entry(root, 240, 310, 'Pin Code', width=22)
        self.pinCode.bind('<FocusIn>', lambda event: setText(self.pinCode, 'Pin Code'))
        self.pinCode.bind('<FocusOut>', lambda event: restoreText(self.pinCode, 'Pin Code'))

        self.Contact = create_entry(root, 420, 310, 'Contact (Phone No./email)', width=40)
        self.Contact.bind('<FocusIn>', lambda event: setText(self.Contact, 'Contact (Phone No./email)'))
        self.Contact.bind('<FocusOut>', lambda event: restoreText(self.Contact, 'Contact (Phone No./email)'))
        
        self.PassWord = create_entry(root, 240, 370, 'Enter a Strong Password', width=70)
        self.PassWord.bind('<FocusIn>', lambda event: setText(self.PassWord, 'Enter a Strong Password'))
        self.PassWord.bind('<FocusOut>', lambda event: restoreText(self.PassWord, 'Enter a Strong Password'))

        self.switchBtn = Button(root, command=switchS_L, image=globalImages[5][0], relief=FLAT, bd=0, highlightthickness=0, activebackground='#ad1e1e')
        self.submitBtn = create_button(root, 'Submit', 390, 430, command= lambda: AdminSubmit(self.pinCode.get(), self.Contact.get(), self.hospName.get(), self.PassWord.get()))

        self.switchBtn.place(x=770, y=30)
