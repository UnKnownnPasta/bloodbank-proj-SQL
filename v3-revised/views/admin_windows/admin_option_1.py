from tkinter import *
from tkinter import messagebox
from __main__ import connection, cursor
from utils import create_images
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


# ------- Option: 2
def donate_blood_hospital(src, tt):
    tt['text'] = '|    Transferring Blood'
    
    lbl_1 = Label(src, text='Choose a hospital:', font=('Josefin Sans', 18))
    lbl_1.place(x=40, y=90)
    hosp_options, hosp_sval = [], StringVar(value='None')

    cursor.execute('select HospitalName, HospitalID from Hospital;')
    data = cursor.fetchall()
    if data != None:
        for row in data:
            hosp_options.append(row[0].title()) if row[1] != id else None
    else:
        hosp_options.append('')
    hosp_menu = OptionMenu(src, hosp_sval, *hosp_options)
    hosp_menu.place(x=230, y=100)


    lbl_2 = Label(src, text='Select Blood Type(s):', font=('Josefin Sans', 18))
    lbl_2.place(x=40, y=150)
    global totalList, selected

    totalList = """"""
    display_label = Label(src, text=totalList, font=('Josefin Sans', 14), bg='#FBFCF8', padx=100, width=10, height=10, anchor='n')
    display_label.place(x=550, y=90)

    selected = []
    def option_selected(vv):
        global totalList, selected
        totalList += f"Requested: {vv}\n"
        selected.append(vv)
        display_label.config(text=totalList)  # Update the display_label text

    def reset_selected(): display_label.config(text="")  # Update the display_label text

    blood_options = ['A+', 'A-', 'B+', 'B-', 'O+', 'O-', 'AB+', 'AB-']
    blood_sval = StringVar(value='        ')
    blood_menu = OptionMenu(src, blood_sval, *blood_options)
    blood_menu.place(x=260, y=160)

    # Clear the menu items first
    blood_menu['menu'].delete(0, 'end')

    for option in blood_options:
        blood_menu['menu'].add_command(label=option, command=lambda v=option: option_selected(v))

    proceed = Button(src, text='Proceed with donation (Update record)', command=lambda: finish(src),
        bd=0, activebackground='#D22B2B', bg='#EE4B2B', relief="flat", font=('Cascadia Code', 15))
    proceed.place(x=40, y=300)

    def finish(ctrl):
        global selected, id
        status = 0

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