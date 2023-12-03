from tkinter import *
from utils import create_button, create_entry, create_images, create_label, wipe_page

IMAGES = create_images()

#               ------------------ Page Handling Functions ----------------------              

def admin_login(admin_info, control, sql):
    cursor, connection = sql

    # Ticker
    tick_text, tick_started = "", False
    ticker_bar = create_label(control, "", 0, 0, font=("Arial", 12), anchor=NE, bg="black", fg="white", width=104)

    # Header
    title_bar = Frame(control, bg="#D22B2B", height=30)
    title_bar.pack(fill=X)
    title_bar.place(rely=0.045, relwidth=1)

    # Add elements to the home bar at top (Hospital name, logo and button)
    b1 = Button(title_bar, bg="#D22B2B", relief="flat", activebackground="#D22B2B", image=IMAGES[8])
    b1.pack(side='left')
    logo_lbl = Label(title_bar, bg="#D22B2B", image=IMAGES[5]).pack(side='left', padx=5)

    # Name of hospital label
    create_label(title_bar, admin_info[1].title(), 90, -2, fg="white", bg="#D22B2B", font=('Josefin Sans', 19), pady=0)
    # Contact label
    create_label(title_bar, 'Ph: ' + admin_info[3], 650, 0, fg='white', bg='#D22B2B', font=('Josefin Sans', 19), pady=0)
    # Home Page button
    b2 = create_button(title_bar, '', 880, 2, background='#D22B2B', activebackground='#D22B2B', image=IMAGES[3])
    
    # Main Content
    display_frame = Frame(control, width=control.winfo_screenwidth(), height=440)
    display_frame.place(x=0, y=69)

    from .admin import load_admin
    load_admin((tick_text, tick_started, ticker_bar), (b1, b2), display_frame, admin_info, control, sql)


def doctor_login(doctor_info, control, sql):
    cursor, connection = sql
    control.configure(bg='#710302')

    # Header
    doc_view = Frame(control, bg="#EDEADE", width=220, height=478, highlightthickness=2, highlightbackground='#AA4A44')
    doc_view.place(x=10, y=10)

    # Appointments
    app_count = Frame(control, bg="#EDEADE", width=690, height=80, highlightthickness=2, highlightbackground='#AA4A44')
    app_count.place(x=240, y=10)
    app_view = Frame(control, bg="#EDEADE", width=690, height=388, highlightthickness=2, highlightbackground='#AA4A44')
    app_view.place(x=240, y=96)

    from .doctor import load_doctor
    load_doctor(doctor_info, control, sql, doc_view, app_count, app_view)