from tkinter import *
from tkinter import messagebox
import mysql.connector as sql
import os, ctypes

MYSQL_PASSWORD = 'root'
current_dir = os.path.dirname(__file__)
from helper import pinVerify, switchL_S, switchS_L, create_button, create_entry
import __main__ as m


#
# os\.path\.join\(current_dir, '(.*?)'\)
#   This module stores all the functions to start the program
#
#       - init() to initialize tkinter
#       - SignUp() for sign up window
#       - Login() for login window
#

root = Tk()
def init():
    global arrow, root, blob, topRoot, globalImg, root

    # Defined here since it wouldn't load otherwise
    bg_img_1 = PhotoImage(file=os.path.join(current_dir, 'bg/bg-blur-v2.png'))
    bg_img_2 = PhotoImage(file=os.path.join(current_dir, 'bg/bg-unblur.png'))
    #logo_img = Image.open('logo-v2-sh.png')
    logo_80 = PhotoImage(file=os.path.join(current_dir, 'src/logo-80.png')) #ImageTk.PhotoImage(logo_img.resize([int(0.13 * s) for s in logo_img.size]))
    logo_120 = PhotoImage(file=os.path.join(current_dir, 'src/logo-120.png')) #ImageTk.PhotoImage(logo_img.resize([int(0.25 * s) for s in logo_img.size]))
    arrow = PhotoImage(file=os.path.join(current_dir, 'src/arrow.png'))
    blob = PhotoImage(file=os.path.join(current_dir, 'src/box.png'))
    profImg = PhotoImage(file=os.path.join(current_dir, 'src/profile.png'))

    # Makes the images accessible globally -- as globalImg[n] n being item index
    globalImg = [bg_img_1, bg_img_2, logo_80, logo_120, profImg]

    ctypes.windll.gdi32.AddFontResourceA(os.path.join(current_dir, 'src/JosefinSans-Regular.ttf'))

    topRoot = Toplevel(root)
    topRoot.withdraw(); 
    topRoot.resizable(False, False)
    topRoot.title('Profile')
    topRoot.geometry('500x400+270+200')
    topRoot.iconphoto(False, PhotoImage(file=os.path.join(current_dir, 'src/logo-nosh.png')))

    topRoot.protocol('WM_DELETE_WINDOW', m.DEL_EVENT)

    global con, cur
    try:
        con = sql.connect(host='localhost', user='root', password=MYSQL_PASSWORD)
        cur = con.cursor()
    except:
        messagebox.showerror('Error', 'Failed to connect to SQL')
    cur.execute('show databases;')
    res = any(db[0] == 'bloodbank' for db in cur.fetchall())
    if res == False:
        cur.execute('create database bloodbank')
    cur.execute('use bloodbank')

    try:
        cur.execute('create table if not exists Hospital (HospitalID int(4) auto_increment primary key, HospitalName varchar(100) unique, Password varchar(20), Contact varchar(100), PinCode char(6) not null)')   #.zfill
        cur.execute('create table if not exists BloodBank (BloodType char(2), Units int not null, RhFactor char(8))')
        cur.execute('create table if not exists Donor (Name varchar(40), Age int(3), Gender char(20), BloodGroup char(2), HospitalID int(4), foreign key (HospitalID) references Hospital(HospitalID))')
        cur.execute('create table if not exists Recipient (Name varchar(40), Age int(3), DateOfTransfer date, HospitalID int(4), BloodType char(2), foreign key (HospitalID) references Hospital(HospitalID))')
    except:
        messagebox.showerror('Error', 'Something went wrong while initializing tables.')

    con.commit()
    root.title('Blood Bank Mng')
    root.iconphoto(False, PhotoImage(file=os.path.join(current_dir, 'src/logo-nosh.png')))
    root.resizable(False, False)
    root.geometry(f"{940}x{500}+{(root.winfo_screenwidth() - 940) // 2}+{(root.winfo_screenheight() - 500) // 2}")
    Login()
    # SignUp()


