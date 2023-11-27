from tkinter import *
from __main__ import connection, cursor
from tkinter import messagebox
from utils import create_button, create_entry
from utils import create_images
globalImages = create_images()

def setText(entry, defaultText):
    if entry.get().strip() == defaultText:
        entry.delete(0, "end")

def restoreText(entry, defaultText):
    if entry.get().strip() == "":
        entry.insert(0, defaultText)

def canvas(ctrl):
    global login_canvas
    login_canvas = Canvas(ctrl, width='940', height='500', highlightthickness=0)
    login_canvas.create_image(0, 0, image=globalImages[1], anchor='nw')
    login_canvas.pack(side = "top", fill = "both", expand = True)

def admin_login(ctrl):
    global login_canvas, root, globalImages
    root = ctrl
    canvas(root)

    standard_look = {"anchor": "nw", "fill":"white"}
    titleLabel1 = login_canvas.create_text(355, 58, text='ADMIN', font=('Franklin Gothic', 25, 'bold'), **standard_look)
    titleLabel2 = login_canvas.create_text(470, 46, text='Login', font=('Josefin Sans', 25), **standard_look)

    topText = login_canvas.create_text(240, 180, text='Sign In', font=('Franklin Gothic', 16, 'bold'), **standard_look)
    altText = login_canvas.create_text(240, 200, text='Fill in details to gain access', font=('Josefin Sans', 14), **standard_look)

    user_name = create_entry(root, 240, 260, 'User Name', width=70)
    user_name.bind('<FocusIn>', lambda event: setText(user_name, 'User Name'))
    user_name.bind('<FocusOut>', lambda event: restoreText(user_name, 'User Name'))

    user_pass = create_entry(root, 240, 320, 'Password', width=70)
    user_pass.bind('<FocusIn>', lambda event: setText(user_pass, 'Password'))
    user_pass.bind('<FocusOut>', lambda event: restoreText(user_pass, 'Password'))

    submit_button = create_button(root, 'Login', 410, 380, command= lambda: validate_cred(user_name.get(), user_pass.get()))


def validate_cred(un, up):
    global ctrl
    for i in [un, up]:
        if i == 'User Name' or i == 'Password' or i.strip() == 0:
            messagebox.showerror('Error', 'Invalid login details')
            return

    query = "select * from hospital where HospitalName=%s and Password=%s"
    values = (un, up)
    cursor.execute(query, values)
    res = cursor.fetchone()
    if res == None:
        messagebox.showerror('Error', 'Login details are not correct.')
        return

    cursor.execute('select HospitalID, PinCode from Hospital where HospitalName=%s', (un,))
    hId, pc = [i for i in cursor.fetchall()[0]]
    
    for i in list(root.__dict__['children'].values()): i.destroy()

    from views.admin_view import admin_view
    admin_view(un, up, hId, pc, root)