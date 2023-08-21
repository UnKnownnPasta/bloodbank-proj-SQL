from tkinter import *
from __main__ import connection, cursor
from tkinter import messagebox
from utils import create_button, create_entry, create_images, wipe_page

# --------------------------- Handle login function for admin page ----------------------------

globalImages = create_images()

#               ------------------- Preliminary Functions ----------------------              
def setText(entry, defaultText):
    if entry.get().strip() == defaultText:
        entry.delete(0, "end")

def restoreText(entry, defaultText):
    if entry.get().strip() == "":
        entry.insert(0, defaultText)

def custom_entry(control, x, y, text):
    entry = create_entry(control, x, y, text, width=70)
    entry.bind('<FocusIn>', lambda event: setText(entry, text))
    entry.bind('<FocusOut>', lambda event: restoreText(entry, text))
    return entry

#               ------------------ Page Handling Functions ----------------------              
def make_canvas(control):
    canvas = Canvas(control, width='940', height='500', highlightthickness=0)
    # Add Background
    canvas.create_image(0, 0, image=globalImages[1], anchor='nw')
    canvas.pack(side="top", fill="both", expand=True)
    return canvas

def validate_cred(control, admin_user: str, admin_pass: str):
    for i in [admin_user, admin_pass]:
        if i == 'User Name' or i == 'Password' or len(i.strip()) == 0 or i.isdigit():
            messagebox.showerror('Error', 'Invalid login details'); return

    cursor.execute(f"select * from hospital where HospitalName='{admin_user}' and Password='{admin_pass}'")
    info = cursor.fetchone()
    if info == None:
        messagebox.showerror('Error', 'Login details are not correct.'); return

    hospital_ID, pincode = info[0], info[4]
    wipe_page(control)

    from views.admin_page import admin_login
    admin_login(admin_user, admin_pass, hospital_ID, pincode, control)

#               ----------------------- Login Page Code ----------------------              
def admin_login(root):
    login_canvas = make_canvas(root)

    # Text on the page
    label_look = {"anchor": "nw", "fill":"white"}
    login_canvas.create_text(355, 58, text='ADMIN', font=('Franklin Gothic', 25, 'bold'), **label_look)
    login_canvas.create_text(470, 46, text='Login', font=('Josefin Sans', 25), **label_look)

    login_canvas.create_text(240, 180, text='Sign In', font=('Franklin Gothic', 16, 'bold'), **label_look)
    login_canvas.create_text(240, 200, text='Fill in details to gain access', font=('Josefin Sans', 14), **label_look)

    # Input 1
    user_name = custom_entry(root, 240, 260, 'User Name')
    # Input 2
    user_pass = custom_entry(root, 240, 320, 'Password')
    # Login Button
    create_button(root, 'Login', 410, 380, command= lambda: validate_cred(root, user_name.get(), user_pass.get()))
