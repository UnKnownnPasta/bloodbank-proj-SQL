from tkinter import messagebox, Frame, OptionMenu, StringVar
from utils import create_button, create_entry, create_label, create_images, wipe_page, create_entry_label
from datetime import datetime
import pickle

IMAGES = create_images()
cursor, connection = None, None
ADMIN = None
DATE_NOW = datetime.now().strftime("%d/%m/%Y")

#                 ------------------- Primary Functions ----------------------            

def load_admin(ticker, titile_icons, display_frame, admin, src, sql):
    global cursor, connection
    cursor, connection = sql
    global ticker_txt, tick_start, ticker_bar
    ticker_txt, tick_start, ticker_bar = ticker
    global sidebar_opened, current_view, contentframe, ADMIN
    sidebar_opened, contentframe = False, display_frame
    ADMIN = admin
    current_view = create_label(src, '|    Hospital Management System', 0, 85, font=('Cascadia Code', 22), width=55, bg='#FBFCF8', height=1, anchor='w')

    titile_icons[0].configure(command= lambda: toggle_sidebar(src))
    # titile_icons[1].configure(command= lambda: _tick('  profile  '))
    titile_icons[1].configure(command= lambda: home_page(contentframe))
    home_page(contentframe)

    _tick("   Logged in as " + admin[1] + "!   ")


def _tick(txt):
    global ticker_txt, tick_start, ticker_bar

    ticker_txt += txt
    ticker_bar.config(text=ticker_txt)

    def rotate():
        global ticker_txt
        if len(ticker_txt) > 270: ticker_txt = ticker_txt.split('  ', 7)[-1]

        ticker_txt += "   "
        ticker_bar.config(text=ticker_txt)
        ticker_bar.after(100, rotate)

    if not tick_start:
        tick_start = True
        rotate()

#                 ------------------- Secondary Functions ----------------------            

def toggle_sidebar(root):
    global home_bar, sidebar_opened
    if sidebar_opened:
        home_bar.destroy()
        sidebar_opened = False
        return 'close'
    else:
        sidebar_opened = True
        create_sidebar(root)

def create_sidebar(root):
    global home_bar, contentframe
    home_bar = Frame(root, bg="#D22B2B")
    home_bar.pack(fill='y')
    home_bar.place(relx=0, rely=0.138, relheight=1, relwidth=0.25)

    option_looks = {
        "font": ("Corbel", 15), "padx": 10, "relief": "flat", "fg": "white", "underline": -1,
        "activeforeground": "white", "background": "#D22B2B", "activebackground": "#D22B2B"
    }

    create_button(home_bar, 'Arrange Appointment', 6, 30, **option_looks, command=lambda: (arrange_appointment(contentframe), toggle_sidebar(root)))
    create_button(home_bar, 'View all Doctors', 6, 100, **option_looks, command=lambda: (view_doctors(contentframe), toggle_sidebar(root)))
    create_button(home_bar, 'View Appointments', 6, 170, **option_looks, command=lambda: (view_appointments(contentframe), toggle_sidebar(root)))
    create_button(home_bar, 'Manage Blood Storage', 6, 240, **option_looks, command=lambda: (manage_blood_storage(contentframe), toggle_sidebar(root)))
    create_button(home_bar, 'EXIT', 4, 380, **option_looks, command=lambda: exit_app(root))

#                   ------------------- Option Functions ----------------------            

def home_page(src):
    wipe_page(src)
    current_view['text'] = '|    Hospital Management System'

    create_label(src, 'Statistics  ' + '-'*88, 9, 80, font=('Cobal', 20))
    data_txt_1 = create_label(src, '', 10, 120, width=30, height=3, bg='#FFFFFF', fg='black', font=('Josefin Sans', 20), padx=-20, pady=0)
    data_1, count, fp = "No. of Appointments Active\n".upper(), 0, open('./appointments.dat', 'rb')
    try:
        while True:
            app = pickle.load(fp)
            if app['Hospital'] == ADMIN[0]: count += 1
    except EOFError: pass
    data_txt_1['text'] = data_1 + str(count)

    data_txt_2 = create_label(src, '', 490, 120, width=29, height=3, bg='#FFFFFF', fg='black', font=('Josefin Sans', 20), padx=-20, pady=0)
    cursor.execute('SELECT sum(Units) FROM BloodTable')
    data_2, result = "Units of Blood Stored\n".upper(), cursor.fetchone()[0]
    data_txt_2['text'] = data_2 + str(result)


