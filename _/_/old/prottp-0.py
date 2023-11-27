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

        OutputLbl = Label(root, text='Output', font=('Courier New', 8), width=90, justify=LEFT, height=6, bg='white', highlightbackground="black", highlightthickness=1)
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

        QueryBtn = Button(root, command= lambda: Query(), text='Query',  **buttonLooks)
        QueryBtn.place(x=40, y=170)
        InsertBtn = Button(root, command= lambda: Insert(), text='Insert Record',  **buttonLooks)
        InsertBtn.place(x=160, y=170)
        InsertBtn = Button(root, command= lambda: Destroy(), text='Delete Record',  **buttonLooks)
        InsertBtn.place(x=350, y=170)

        def clearOpt(): OutputLbl['text'] = ''

        # Function to check if the tables Donor and Receiver already exist
        def checkTable():
            checkQuery = "SHOW TABLES FROM school LIKE %s"
            tables = [[False, 'Donor'], [False, 'Receiver']] # Storing the result here
            cursor = con.cursor()


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
            createQuery_1 = "create table if not exists Donor (DonorID int(3) primary key not null unique, DonorName char(20), DonorAge int(2), DonorAddress char(20), BloodType char(3))"
            createQuery_2 = "create table if not exists Receiver (ReceiverID int(3) primary key not null unique, DonorID int, foreign key (DonorID) references Donor(DonorID), ReceiverName char(20), ReceiverAge int(2), ReceiverAddress char(20), BloodGroup char(3), Date date)"

            cursor.execute(createQuery_1)
            cursor.execute(createQuery_2)
            
            OutputLbl['text'] = 'Donor and Receiver tables are ready'

        def Query():
            win_1 = Toplevel(root)
            win_1.geometry('500x300')
            win_1.title('')
            win_1.iconphoto(False, PhotoImage(file='plus.png'))
            win_1.resizable(False, False)

            heading = Label(win_1, text='| QUERY', font=('Franklin Gothic', 20))
            heading.place(x=40, y=15)

            lbl_1 = Label(win_1, text='SELECT', font=('Candara', 17))
            lbl_2 = Label(win_1, text='FROM', font=('Candara', 17))
            lbl_3 = Label(win_1, text='WHERE', font=('Candara', 17))
            lbl_4 = Label(win_1, text='ORDER BY', font=('Candara', 17))
            selectEntry_1 = Entry(win_1, font=('Candara', 15), width=15) # what to select
            selectEntry_2 = Entry(win_1, font=('Candara', 15), width=10) # which table
            selectEntry_3 = Entry(win_1, font=('Candara', 15), width=15) # where condition
            selectEntry_4 = Entry(win_1, font=('Candara', 15), width=15) # order by condition
            
            lbl_1.place(x=40, y=67)
            selectEntry_1.place(x=120, y=70)
            lbl_2.place(x=40, y=107)
            selectEntry_2.place(x=120, y=110)
            lbl_3.place(x=40, y=147)
            selectEntry_3.place(x=125, y=150)
            lbl_4.place(x=40, y=187)
            selectEntry_4.place(x=150, y=190)
            
            btn = Button(win_1, text='Submit', **buttonLooks, command= lambda: doQuery())
            btn.place(x=100, y=240)


            def doQuery():
                statement = "SELECT %s FROM %s"%(selectEntry_1.get(), selectEntry_2.get())
                if selectEntry_3.get() != '':
                    statement += ' WHERE %s'%(selectEntry_3.get(),)
                if selectEntry_4.get() != '':
                    statement += ' ORDER BY %s'%(selectEntry_4.get(),)

                cur.execute(statement)

                rows = cur.fetchall()
                t = '{:<10}{:<20}{:<10}{:<20}{:<10}'
                v = '{:<10}{:<10}{:<15}{:<10}{:<15}{:<10}{:<10}'

                if selectEntry_2.get() == 'Donor':
                    header = t.format('DonorID', 'DonorName', 'DonorAge', 'DonorAddress', 'BloodType')
                else:
                    header = v.format('DonorID', 'RID', 'RName', 'RAge', 'RAddress', 'BloodType', 'Date')

                output = [header]  # Store the lines in a list

                for row in rows:
                    row = [str(x).strip() for x in row]  # Trim whitespace from each item
                    if selectEntry_2.get() == 'Donor':
                        line = t.format(*[str(i) for i in row])  # Take only the first 5 items
                    else:
                        line = v.format(*[str(i) for i in row])  # Take only the first 7 items
                    output.append(line)

                OutputLbl['text'] = '\n'.join(output)

        def Insert():
            win_2 = Toplevel(root)
            win_2.geometry('500x300')
            win_2.title('')
            win_2.iconphoto(False, PhotoImage(file='plus.png'))
            win_2.resizable(False, False)

            heading = Label(win_2, text='| INSERT', font=('Franklin Gothic', 20))
            heading.place(x=40, y=15)

            Lbl_1 = Label(win_2, text='INSERT INTO', font=('Candara', 17))
            Lbl_2 = Label(win_2, text='VALUES (..)', font=('Candara', 17))
            selectEntry_1 = Entry(win_2, font=('Candara', 15), width=15) # which table
            selectEntry_2 = Entry(win_2, font=('Candara', 15), width=40) # values

            Lbl_1.place(x=40, y=67)
            selectEntry_1.place(x=180, y=70)
            Lbl_2.place(x=40, y=107)
            selectEntry_2.place(x=40, y=145)

            btn = Button(win_2, text='Submit', **buttonLooks, command= lambda: doInsert())
            btn.place(x=100, y=240)


            def doInsert():
                statement = "INSERT INTO %s VALUES %s"%(selectEntry_1.get(), selectEntry_2.get())
                print(statement)

                # try:
                #     cur.execute(statement)
                #     con.commit()
                # except:
                #     OutputLbl['text'] = 'Failed to insert record.'
                cur.execute(statement)

                rows = cur.fetchall()
                success = 'Successfully inserted record into %s table!\nValues: %s'%(selectEntry_1.get(), selectEntry_2.get())
                OutputLbl['text'] = success

        def Destroy():
            win_3 = Toplevel(root)
            win_3.geometry('500x300')
            win_3.title('')
            win_3.iconphoto(False, PhotoImage(file='plus.png'))
            win_3.resizable(False, False)

            heading = Label(win_3, text='| INSERT', font=('Franklin Gothic', 20))
            heading.place(x=40, y=15)

            Lbl1 = Label(win_3, text='DELETE FROM', font=('Candara', 17))
            Lbl2 = Label(win_3, text='WHERE', font=('Candara', 17))
            selectEntry_1 = Entry(win_3, font=('Candara', 15), width=15)  # which table
            selectEntry_2 = Entry(win_3, font=('Candara', 15), width=40)  # which record

            Lbl1.place(x=40, y=67)
            selectEntry_1.place(x=190, y=70)
            Lbl2.place(x=40, y=107)
            selectEntry_2.place(x=40, y=145)

            btn = Button(win_3, text='Submit', **buttonLooks, command=lambda: doDelete())
            btn.place(x=100, y=240)


            def doDelete():
                statement = "DELETE FROM %s WHERE %s" % (selectEntry_1.get(), selectEntry_2.get())

                try:
                    cur.execute(statement)
                    con.commit()
                    OutputLbl['text'] = f"Successfully removed record from {selectEntry_1.get()} table!"
                except:
                    OutputLbl['text'] = 'Failed to delete record.'


    else:
        return 'error'

if __name__ == '__main__':
    main()
    root.mainloop()