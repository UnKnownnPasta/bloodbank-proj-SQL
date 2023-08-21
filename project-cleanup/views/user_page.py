# To store hospital and user names
HOPSITAL = ""
USER = ""

# --------------------------------- User page handling -------------------------------------

from tkinter import *
from tkinter import font, ttk, messagebox
from utils import create_button, create_entry, wipe_page, create_label
from __main__ import cursor, connection
from datetime import datetime

images = {}

#             ------------------- Preliminary Functions ----------------------              
def home_bar(source):
    global titleFrame, HOPSITAL
    titleFrame = Frame(source, width=920, height=45, bg='#c85038')
    titleFrame.place(x=10, y=10)

    # App icon
    create_label(titleFrame, "", 10, 0, image=images[5], bg='#c85038')

    # Log out button
    create_button(titleFrame, "", 870, 4, image=images[8], background='#c85038', relief="flat",
        bd=0, activebackground='#c85038', command= lambda: destroy(source))


def display_info(frame, text1, text2, x1, y1, x2, y2, ):
    small_text = create_label(frame, text1, x1, y1, bg='#7B1818', font=('Bahnscrift', 12), fg='white')

    underlined_font = font.Font(family='Josefin Sans', size=25, underline=True)
    create_label(frame, text2, x2, y2, font=underlined_font, fg='white', bg='#7B1818')
    small_text.lift()

def create_dropdown(options: list, x, y):
    string_data = StringVar()
    combobox = ttk.Combobox(hospitalFrame, textvariable=string_data, values=options, state="readonly")
    combobox.place(x=x, y=y)
    return string_data

def update_bloodbank(type, quantity):
    cursor.execute(f'update bloodtable set Units = Units+{int(quantity)} where concat(BloodType, RhFactor)="{type}"')
    connection.commit()


#           ------------------- Left Side of Page: Displaying ----------------------              
def left_display_info(control):
    global data
    user_info_frame = Frame(control, bg='#7B1818', width=435, height=425)
    user_info_frame.place(x=10, y=65)

    cursor.execute(f"select * from recipient where Name='{USER}'")
    data = cursor.fetchone()

    create_label(user_info_frame, 'Your Information ', 10, 15, bg='#841d1d', fg='white', padx=3, width=27, height=1, font=('Josefin Sans', 20))

    # Add a profile icon then display name of user
    create_label(user_info_frame, "", 20, 100, image=images[7], bg='#7B1818')
    create_label(user_info_frame, USER.title(), 60, 83, bg='#7B1818', width=10, height=1,
        fg='white', anchor="center", font=font.Font(family='Josefin Sans', size=25, underline=True))

    # Now show all the information of user on window
    # display_info() creates labels ... see the function
    display_info(user_info_frame, 'AGE', data[2], 23, 160, 23, 170)
    display_info(user_info_frame, 'SEX', data[3].title(), 150, 160, 150, 170)
    display_info(user_info_frame, 'BLOOD TYPE', data[4], 280, 160, 280, 170)


#          ------------------- Right Side of Page: Displaying ----------------------              
# Function to display options to user
def show_options():
    global b1, b2, hospitalFrame

    for i in list(hospitalFrame.__dict__['children'].values()):
        if i['text'] != 'Request services': i.destroy()

    b1 = create_button(hospitalFrame, 'Donate Blood (Transfusion)', 55, 100, padx=80, command= lambda: option_1_request())
    b2 = create_button(hospitalFrame, 'Request Blood', 55, 200, padx=124, command= lambda: option_2_appoint())

def right_display_options(control):
    global hospitalFrame
    hospitalFrame = Frame(control, bg='#7B1818', width=475, height=425)
    hospitalFrame.place(x=455, y=65)

    create_label(hospitalFrame, 'Request services', 10, 15, bg='#841d1d', fg='white', width=30, height=1, font=('Josefin Sans', 20))

    # Make options visible
    show_options()