def arrange_appointment(src):
    _tick('    Arranging a new appointment    ')
    current_view['text'] = '|    Fill Details of Person'
    wipe_page(src)

    e_1 = create_entry_label(src, 'Enter name of person:', 270, 100, 40, 100, 40)
    e_2 = create_entry_label(src, 'Gender:', 130, 165, 40, 165, 9)
    e_3 = create_entry_label(src, 'Age:', 310, 165, 245, 165, 9)

    create_label(src, 'Select a Doctor:', 430, 165, font=('Josefin Sans', 18))
    cursor.execute('SELECT Name, ID from Doctors where HospitalID = %s'%(ADMIN[0]))
    text_var, options = StringVar(src), cursor.fetchall()
    e_4 = OptionMenu(src, text_var, *[i[0] for i in options])
    e_4['relief'] = 'flat'; e_4['bg'] = '#FFFFFF'; e_4['width'] = 15; e_4['activebackground'] = '#FFFFFF'; e_4['height'] = 2
    e_4.place(x=585, y=170)

    e_5 = create_entry_label(src, 'Blood Group:', 180, 240, 40, 240, 9)
    e_6 = create_entry_label(src, 'Date:', 370, 240, 300, 240, 15)
    
    create_label(src, 'Status:', 530, 240, font=('Josefin Sans', 18))
    type_var, choices = StringVar(src), ['Needs Donation', 'Is Donating']
    e_7 = OptionMenu(src, type_var, *choices)
    e_7['relief'] = 'flat'; e_7['bg'] = '#FFFFFF'; e_7['width'] = 15; e_7['activebackground'] = '#FFFFFF'; e_7['height'] = 2
    e_7.place(x=610, y=240)

    create_button(src, 'Appoint', 60, 340, command=lambda: validate())

    def validate():
        nonlocal options
        name, age, doctor, date = e_1.get().strip(), e_3.get().strip(), text_var.get().strip(), e_6.get().strip()
        gender = e_2.get().strip().upper()
        blood_group, status = e_5.get().strip().upper(), type_var.get().strip()
        valid_blood_groups = ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']

        if not name or not name.replace(' ', '').isalpha(): messagebox.showerror('Error', 'Please enter a valid name.'); return
        if gender not in ['M', 'F']: messagebox.showerror('Error', 'Please enter a valid gender (M/F).'); return
        if not age.isdigit() or not 17 < int(age) < 66: messagebox.showerror('Error', 'Please enter a valid age.'); return
        if not doctor: messagebox.showerror('Error', 'Please select a doctor.'); return
        if not status: messagebox.showerror('Error', 'Please choose a status.'); return
        if blood_group not in valid_blood_groups: messagebox.showerror('Error', 'Please enter a valid blood group.'); return
        try: date_given = datetime.strptime(date, '%d/%m/%Y')
        except ValueError: messagebox.showerror('Error', 'Please enter a valid date.'); return
        cursor.execute(f"select sum(Units) from BloodTable where concat(BloodType, RhFactor) = '{blood_group}'")
        if cursor.fetchone()[0] == 0.0: messagebox.showerror('Error', f'Not enough units of {blood_group} in stock.'); return

        with open('./appointments.dat', 'ab') as f:
            pickle.dump({"Name": name, "Info": (gender, age), "Status": status, "BloodGrp": blood_group, "Doctor": dict(options).get(doctor), "Date": date, "Hospital": ADMIN[0]}, f)
        messagebox.showinfo('Success', f'Recorded a Appointment for {name.title()} with Dr. {doctor} on {date}.')


