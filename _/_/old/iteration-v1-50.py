from tkinter import *
from tkinter import messagebox
import mysql.connector as sql

root = Tk()

def main(): # Login Screen
    global root, signinLabel, usernameLbl, passwLbl, unField, pwField, loginBtn
    root.title('Blood bank mng')
    root.iconphoto(False, PhotoImage(file='./plus.png'))
    root.geometry('400x300')
    root.resizable(False, False)
    
    signinLabel = Label(root, text='LOG IN', font=('Bahnschrift', 20, 'bold'))

    signinLabel.place(y=10, relx=0.4)

    usernameLbl = Label(root, text='Username', font=('Cascadia Code', 10, 'italic'))
    usernameLbl.place(x=50, y=100)

    passwLbl = Label(root, text='Password', font=('Cascadia Code', 10, 'italic'))
    passwLbl.place(x=50, y=140)

    unField = Entry(root)
    unField.place(x = 150, y=100)

    pwField = Entry(root, show='*')
    pwField.place(x = 150, y=140)

    loginBtn = Button(root, text='Submit', relief=RIDGE, padx=40, command= lambda: unpwCheck(unField.get(), pwField.get()))
    loginBtn.place(x=150, y=200)


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


# Function that handles the main window after login
def detailsWindow(passw) -> None:
    con = sql.connect(host='localhost', user='root', password='root')

    if con.is_connected():
        root.geometry('700x500') # Resize window
        cur = con.cursor()
        cur.execute('use school')
        con.commit()

        text_1 = Label(root, text='| INITIALIZE', font=('Franklin Gothic', 20))
        text_1.place(x=40, y=15)

        OutputLbl = Label(root, text='Output', font=('Bahnscrift', 12), width=66, justify=LEFT, height=6, bg='white', highlightbackground="black", highlightthickness=1)
        OutputLbl.place(x=40, y=360)
      
        # A dictionary containing all color, border font stuff of buttons
        buttonLooks = {
             'relief':FLAT, 'padx':20, 'font':('Century Gothic', 15),
             'bg':'#808080', 'fg':'white', 'activebackground':'#808083', 'activeforeground':'white'
        }

        clearOutput = Button(root, command= lambda: clearOpt(), text='CLEAR', relief=FLAT, padx=20, font=('Century Gothic', 8),
             bg='#808080', fg='white', activebackground='#808083', activeforeground='white')
        clearOutput.place(x=40, y=332)

        intializeButton = Button(root, command= lambda: checkTable(), text='Check Tables', **buttonLooks)
        intializeButton.place(x=40, y=65)

        createButton = Button(root, command= lambda: createTable(), text='Create Tables', **buttonLooks)
        createButton.place(x=240, y=65)

        text_2 = Label(root, text='| COMMANDS', font=('Franklin Gothic', 20))
        text_2.place(x=40, y=120)

        QueryDonor = Button(root, command= lambda: Query('Donor'), text='Query on Donor',  **buttonLooks)
        QueryDonor.place(x=40, y=170)
        QueryReceiver = Button(root, command= lambda: Query('Receiver'), text='Query on Receiver',  **buttonLooks)
        QueryReceiver.place(x=263, y=170)

        def clearOpt(): OutputLbl['text'] = ''

        # Function to check if the tables Donor and Receiver already exist
        def checkTable():
            checkQuery = "SHOW TABLES FROM school LIKE %s"
            tables = [[False, 'Donor'], [False, 'Receiver']] # Storing the result here
            cursor = con.cursor()
            OutputLbl['text'] = ''

            for i in tables: # check both tables
                cursor.execute(checkQuery, (i[1],))
                row = cursor.fetchone()
                if row: # i[1] gives the table name (see 'tables' list)
                    OutputLbl['text'] += f'   {i[1]} table was found     '
                else:
                    OutputLbl['text'] += f'   {i[1]} table was not found     '

        # Function to create Donor and Receiver tabke
        def createTable():
            cursor = con.cursor()
            createQuery_1 = "create table Donor (DonorID int(3) primary key not null unique, DonorName char(20), DonorAge int(2), DonorAddress char(20), BloodType char(3))"
            createQuery_2 = "create table Receiver (ReceiverID int(3) primary key not null unique, DonorID int, foreign key (DonorID) references Donor(DonorID), ReceiverName char(20), ReceiverAge int(2), ReceiverAddress char(20), BloodGroup char(3), Date date)"

            cursor.execute(createQuery_1)
            cursor.execute(createQuery_2)
            
            OutputLbl['text'] = 'Created both tables.'

        def Query(tbl):
            win = Toplevel(root)
            win.geometry('500x300')
            win.title('')
            win.iconphoto(False, PhotoImage(file='plus.png'))
            win.resizable(False, False)

            heading_1 = Label(win, text='| QUERY', font=('Franklin Gothic', 20))
            heading_1.place(x=40, y=15)

            heading_2 = Label(win, text='| VALUES', font=('Franklin Gothic', 20))
            heading_2.place(x=40, y=120)

            field_1 = Entry(win, width=39, relief=FLAT, bg='#808080', fg='white', font=('Bahnscrift', 15))
            field_1.place(x=41, y=70)

            field_2 = Entry(win, width=39, relief=FLAT, bg='#808080', fg='white', font=('Bahnscrift', 15))
            field_2.place(x=41, y=173)
            
            btn = Button(win, text='Submit', **buttonLooks, command= lambda: func())
            btn.place(x=100, y=240)
            OutputLbl['text'] = ''

            def func():
                cursor = con.cursor()
                query = field_1.get()
                values = field_2.get()

                cur.execute(query, values)

                res = cur.fetchall()
                t = '{:<10}{:<20}{:<10}{:<20}{:<10}'
                v = '{:<10}{:<10}{:<20}{:<10}{:<20}{:<10}{:<15}'
                if tbl == 'Donor':
                    OutputLbl['text'] = t.format('ID', 'Name', 'Age', 'Address', 'BloodType')
                else:
                    OutputLbl['text'] = v.format('D_ID', 'ID', 'Name', 'Age', 'Address', 'BloodType', 'Date')
                for row in res:
                    for x in row:
                        x = str(x).strip()
                    if tbl == 'Donor':
                        OutputLbl['text'] += '\n' + t.format(row[0], row[1], row[2], row[3], row[4])
                    elif tbl == 'Receiver':
                        OutputLbl['text'] += '\n' + t.format(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7])

    else:
        return 'error'

if __name__ == '__main__':
    main()
    root.mainloop()