#          ------------------- Right Side of Page: Functions ----------------------              
def option_1_request():
    global b1, b2, hospitalFrame, data, root
    b1.destroy(); b2.destroy()

    # User Input: 1
    create_label(hospitalFrame, "Enter Quantity of Blood:", 20, 80, bg='#7B1818', font=('Josefin Sans', 17), fg='white')
    blood_qty_entry = create_entry(hospitalFrame, 280, 80, "", width=10)

    # User Input: 2
    create_label(hospitalFrame, "Hospital:", 20, 130, bg='#7B1818', font=('Josefin Sans', 17), fg='white')
    cursor.execute(f'SELECT HospitalName FROM hospital')
    name_list = cursor.fetchall()
    hospitals = []
    for name in name_list:
        hospitals.append(name[0])
    selected_hospital = create_dropdown(hospitals, 120, 145)

    # User Input: 3
    create_label(hospitalFrame, "Date of Appointment: (DD/MM/YYYY)", 20, 180, bg='#7B1818', font=('Josefin Sans', 17), fg='white')
    date_entry = create_entry(hospitalFrame, 20, 230, "")

    # Buttons
    create_button(hospitalFrame, "Request", 100, 310, command=lambda:validate_info())
    create_button(hospitalFrame, "Back", 260, 310, command=lambda: show_options())

    def validate_info():
        date_text = date_entry.get().replace(' ', '')

        if not blood_qty_entry.get().isdigit() or blood_qty_entry.get().isspace():
            messagebox.showerror('Error', "Didn't specify blood quantity.")

        elif selected_hospital.get() == '':
            messagebox.showerror('Error', 'Select a hospital for a appointment.')

        elif len(date_text) != 0 or date_text.replace('/', '').isdigit():
            try:
                datee = datetime.strptime(date_text, "%d/%m/%Y")
                update_bloodbank(data[4], blood_qty_entry.get())
                messagebox.showinfo('Success', f"Requested a appointment in {selected_hospital.get()}! It'll be around {datee.date()}")
                show_options()
            except ValueError:
                messagebox.showerror('Error', 'Invalid Date format.'); return
        else:
            messagebox.showerror('Error', 'Invalid Date format.'); return


def option_2_appoint():
    global b1, b2, hospitalFrame, data, root
    b1.destroy(); b2.destroy()

    create_label(hospitalFrame, "Hospital:", 20, 65, bg='#7B1818', font=('Josefin Sans', 17), fg='white')

    # User Input: 1
    cursor.execute('SELECT HospitalName FROM hospital;')
    name_list = cursor.fetchall()
    hospitals = []
    for name in name_list:
        hospitals.append(name[0])
    selected_hospital = create_dropdown(hospitals, 120, 80)

    # User Input: 2
    create_label(hospitalFrame, "Info on any current/past illness:", 20, 100, bg='#7B1818', font=('Josefin Sans', 17), fg='white')
    illness_entry = create_entry(hospitalFrame, 20, 150, "", width=67)

    # User Input: 3
    create_label(hospitalFrame, "Date of Appointment: (DD/MM/YYYY)", 20, 210, bg='#7B1818', font=('Josefin Sans', 17), fg='white')
    date_entry = create_entry(hospitalFrame, 20, 260, "")

    # Buttons
    create_button(hospitalFrame, "Donate", 100, 350, command=lambda: validate_info())
    create_button(hospitalFrame, "Back", 260, 350, command=lambda: show_options())

    def validate_info():
        date_text = date_entry.get().strip().replace(' ', '')

        if selected_hospital.get() == '':
            messagebox.showerror('Error', 'No Hospital Selected')
        
        elif illness_entry.get().isdigit() or illness_entry.get().isspace() or illness_entry.get() == '':
            messagebox.showerror('Error', 'Please mention any past illness or medical condition(s)')
        
        elif len(date_text) != 0 or date_text.replace('/', '').isdigit():
            try:
                datee = datetime.strptime(date_text, "%d/%m/%Y")
                messagebox.showinfo('Success', f"Successfully set a appointment in {selected_hospital.get()}, on {date_text}!")
                show_options()
            except ValueError:
                messagebox.showerror('Error', 'Invalid Date format.'); return
        else:
            messagebox.showerror('Error', 'Invalid Date format.'); return



# ---------------------------- Loading all pages and windows -------------------------------
def user_window(hosp, usr, source, img):
    global HOPSITAL, USER, root
    HOPSITAL, USER = hosp, usr

    root = source
    root.configure(bg='#710302')
    images.update(img)

    # Create home bar
    home_bar(source)

    # Then make left side of window
    left_display_info(source)

    # Then make the right side
    right_display_options(source)

def destroy(src):
    wipe_page(src)

    from views.welcome_page import welcome_screen
    welcome_screen(src)