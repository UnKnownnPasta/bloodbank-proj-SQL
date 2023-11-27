from tkinter import messagebox, font, ttk
from tkinter import *
import mysql.connector as sql

global con, cur
con = sql.connect(host='localhost', user='root', password='root')
cur = con.cursor()
cur.execute('use bloodbank')

global root, bg_img, logo_img
root = Tk()
bg_img_1 = PhotoImage(file='bg-blur-v2.png')
bg_img_2 = PhotoImage(file='bg-unblur.png')
logo_img = PhotoImage(file='l2-2.png')
root.title('Blood Bank Mng')
root.iconphoto(False, PhotoImage(file='logo.png'))
root.geometry(f"{940}x{500}+{(root.winfo_screenwidth() - 940) // 2}+{(root.winfo_screenheight() - 500) // 2}")
root.resizable(False, False)

def SignUp():
    global hospName, pinCode, Contact, submBtnSu, canvasSu, swchBtnSu
    canvasSu = Canvas(root, width='940', height='500', highlightthickness=0)
    canvasSu.create_image(0, 0, image=bg_img_1, anchor='nw')
    canvasSu.pack(side = "top", fill = "both", expand = True)

    sText = canvasSu.create_text(240, 180, text='Enter Details to Create A Account..', anchor='nw', font=('Josefin Sans', 17), fill='white')
    altText = canvasSu.create_text(320, 48, text='BLOOD BANK MANAGEMENT', anchor='nw', font=('Josefin Sans', 20, 'bold'), fill='white')
    canvasSu.create_image(230, 30, image=logo_img, anchor=NW)

    def on_focus_1(event): hospName.delete(0, 'end') if hospName.get().strip() == "Hospital Name"  else None
    def on_focus_2(event): pinCode.delete(0, 'end') if pinCode.get().strip() == "Pin Code" else None
    def on_focus_3(event): Contact.delete(0, 'end') if Contact.get().strip() == "Contact (Phone No./email)" else None
    def off_focus_1(event): hospName.insert(0, 'Hospital Name') if hospName.get().strip() == "" else None
    def off_focus_2(event): pinCode.insert(0, 'Pin Code') if pinCode.get().strip() == "" else None
    def off_focus_3(event): Contact.insert(0, 'Contact (Phone No./email)') if Contact.get().strip() == "" else None
    hospName = Entry(root, bd=16, relief=FLAT, width=70)
    hospName.insert(0, 'Hospital Name')
    hospName.bind('<FocusIn>', on_focus_1)
    hospName.bind('<FocusOut>', off_focus_1)

    pinCode = Entry(root, bd=16, relief=FLAT, width=70)
    pinCode.insert(0, 'Pin Code')
    pinCode.bind('<FocusIn>', on_focus_2)
    pinCode.bind('<FocusOut>', off_focus_2)

    Contact = Entry(root, bd=16, relief=FLAT, width=70)
    Contact.insert(0, 'Contact (Phone No./email)')
    Contact.bind('<FocusIn>', on_focus_3)
    Contact.bind('<FocusOut>', off_focus_3)

    swchBtnSu = Button(root, text='Log in', command=switchS_L)
    submBtnSu = Button(root, text='Submit', background='#6CB4EE', relief=FLAT, padx=20, pady=10, activebackground='#6CB4EE', command=SignSubm)

    hospName.place(x=240, y=250)
    pinCode.place(x=240, y=310)
    Contact.place(x=240, y=370)
    submBtnSu.place(x=240, y=430)
    swchBtnSu.place(x=870, y=30)

def Login():
    global canvasLi, userName, userPass, submBtnLi, swchBtnLi
    canvasLi = Canvas(root, width='940', height='500', highlightthickness=0)
    canvasLi.create_image(0, 0, image=bg_img_2, anchor='nw')
    canvasLi.pack(side = "top", fill = "both", expand = True)

    titleLabel1 = canvasLi.create_text(355, 58, text='ADMIN', anchor='nw', font=('Franklin Gothic', 25, 'bold'), fill='white')
    titleLabel2 = canvasLi.create_text(470, 46, text='Login', anchor='nw', font=('Josefin Sans', 25), fill='white')

    sText = canvasLi.create_text(240, 180, text='Sign In', anchor='nw', font=('Franklin Gothic', 16, 'bold'), fill='white')
    altText = canvasLi.create_text(240, 200, text='Fill in details to gain access', anchor='nw', font=('Josefin Sans', 14), fill='white')

    def on_focus_1(event): userName.delete(0, 'end') if userName.get().strip() == "User Name"  else None
    def on_focus_2(event): userPass.delete(0, 'end') if userPass.get().strip() == "Password" else None
    def off_focus_1(event): userName.insert(0, 'User Name') if userName.get().strip() == "" else None
    def off_focus_2(event): userPass.insert(0, 'Password') if userPass.get().strip() == "" else None
    userName = Entry(root, bd=16, relief=FLAT, width=70)
    userName.insert(0, 'User Name')
    userName.bind('<FocusIn>', on_focus_1)
    userName.bind('<FocusOut>', off_focus_1)

    userPass = Entry(root, bd=16, relief=FLAT, width=70)
    userPass.insert(0, 'Password')
    userPass.bind('<FocusIn>', on_focus_2)
    userPass.bind('<FocusOut>', off_focus_2)

    submBtnLi = Button(root, text='Submit', background='#6CB4EE', relief=FLAT, padx=20, pady=10, activebackground='#6CB4EE', )#command= lambda: program(userName.get(), userPass.get()))
    swchBtnLi = Button(root, text='Sign Up', command=switchL_S)

    userName.place(x=240, y=260)
    userPass.place(x=240, y=320)
    submBtnLi.place(x=240, y=380)
    swchBtnLi.place(x=870, y=30)

def switchS_L():
    w = [hospName, pinCode, Contact, submBtnSu, canvasSu, swchBtnSu]
    for i in w:
        i.destroy()
    Login()

def SignSubm():
    print(pinCode.get(), Contact.get(), hospName.get())

def switchL_S():
    w = [canvasLi, userName, userPass, submBtnLi, swchBtnLi]
    for i in w:
        i.destroy()
    SignUp()

def program(un, pw, pc):
    w_super = [hospName, pinCode, Contact, submBtnSu, canvasSu, swchBtnSu, canvasLi, userName, userPass, submBtnLi, swchBtnLi]
    for i in w_super:
        i.destroy()
    

SignUp()
root.mainloop()