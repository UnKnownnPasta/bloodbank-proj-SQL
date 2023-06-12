from tkinter import messagebox, font, ttk
from tkinter import *
import mysql.connector as sql
# import subprocess, sys, imp

global con, cur
con = sql.connect(host='localhost', user='root', password='root')
cur = con.cursor()

root = Tk()

def main():
    global root, bg_img
    bg_img = PhotoImage(file='bg.png')
    root.title('Blood bank mng')
    root.iconphoto(False, PhotoImage(file='logo.png'))
    root.geometry('1080x500')
    root.resizable(False, False)

    canvas = Canvas(root, width='1080', height='500', highlightthickness=0)
    canvas.create_image(0, 0, image=bg_img, anchor='nw')
    canvas.pack(side = "top", fill = "both", expand = True)

    titleLabel1 = canvas.create_text(415, 34, text='ADMIN', anchor='nw', font=('Franklin Gothic', 25, 'bold'), fill='white')
    titleLabel2 = canvas.create_text(533, 22, text='Login', anchor='nw', font=('Josefin Sans', 25), fill='white')

    sText = canvas.create_text(300, 170, text='Sign In', anchor='nw', font=('Franklin Gothic', 16, 'bold'), fill='white')
    altText = canvas.create_text(300, 190, text='Fill in details to gain access', anchor='nw', font=('Josefin Sans', 14), fill='white')

    def on_focus_1(event): userName.delete(0, 'end') if event else None
    def on_focus_2(event): userPass.delete(0, 'end') if event else None
    userName = Entry(root, bd=16, relief=FLAT, width=70)
    userName.insert(END, 'User Name')
    userName.bind('<FocusIn>', on_focus_1)

    userPass = Entry(root, bd=16, relief=FLAT, width=70)
    userPass.insert(END, 'Password')
    userPass.bind('<FocusIn>', on_focus_2)

    submBtn = Button(root, text='Submit', background='#6CB4EE', relief=FLAT, bd=10, padx=10)

    userName.place(x=300, y=250)
    userPass.place(x=300, y=310)
    submBtn.place(x=300, y=370)

main()
root.mainloop()