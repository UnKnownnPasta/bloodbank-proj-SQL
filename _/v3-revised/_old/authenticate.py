from tkinter import *
from tkinter import font, messagebox


#  Here these parts of the functions are handled:
#     Startup screen
#     Admin view of signup/login
#     Handling successful logins


# ------------------------ Define function for the text disappear-reappear effect -------------------------

def setText(entry, defaultText):
    entry.delete(0, END) if entry.get().strip() == defaultText else None

def restoreText(entry, defaultText):
    entry.insert(0, defaultText) if entry.get().strip() == "" else None

root, images = None, None

count = 0

# ----------------------------- Main Functions for welcome/login/signup pages -----------------------------
def WelcomeWindow(src, img, sql):
    print(img)
    global root, images, canvas
    root, images = src, img

    canvas = Canvas(src, width='940', height='500', highlightthickness=0)
    canvas.create_image(0, 0, image=img[7], anchor='nw')
    canvas.pack(side = "top", fill = "both", expand = True)


    temporary_button = Button(src, command= lambda: replace_widget(),
        bd=0, activebackground='#D22B2B', bg='#EE4B2B', relief=FLAT, image=img[8]
    )
    temporary_button.place(x=310, y=250)


    canvas.create_text(377, 85, text='Welcome!!', font=('Hello Sunday', 56), anchor=NW, fill='#303030')
    canvas.create_text(380, 85, text='Welcome!!', font=('Hello Sunday', 55), anchor=NW, fill="#D22B2B")
    canvas.create_image(290, 70, image=img[3], anchor='nw')


    switch_label = Button(src, text='Or, Login as a Admin'.upper(),
        padx=30, pady=0, relief=SOLID, activebackground='#D22B2B', bg='#D22B2B',
        command=lambda: LogOut(), borderwidth=1, highlightcolor='black', fg='white',
        font=('Calibri Light', 12), activeforeground='white', height=1
    )
    switch_label.place(x=350, y=450)


    # When you incorrectly input details to login, it writes a error on the window
    # This label is the label that shows that error text
    errorText = canvas.create_text(250, 200, text='', font=('Josefin Sans', 16), fill='', anchor=NW)



    def replace_widget():
        from helper import create_button, create_entry

        temporary_button.destroy()

        hospital_name = create_entry(src, 240, 240, 'Hospital Name', width=70)
        hospital_name.bind('<FocusIn>', lambda event: setText(hospital_name, 'Hospital Name'))
        hospital_name.bind('<FocusOut>', lambda event: restoreText(hospital_name, 'Hospital Name'))

        user_name = create_entry(src, 240, 300, 'Your Name', width=70)
        user_name.bind('<FocusIn>', lambda event: setText(user_name, 'Your Name'))
        user_name.bind('<FocusOut>', lambda event: restoreText(user_name, 'Your Name'))

        submit = create_button(src, 'Login', 405, 360, command= lambda: validate(hospital_name.get(), user_name.get()))


    def displayError():
        global count
        count += 1
        canvas.itemconfigure(errorText, fill='white', text=f'Invalid Login Details. [{count}]')


    def validate(hospname, usrname):
        # This is to make sure the user actually
        # submits a valid login and password

        for value in [hospname, usrname]:
            if len(value.strip()) == 0 or value in ['Hospital Name', 'Your Name'] or value.isdigit():
                displayError()
                return
        
        sql.execute('select HospitalName, Name from hospital, recepients where HospitalName=%s and Name=%s'%(hospname, usrname))
        print(sql.fetchone())

        canvas.destroy()
        UserWindow(hospname, usrname)
        
        
    def LogOut():
        pass
        

def UserWindow(hosp, user):
    global root, images
    root.configure(bg='#710302')

    titleFrame = Frame(root, width=920, height=45, bg='#c85038')
    titleFrame.place(x=10, y=10)

    home_logo = Label(titleFrame, image=images[2], bg='#c85038')
    home_logo.place(x=10, y=0)

    logout_button = Button(titleFrame, image=images[9],
        bg='#c85038', relief=FLAT, bd=0, activebackground='#c85038', command= lambda: (
            destroy(), titleFrame.destroy()
        )
    )
    logout_button.place(x=870, y=4)

    Name = Label(titleFrame, text=hosp, bg='#c85038', font=('Calibri Light', 24), fg='white')
    Name.place(x=55)

    mainFrame = Frame(root, bg='#7B1818', width=920, height=425)
    mainFrame.place(x=10, y=65)




    def destroy():
        titleFrame.destroy()
        mainFrame.destroy()
        WelcomeWindow(root, images)
        return None