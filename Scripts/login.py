from tkinter import messagebox, Canvas
from utils import create_button, create_entry, create_label, create_images, wipe_page

IMAGES = create_images()

#               ------------------- Preliminary Functions ----------------------              

def create_canvas(src):
    canv = Canvas(src, width=940, height=500, highlightthickness=0)
    canv.pack()
    return canv

def setText(entry, defaultText):
    if entry.get().strip() == defaultText:
        entry.delete(0, "end")

def restoreText(entry, defaultText):
    if entry.get().strip() == "":
        entry.insert(0, defaultText)

def bind_focus_events(widget, text):
    widget.bind('<FocusIn>', lambda event: setText(widget, text))
    widget.bind('<FocusOut>', lambda event: restoreText(widget, text))

#               ------------------ Page Handling Functions ----------------------              

def show_choice(cur, con, src):
    canvas = create_canvas(src=src)
    canvas.create_image(0, 0, image=IMAGES[2], anchor='nw')

    canvas.create_text(410, 220, text='Login As:', font=('Josefin Sans', 20), anchor='nw', fill='#FFFFFF')
    create_button(src, 'Doctor', 310, 290, command= lambda: (wipe_page(src), show_doctor(cur, con, src)))
    create_button(src, 'Admin', 490, 290, command= lambda: (wipe_page(src), show_admin(cur, con, src)))

def show_doctor(cur, con, src):
    canvas = create_canvas(src=src)
    canvas.create_image(0, 0, image=IMAGES[2], anchor='nw')

    canvas.create_text(300, 40, text='DOCTOR LOGIN', font=('Josefin Sans', 34), anchor='nw', fill='#FFFFFF')
    canvas.create_image(230, 175, image=IMAGES[9], anchor='nw')
    canvas.create_text(280, 170, text='Enter Login Details:', font=('Josefin Sans', 20), anchor='nw', fill='#FFFFFF')

    text = canvas.create_text(250, 257, text='Dr.', anchor='nw', fill='#000000')
    rect = canvas.create_rectangle(230, 240, 280, 289, fill='#FFFFFF', outline="")
    canvas.lower(rect, text)
    doctor_name = create_entry(src, 280, 240, 'Registered Name', width=66)
    bind_focus_events(doctor_name, 'Registered Name')

    doctor_id = create_entry(src, 230, 300, 'Your ID', width=33)
    bind_focus_events(doctor_id, 'Your ID')
    hospital_id = create_entry(src, 478, 300, 'Hospital ID', width=33)
    bind_focus_events(hospital_id, 'Hospital ID')

    create_button(src, 'Submit', 400, 370, command= lambda: validate_credentials_doc(src, doctor_name.get().strip(), doctor_id.get(), hospital_id.get(), cur, con))


def show_admin(cur, con, src):
    canvas = create_canvas(src=src)
    canvas.create_image(0, 0, image=IMAGES[2], anchor='nw')

    canvas.create_text(355, 58, text='ADMIN', font=('Franklin Gothic', 25, 'bold'), anchor='nw', fill='#FFFFFF')
    canvas.create_text(470, 46, text='Login', font=('Josefin Sans', 25), anchor='nw', fill='#FFFFFF')
    canvas.create_image(230, 175, image=IMAGES[9], anchor='nw')
    canvas.create_text(280, 170, text='Enter Login Details:', font=('Josefin Sans', 20), anchor='nw', fill='#FFFFFF')

    admin_hospital = create_entry(src, 240, 240, 'Registered Hospital Name', width=70)
    bind_focus_events(admin_hospital, 'Registered Hospital Name')

    admin_password = create_entry(src, 240, 300, 'Password', width=70)
    bind_focus_events(admin_password, 'Password')

    create_button(src, 'Submit', 400, 370, command= lambda: validate_credentials_admin(src, admin_hospital.get().strip(), admin_password.get().strip(), cur, con))

#              ------------------- Authentication Functions -----------------------             

def validate_credentials_doc(src, d_name, d_id, h_id, cursor, pointer):
    if (d_name.lower() == 'registered name' or
         not d_id.isdigit() or not h_id.isdigit() or
          len(d_id) != 4 or len(h_id) != 4):
        messagebox.showerror('Error', 'Invalid login details')
        return

    cursor.execute(f"SELECT * FROM Doctors WHERE Name='{d_name}' AND HospitalID={h_id} AND ID={d_id}")
    doctor_info = cursor.fetchone()

    if doctor_info is None:
        messagebox.showerror('Error', 'Login details are not correct.')
        return

    wipe_page(src)

    from .views import doctor_login
    doctor_login(doctor_info, src, (cursor, pointer))


def validate_credentials_admin(src, user, password, cursor, pointer):
    if (user.lower() == 'registered hospital name' or password.lower() == 'password' or
            len(user) == 0 or len(password) == 0 or
            user.isdigit() or password.isdigit()):
        messagebox.showerror('Error', 'Invalid login details')
        return

    cursor.execute(f"SELECT * FROM hospital WHERE HospitalName='{user}' AND Password='{password}'")
    admin_info = cursor.fetchone()

    if admin_info is None:
        messagebox.showerror('Error', 'Login details are not correct.')
        return

    wipe_page(src)

    from .views import admin_login
    admin_login(admin_info, src, (cursor, pointer))
