from tkinter import messagebox, Canvas, Scrollbar, Text
from utils import create_button, create_entry, create_label, wipe_page, create_images
import pickle

#                 ------------------- Preliminary Stuff ----------------------            

# Appointments data is like:
#       Name, Info (Age, Gender), Status ('Is Donating', 'Needs Donation'), BloodGrp, Doctor (ID), Date, Hospital (ID)

IMAGES = create_images()
DOCTOR = {}
cursor, connection = None, None
root = None
types = ["DoctorID", "HospitalID", "Name", "Age", "Gender", "Email"]
INFO = None

#                 ------------------- Primary Functions ----------------------            

def load_doctor(doctor_info, src, sql, info_view, info_bar, app_view):
    global DOCTOR, cursor, connection, root, INFO
    for i in range(6):
        DOCTOR[types[i]] = doctor_info[i] if i != 4 else 'Male' if doctor_info[4] == 'M' else 'Female'
    root, INFO = src, app_view
    cursor, connection = sql

    update_info_bar(info_bar)
    update_doctor_info(info_view)
    appointments(app_view)


def update_info_bar(src):
    wipe_page(src)
    _data = []
    with open('./appointments.dat', 'rb') as f:
        try:
            while True: _data.append(pickle.load(f))
        except EOFError: pass

    _data = [i for i in _data if i['Doctor'] == DOCTOR['DoctorID']]

    from .login import show_doctor
    create_label(src, f'No. of Appointments: {len(_data)}', 40, 3, font=('Josefin Sans', 27), bg='#EDEADE')
    # Refresh & Logout
    create_button(src, '', 590, 0, image=IMAGES[0], width=60, height=74, command= lambda: update_info_bar(src))
    create_button(src, '', 522, 0, image=IMAGES[7], width=60, height=74, command= lambda: (wipe_page(root), show_doctor(cursor, connection, root)))


def update_doctor_info(src):
    wipe_page(src)
    create_label(src, '', 45, 10, image=IMAGES[10], background='#EDEADE')
    for y, data in enumerate(DOCTOR.items()):
        if y != 5:
            create_label(src, str(data[0]) + ': ', 4, y*40 + 160, font=('Lucidia Console', 16), bg='#EDEADE')
            create_label(src, str(data[1]), 110, y*40 + 153, font=('Josefin Sans', 16), bg='#EDEADE')
    create_label(src, '|' + DOCTOR['Email'], 0, 430, font=('Josefin Sans', 16), bg='#EDEADE')


#                 ------------------- Secondary Functions ----------------------            

def remove_app(app, status):
    current_apps = []
    with open('./appointments.dat', 'rb') as f:
        try:
            while True: current_apps.append(pickle.load(f))
        except EOFError: pass
    
    result = messagebox.askquestion("Confirmation", "Are you sure you want to " + ("approve this record?" if status == 'add' else "remove this record?"))
    if result == 'yes': 
        current_apps.pop(app[-1])
        with open('./appointments.dat', 'wb') as f:
            for i in current_apps:
                pickle.dump(i, f)
        wipe_page(INFO)
        appointments(INFO)
        if status == 'add':
            messagebox.showinfo('Success', f'Recorded appointment for {app[0]} to be completed.')
        else:
            messagebox.showinfo('Success', f'Removed appointment for {app[0]}.')
    else:
        messagebox.showinfo('No Action Taken', f'Appointment for {app[0]} is still valid')

def update_bloodbank(bloodtype, stat):
    if stat == 'Is Donating':
        cursor.execute(f"UPDATE BloodTable SET Units = Units + 1 WHERE concat(BloodType, RhFactor) = '{bloodtype}'")
        connection.commit()
    elif stat == 'Needs Donation':
        cursor.execute(f"UPDATE BloodTable SET Units = Units - 1 WHERE concat(BloodType, RhFactor) = '{bloodtype}'")
        connection.commit()


#                  ------------------- Tertiary Functions ----------------------            

def appointments(src):
    records_f, seperator = "|{:^14}"*5 + "|\n",  "+{:^14}"*5 + "+\n"
    seperator = seperator.format(*[*['-'*14]*5])

    app_data = "" + seperator + records_f.format('Name', 'Info', 'Status', 'Blood Group', 'Date') + seperator
    apppointments = []
    with open('./appointments.dat', 'rb') as f:
        try:
            while True:
                app = pickle.load(f)
                mod_app = list(app.values())
                mod_app = mod_app[:-1]
                mod_app.append(app['Doctor'])
                mod_app[1] = f'Male, {mod_app[1][1]}' if str(mod_app[1][0]) == 'M' else f'Female, {mod_app[1][1]}'
                mod_app.pop(4)
                apppointments.append(mod_app)
        except EOFError: 
            pass
    list_count = app_count = -1
    for row in apppointments:
        list_count += 1
        if row[-1] == DOCTOR['DoctorID']:
            app_count += 1
            app_data += records_f.format(*row)
            L = row; L.append(list_count)
            create_button(src, 'x', 620, 50 + app_count*16, padx=-20, pady=-30, font=('Cobal', 9, 'bold'), command= lambda l=L: (remove_app(l, 'remove')))
            create_button(src, '✓', 640, 50 + app_count*16, padx=-20, pady=-30, font=('Cobal', 9, 'bold'), command= lambda l=L: (remove_app(l, 'add'), update_bloodbank(l[-4], l[-5])))
    app_data += seperator

    # Create a Text widget
    text_widget = Text(src, wrap='none', width=83, height=24)
    text_widget.insert('insert', app_data)

    # Create a vertical scrollbar
    scrollbar = Scrollbar(src, command=text_widget.yview)
    scrollbar.pack(side='right', fill='y')
    text_widget.config(yscrollcommand=scrollbar.set)

    # Pack the Text widget
    text_widget['state'] = 'disabled'
    text_widget.pack()
    text_widget.lower()
    scrollbar.lower()
