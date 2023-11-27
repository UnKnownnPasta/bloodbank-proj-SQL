from tkinter import messagebox
from tkinter import *
import mysql.connector as sql

global con, cur
con = sql.connect(host='localhost', user='root', password='root')
cur = con.cursor()

root = Tk()
root.config(highlightthickness=0, highlightbackground='black')

def main():
    # Login window details
    global root, background_image
    root.title('Blood bank mng')
    root.iconphoto(False, PhotoImage(file='plus.png'))
    root.geometry('1080x500')
    root.resizable(False, False)

    background_image = PhotoImage(file='bloodcells-ff-2.png')

    canvas = Canvas(root, width='1080', height='500', highlightthickness=0)
    canvas.create_image(0, 0, image=background_image, anchor='nw')
    canvas.pack(side = "top", fill = "both", expand = True)

    titleLabel1 = canvas.create_text(410, 32, text='ADMIN', anchor='nw', font=('Century Gothic', 28, 'bold'), fill='white')
    titleLabel2 = canvas.create_text(540, 32, text='Login', anchor='nw', font=('Century Gothic', 25), fill='white')

    sText = canvas.create_text(300, 170, text='Sign In', anchor='nw', font=('Century Gothic', 15, 'bold'), fill='white')
    altText = canvas.create_text(300, 200, text='Fill in details to gain access', anchor='nw', font=('Century Gothic', 13, 'italic'), fill='white')

    userEntry = Entry(root, relief='flat')
    userEntry.pack(padx='400', pady='60')
    userEntry.place(x=390, y=250)

main()
root.mainloop()