def view_doctors(src):
    _tick('    Listing registered doctors    ')
    current_view['text'] = '|    Viewing Doctors'
    
    records_f, seperator = "|{:^11}" + "|{:^15}"*2 + "|{:^5}|{:^10}|{:^25}|{:^15}|\n",  "+{:^11}" +  "+{:^15}"*2 + "+{:^5}+{:^10}+{:^25}+{:^15}+\n"
    seperator = seperator.format(*['-----------', '---------------', '---------------', '-----', '----------', '-'*25, '-'*15])

    wipe_page(src)
    doc_data = "" # String of data
    cursor.execute('select * from Doctors where HospitalID=%s'%ADMIN[0])
    doc_data += seperator + records_f.format('ID', 'HospitalID', 'Name', 'Age', 'Gender', 'Email', 'Appointments') + seperator
    apppointments, docs = {}, cursor.fetchall()
    # Create Key: Value pair for;  DoctorID: Appointment count
    for row in docs:  apppointments[row[0]] = 0
    with open('./appointments.dat', 'rb') as f:
        try:
            while True:
                app = pickle.load(f)
                if app['Hospital'] == ADMIN[0]: apppointments[app['Doctor']] += 1 
        except EOFError: pass
    for row in docs:  doc_data += records_f.format(*row, apppointments[row[0]])
    doc_data += seperator

    create_label(src, doc_data, 1, 70, bg='#f0f0f0', width=110, height=12, font=('Lucida Console', 11), bd=0, anchor='nw')


def view_appointments(src):
    _tick('    Listing current appointments    ')
    current_view['text'] = '|    Viewing Appointments'
    
    wipe_page(src)
    records_f, seperator = "|{:^14}"*6 + "|{:<11}" + "|\n",  "+{:^14}"*6 + "+{:^11}" + "+\n"
    seperator = seperator.format(*[*['-'*14]*6, '-'*11])

    app_data = "" # String of data
    app_data += seperator + records_f.format('Name', 'Info', 'Status', 'Blood Group', 'Doctor ID', 'Date', 'Hospital ID') + seperator
    apppointments = []
    with open('./appointments.dat', 'rb') as f:
        try:
            while True:
                app = pickle.load(f)
                if app['Hospital'] == ADMIN[0]:
                    ml = list(app.values()); ml[1] = f'Male, {ml[1][1]}' if str(ml[1][0]) == 'M' else f'Female, {ml[1][1]}'
                    apppointments.append(ml)
        except EOFError: pass
    for row in apppointments: app_data += records_f.format(*row)
    app_data += seperator

    create_label(src, app_data, 6, 70, bg='#f0f0f0', width=110, height=100, font=('Lucida Console', 11), bd=0, anchor='nw')


def manage_blood_storage(src):
    _tick('    Now Managing Blood Storage    ')
    current_view['text'] = '|    Viewing Blood Storage'
    records_f, seperator = "|{:^15}|{:^15}|\n", "+{:^15}+{:^15}+\n".format('-'*15, '-'*15)

    def load_blood_data():
        wipe_page(src)
        cursor.execute('select concat(BloodType, RhFactor), Units from BloodTable')
        blood_data = "" + seperator + records_f.format('BloodType', 'Units') + seperator
        for row in cursor.fetchall(): blood_data += records_f.format(*row)
        blood_data += seperator

        create_label(src, blood_data, 30, 120, bg='#f0f0f0', width=33, height=12, font=('Lucida Console', 15), bd=0, anchor='nw')
        global update_btn
        update_btn = create_button(src, 'Update Blood Data', 500, 310, command=lambda: update_blood_data())

    load_blood_data()

    def update(blood, qty):
        if (blood.isdigit() or blood.upper() not in ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']):
            messagebox.showerror('Error', 'Invalid Blood Type,'); return
        if (not (len(qty) <= 2 and qty.isdigit()))  and  (not (len(qty) <= 3 and (qty[0] == '+' or qty[0] == '-') and qty[1:].isdigit() )) :
            messagebox.showerror('Error', 'Invalid Blood Quantity,'); return
        cursor.execute(f'SELECT SUM(Units + {str(qty)}) FROM BloodTable WHERE CONCAT(BloodType, RhFactor) = "{blood.upper()}"')
        if cursor.fetchone()[0] < 0.0: messagebox.showerror('Error', "Can't deduct that much blood."); return

        cursor.execute('UPDATE BloodTable SET Units = Units + %s WHERE concat(BloodType, RhFactor) = "%s"' % (qty, blood))
        connection.commit()
        load_blood_data()

    def update_blood_data():
        global update_btn
        update_btn.destroy()
        e1 = create_entry_label(src, 'Enter Blood Type:', 730, 125, 500, 130, 12)
        e2 = create_entry_label(src, 'Enter Blood Quantity:', 730, 175, 500, 180, 12)
        create_button(src, 'Update', 500, 300, command=lambda: update(e1.get(), e2.get()))


def exit_app(src):
    wipe_page(src)
    from .login import show_admin
    show_admin(cursor, connection, src)