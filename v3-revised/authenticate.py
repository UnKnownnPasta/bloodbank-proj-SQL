from tkinter import *
from tkinter import messagebox, font

global root, images, count
root = None
images = None

count = 0

# ------------------------ Define function for the text disappear-reappear effect -------------------------

def setText(entry, defaultText):
    entry.delete(0, END) if entry.get().strip() == defaultText else None

def restoreText(entry, defaultText):
    entry.insert(0, defaultText) if entry.get().strip() == "" else None



# ----------------------------- Main Functions for welcome/login/signup pages -----------------------------
def WelcomeWindow(src, img):
    canvas = Canvas(root, width='940', height='500', highlightthickness=0)
    canvas.create_image(0, 0, image=img[7], anchor='nw')
    canvas.pack(side = "top", fill = "both", expand = True)

    temporary_button = Button(root, command= lambda: replace_widget(),
        bd=0, activebackground='#D22B2B', bg='#EE4B2B', relief=FLAT, image=img[8]
    )
    temporary_button.place(x=310, y=250)


    canvas.create_text(377, 85, text='Welcome!!', font=('Hello Sunday', 56), anchor=NW, fill='#303030')
    canvas.create_text(380, 85, text='Welcome!!', font=('Hello Sunday', 55), anchor=NW, fill="#D22B2B")
    canvas.create_image(290, 70, image=img[3], anchor='nw')


    switch_label = Button(root, text='Or, Login as a Admin'.upper(),
        padx=30, pady=0, relief=SOLID, activebackground='#D22B2B', bg='#D22B2B',
        command=lambda: LogOut(), borderwidth=2, highlightcolor='black', fg='white',
        font=('Calibri Light', 12), activeforeground='white', height=1
    )
    switch_label.place(x=350, y=450)


    # When you incorrectly input details to login, it writes a error on the window
    # This label is the label that shows that error text
    errorText = canvas.create_text(250, 200, text='', font=('Josefin Sans', 16), fill='', anchor=NW)

    def replace_widget():
        from helper import create_button, create_entry

        temporary_button.destroy()

        hospital_name = create_entry(root, 240, 240, 'Hospital Name', width=70)
        hospital_name.bind('<FocusIn>', lambda event: setText(hospital_name, 'Hospital Name'))
        hospital_name.bind('<FocusOut>', lambda event: restoreText(hospital_name, 'Hospital Name'))

        user_name = create_entry(root, 240, 300, 'Your Name', width=70)
        user_name.bind('<FocusIn>', lambda event: setText(user_name, 'Your Name'))
        user_name.bind('<FocusOut>', lambda event: restoreText(user_name, 'Your Name'))

        submit = create_button(root, 'Login', 405, 360, command= lambda: validate(hospital_name.get(), user_name.get()))


    def displayError():
        global count
        count += 1
        canvas.itemconfigure(errorText, fill='white', text=f'Invalid Login Details. [{count}]')


    def validate(hn, un):
        # This is to make sure the user actually
        # submits a valid login and password

        for i in [hn, un]:
            if len(i.strip()) == 0 or i in ['Hospital Name', 'Your Name'] or i.isdigit():
                displayError()
                return

        launchUserApp(un, hn)



    def LogOut():
        for widget in __dict__.values():
            if not isinstance(widget, int):
                widget.destroy()
        app.doLogin()