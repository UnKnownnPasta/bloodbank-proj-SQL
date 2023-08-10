from tkinter import *
from __main__ import connection, cursor

def donate_blood(src):
    chlbl = Label(src, text='Choose a hospital:', font=('Josefin Sans', 18))
    chlbl.place(x=40, y=90)


    op_hospital, sval_hospital = [], StringVar(value='- - - - - - - - - - -')

    cursor.execute('select HospitalName from Hospital;')
    data = cursor.fetchall()
    if data != None:
        for row in data:
            op_hospital.append(row)
    else:
        op_hospital.append('')

    dd_hospital = OptionMenu(src, sval_hospital, *op_hospital)
    dd_hospital.place(x=240, y=100)


    bldlbl = Label(src, text='Select Blood Type(s):', font=('Josefin Sans', 18))
    bldlbl.place(x=40, y=90)

    totalList = """----------------
"""
    bldlist = Label(src, text=totalList, font=('Josefin Sans', 15))
    bldlbl.place(x=400, y=100)

    def option_selected(vv):
        totalList += f"Requested: {vv}"
    def reset_selected():
        totalList = totalList[:17]
        

    op_blood = ['A+', 'A-', 'B+', 'B-', 'O+', 'O-', 'AB+', 'AB-']
    sval_blood = StringVar(value='- - - - - - -')
    dd_blood = OptionMenu(src, sval_blood, *op_blood)
    dd_blood.place(x=240, y=100)

    for option in op_blood:
        dd_blood['menu'].add_command(label=op_blood, command=lambda v=option: option_selected(v))