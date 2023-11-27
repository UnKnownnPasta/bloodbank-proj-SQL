from tkinter import messagebox
from tkinter import *
import mysql.connector as sql

global con, cur
con = sql.connect(host='localhost', user='root', password='root')
cur = con.cursor()

root = Tk()

def main():
    # Login window details
    global root, background_image
    root.title('Blood bank mng')
    root.iconphoto(False, PhotoImage(file='plus.png'))
    root.geometry('900x500')
    root.resizable(False, False)

    background_image = PhotoImage(file='bloodcells-ffn.png')

    canvas = Canvas(root, width = 900, height = 500)
    canvas.create_image(0, 0, image=background_image, anchor='nw')
    canvas.pack(side = "top", fill = "both", expand = True)

    titleLabel1 = canvas.create_text(330, 32, anchor = "nw", text='ADMIN', font=('Century Gothic', 28, 'bold'), fill='white')
    titleLabel2 = canvas.create_text(460, 32, anchor = "nw", text='Login', font=('Century Gothic', 25), fill='white')






main()
root.mainloop()

# Function that verifies the login Details
def unpwCheck(un, pw): # username, password
    # To access current login screen widgets
    widgets = [signinLabel, usernameLbl, passwLbl, unField, pwField, loginBtn]

    # Check Login Details
    if (un=='1' or pw=='1') or (un != '' or pw !=''):
        return messagebox.showerror('Error', 'Invalid Login details')
    elif un == '' and pw == '':
        for i in widgets:
            i.destroy() # Remove widgets as we're going out of login screen
    
        status = detailsWindow(pw) # Here we call the main interface. If any error occurs during startup, the following if statements will handle it

        if status == 'error': # if there is a error while running detailsWindow()
            messagebox.showerror('Error', 'Please login again')
            main() # Return to login screen