def SignUp():
    global hospName, pinCode, Contact, submBtnSu, canvasSu, swchBtnSu, PassWord
    canvasSu = Canvas(root, width='940', height='500', highlightthickness=0)
    canvasSu.create_image(0, 0, image=globalImg[0], anchor='nw')
    canvasSu.pack(side = "top", fill = "both", expand = True)

    sText = canvasSu.create_text(240, 180, text='Enter Details to Create A Account..', anchor=NW, font=('Josefin Sans', 17), fill='white')
    altText = canvasSu.create_text(320, 48, text='BLOOD BANK MANAGEMENT', anchor=NW, font=('Josefin Sans', 20, 'bold'), fill='white')
    canvasSu.create_image(230, 30, image=globalImg[3], anchor=NW)

    def setText(entry, defText):
        entry.delete(0, END) if entry.get().strip() == defText else None
        
    def restoreText(entry, defText):
        entry.insert(0, defText) if entry.get().strip() == "" else None

    hospName = create_entry(root, 240, 250, 'Hospital Name', width=70)
    hospName.bind('<FocusIn>', lambda event: setText(hospName, 'Hospital Name'))
    hospName.bind('<FocusOut>', lambda event: restoreText(hospName, 'Hospital Name'))

    pinCode = create_entry(root, 240, 310, 'Pin Code', width=22)
    pinCode.bind('<FocusIn>', lambda event: setText(pinCode, 'Pin Code'))
    pinCode.bind('<FocusOut>', lambda event: restoreText(pinCode, 'Pin Code'))

    Contact = create_entry(root, 420, 310, 'Contact (Phone No./email)', width=40)
    Contact.bind('<FocusIn>', lambda event: setText(Contact, 'Contact (Phone No./email)'))
    Contact.bind('<FocusOut>', lambda event: restoreText(Contact, 'Contact (Phone No./email)'))
    
    PassWord = create_entry(root, 240, 370, 'Enter a Strong Password', width=70)
    PassWord.bind('<FocusIn>', lambda event: setText(PassWord, 'Enter a Strong Password'))
    PassWord.bind('<FocusOut>', lambda event: restoreText(PassWord, 'Enter a Strong Password'))

    swchBtnSu = Button(root, command=switchS_L, image=arrow, relief=FLAT, bd=0, highlightthickness=0, activebackground='#ad1e1e')
    submBtnSu = create_button(root, 'Submit', 425, 430, command= lambda: m.SignSubm(pinCode.get(), Contact.get(), hospName.get(), PassWord.get()))

    swchBtnSu.place(x=770, y=30)


def Login():
    global canvasLi, userName, userPass, submBtnLi, signBtnLi
    canvasLi = Canvas(root, width='940', height='500', highlightthickness=0)
    canvasLi.create_image(0, 0, image=globalImg[1], anchor='nw')
    canvasLi.pack(side = "top", fill = "both", expand = True)

    titleLabel1 = canvasLi.create_text(355, 58, text='ADMIN', anchor='nw', font=('Franklin Gothic', 25, 'bold'), fill='white')
    titleLabel2 = canvasLi.create_text(470, 46, text='Login', anchor='nw', font=('Josefin Sans', 25), fill='white')

    sText = canvasLi.create_text(240, 180, text='Sign In', anchor='nw', font=('Franklin Gothic', 16, 'bold'), fill='white')
    altText = canvasLi.create_text(240, 200, text='Fill in details to gain access', anchor='nw', font=('Josefin Sans', 14), fill='white')

    def setText(entry, defText):
        entry.delete(0, END) if entry.get().strip() == defText else None

    def restoreText(entry, defText):
        entry.insert(0, defText) if entry.get().strip() == "" else None

    userName = create_entry(root, 240, 260, 'User Name', width=70)
    userName.bind('<FocusIn>', lambda event: setText(userName, 'User Name'))
    userName.bind('<FocusOut>', lambda event: restoreText(userName, 'User Name'))

    userPass = create_entry(root, 240, 320, 'Password', width=70)
    userPass.bind('<FocusIn>', lambda event: setText(userPass, 'Password'))
    userPass.bind('<FocusOut>', lambda event: restoreText(userPass, 'Password'))
    userPass.bind('<Return>',  lambda event: m.loginSubm(userName.get(), userPass.get()))

    submBtnLi = create_button(root, 'Login', 353, 380, command= lambda: m.loginSubm(userName.get(), userPass.get()))
    signBtnLi = create_button(root, 'Sign Up', 485, 380, command=switchL_S)
   
    orLbl = canvasLi.create_text(440, 385, text='..OR..', anchor='nw', font=('Josefin Sans', 14), fill='white')


global storage
storage = ["", 0]
scrollbar = Label(root, font=("Arial", 12), anchor=NE, bg="black", fg="white", width=104)

scrollbar.place(x=0, y=0)
def scroll_text(txt):
    global storage
    storage[0] += txt
    if len(storage[0]) > 140:
        storage[0] = '  '.join(storage[0].split('  ')[7:])
    scrollbar.configure(text=storage[0])

    def rotate(): # Text Capacity = 187 + word length
        text = scrollbar.cget("text")
        if len(text) >= 187+len(storage[0]):
            storage[0] = ""
        scrollbar.config(text=text + "  ")
        scrollbar.after(100, rotate)

    if not storage[1]:
        storage[1] = 1; rotate()