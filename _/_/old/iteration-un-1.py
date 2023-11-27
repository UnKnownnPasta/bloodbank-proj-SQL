from tkinter import messagebox, font
from tkinter import *
import mysql.connector as sql
# import subprocess, sys, imp

global con, cur
con = sql.connect(host='localhost', user='root', password='root')
cur = con.cursor()

root = Tk()

# try:
#     imp.find_module('pyglet')
# except:
#     subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# from pyglet import font, text
# font.add_file('it-s/it-new/JosefinSans-Thin.ttf')

def main():
    global root, bg_img
    bg_img = PhotoImage('it-s/it-new/bg.png')
    root.title('Blood bank mng')
    root.iconphoto(False, PhotoImage(file='it-s/it-new/logo.png'))
    root.geometry('1080x500')
    root.resizable(False, False)

    canvas = Canvas(root, width='1080', height='500', highlightthickness=0)
    canvas.create_image(0, 0, image=bg_img, anchor='nw')
    canvas.pack(side = "top", fill = "both", expand = True)

    titleLabel1 = canvas.create_text(410, 32, text='ADMIN', anchor='nw', font=('Lato Regular', 28, 'bold'), fill='white')
    titleLabel2 = canvas.create_text(540, 32, text='Login', anchor='nw', font=('Josefin Sans Thin', 28), fill='white')

    sText = canvas.create_text(300, 170, text='Sign In', anchor='nw', font=('Century Gothic', 15, 'bold'), fill='white')
    altText = canvas.create_text(300, 200, text='Fill in details to gain access', anchor='nw', font=('Century Gothic', 13, 'italic'), fill='white')

    userEntry = Entry(root, relief='flat')
    userEntry.pack(padx='400', pady='60')
    userEntry.place(x=390, y=250)

main()
root.mainloop()