from tkinter import *
from tkinter import messagebox
from __main__ import connection, cursor
from utils import create_images, create_entry, create_button
from random import randint
images = create_images()

def destroy_frameitems(frame):
    for i in list(frame.__dict__['children'].values()):
        if isinstance(i, Label):
            if not i['text'].startswith('|'): i.destroy()
        else: i.destroy()

def donation_choice(src, ID, x):
    global images, id
    id = ID
    destroy_frameitems(src)
    lb_1 = Label(src, text='Arrange donation for a person:', font=('Cascadia Code', 19))
    lb_2 = Label(src, text='Transfer blood to another hospital:', font=('Cascadia Code', 19))
    lb_1.place(x=40, y=90)
    lb_2.place(x=40, y=240)

    opt_1 = Button(src, text='Donate', command=lambda: (destroy_frameitems(src), donate_blood_citizen(src=src, tt=x)),
            bd=0, activebackground='#D22B2B', bg='#EE4B2B', relief="flat", padx=141, pady=8, fg='white', font=('Cascadia Code', 15))
    opt_2 = Button(src, text='Transfer', command=lambda: (destroy_frameitems(src), donate_blood_hospital(src=src, tt=x)),
            bd=0, activebackground='#D22B2B', bg='#EE4B2B', relief="flat", padx=130, pady=8, fg='white', font=('Cascadia Code', 15))
    opt_1.place(x=110, y=150)
    opt_2.place(x=110, y=300)

# ------- Option: 1
def donate_blood_citizen(src, tt):
    tt['text'] = '|    Arranging Appointment'

    def make_lbl_entry(ctrl, txt, x1, y1, x2, y2, w) -> Entry:
        nm = create_entry(src, x1, y1, '', width=w)
        lbl = Label(src, text=txt, font=('Josefin Sans', 18))
        lbl.place(x=x2, y=y2)
        return nm
    
    e_1 = make_lbl_entry(src, 'Enter name of person:', 270, 100, 40, 100, 60)
    e_2 = make_lbl_entry(src, 'Gender:', 130, 165, 40, 165, 9)
    e_3 = make_lbl_entry(src, 'Age:', 310, 165, 245, 165, 9)
    e_4 = make_lbl_entry(src, 'Blood Group Required:', 270, 240, 40, 240, 9)

    create_button(src, 'Appoint', 60, 340, command=lambda: validate())

    def validate():
        def val(strings: list[str]):
            allowed_characters = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 +-")
            return all(char in allowed_characters for char in strings)

        if False in {val(e_1.get()), val(e_2.get()), val(e_3.get()), val(e_4.get())}:
            messagebox.showerror('Error', 'All fields are not properly filled out.')
        else:
            try: cursor.execute(f"insert into recipient values ({randint(1000, 9999)}, '{e_1.get()}', '{e_3.get()}', '{e_2.get()}', '{e_4.get()}', 0, 0)")
            except: messagebox.showerror('Error', 'Failed to appoint user; Verify user details'); connection.rollback()
            connection.commit()
            destroy_frameitems(src); donation_choice(src=src, ID=id, x=tt)


# ------- Option: 2
def donate_blood_hospital(src, tt):
    tt['text'] = '|    Transferring Blood'
    
    lx = Label(src, text='Select the following;', font=('Josefin Sans', 18))
    lx.place(x=40, y=100)


    lbl_1 = Label(src, text='Choose a hospital:', font=('Josefin Sans', 18))
    lbl_1.place(x=40, y=170)
    hosp_options, hosp_sval = [], StringVar(value='None')

    cursor.execute('select HospitalName, HospitalID from Hospital;')
    data = cursor.fetchall()
    if data != None:
        for row in data:
            hosp_options.append(row[0].title()) if row[1] != id else None
    else:
        hosp_options.append('')
    hosp_menu = OptionMenu(src, hosp_sval, *hosp_options)
    hosp_menu.place(x=230, y=180)


    lbl_2 = Label(src, text='Select Blood Type(s):', font=('Josefin Sans', 18))
    lbl_2.place(x=40, y=230)
    global totalList, selected, display_label

    totalList = """"""
    display_label = Label(src, text=totalList, font=('Josefin Sans', 14), bg='#FBFCF8', padx=100, width=10, height=10, anchor='n')
    display_label.place(x=550, y=90)

    selected = []
    def option_selected(vv):
        global totalList, selected
        totalList += f"Requested: {vv}\n"
        selected.append(vv)
        display_label.config(text=totalList)  # Update the display_label text

    def reset_selected(): 
        global selected, display_label, totalList
        display_label.config(text="")  # Update the display_label text
        selected.clear(); totalList = """"""

    blood_options = ['A+', 'A-', 'B+', 'B-', 'O+', 'O-', 'AB+', 'AB-']
    blood_sval = StringVar(value='        ')
    blood_menu = OptionMenu(src, blood_sval, *blood_options)
    blood_menu.place(x=260, y=240)

    # Clear the menu items first
    blood_menu['menu'].delete(0, 'end')

    for option in blood_options:
        blood_menu['menu'].add_command(label=option, command=lambda v=option: option_selected(v))

    proceed = Button(src, text='Proceed with donation', command=lambda: finish(src),
        bd=0, activebackground='#D22B2B', bg='#EE4B2B', relief="flat", font=('Cascadia Code', 15))
    proceed.place(x=40, y=353)

    reset = Button(src, text='Reset Selections', command=lambda: reset_selected(),
        bd=0, activebackground='#D22B2B', bg='#EE4B2B', relief="flat", font=('Cascadia Code', 15))
    reset.place(x=340, y=353)

    def finish(ctrl):
        global selected, id
        status = 0

        if hosp_sval.get() == '' or blood_sval.get() == '': messagebox.showerror('Error', 'Need to fill out all required fields')

        for i in selected:
            cursor.execute('select Units from bloodtable where concat(BloodType, RhFactor) = "%s"'%(i,))
            if cursor.fetchone()[0] == 0: status = 1
            q = f'update bloodtable set Units = Units - 1 where concat(BloodType, RhFactor) = "{i}"'
            cursor.execute(q)
        else: pass

        if status == 1:
            messagebox.showerror('Error', 'Not enough storage of blood available')
            connection.rollback()
            return
        else: connection.commit()

        cursor.execute('select HospitalName, HospitalID from hospital where HospitalID = %s'%(id))
        data = cursor.fetchone()
        messagebox.showinfo('Success', f'Updated unit of bloods stored in your bank, {data[0]} to {blood_sval.get()}')
        destroy_frameitems(ctrl)
        donate_blood_hospital(ctrl, tt=tt)