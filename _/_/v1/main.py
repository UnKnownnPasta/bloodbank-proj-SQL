from tkinter import *
from tkinter import messagebox
import mysql.connector as sql
root = Tk()
# img = PhotoImage(file='plus.png')
db = 'school'
password = 'root'

def create_label(tw, text, x, y, font):
    label = Label(tw, text=text, font=font)
    label.place(x=x, y=y)
    return label

def create_entry(tw, width, x, y):
    entry = Entry(tw, font=('Candara', 15), width=width)
    entry.place(x=x, y=y)
    return entry

def create_button(tw, cmd, text, x, y):
    buttonLooks = {
            'relief':FLAT, 'padx':20, 'font':('Century Gothic', 15),
            'bg':'#808080', 'fg':'white', 'activebackground':'#808083', 'activeforeground':'white'
    }
    button = Button(tw, command= cmd, text=text, **buttonLooks)
    button.place(x=x, y=y)
    return button

def main(): # Login Screen
    global root, signinLabel, usernameLbl, passwLbl, unField, pwField, loginBtn
    root.title('Blood Bank Management')
    # root.iconphoto(False, img)
    root.geometry('400x300')
    root.resizable(False, False)
    
    signinLabel = create_label(root, 'LOG IN', 165, 10, ('Bahnschrift', 20, 'bold'))
    usernameLbl = create_label(root, 'Username', 50, 100, ('Cascadia Code', 10, 'italic'))
    passwLbl = create_label(root, 'Password', 50, 140, ('Cascadia Code', 10, 'italic'))

    unField = Entry(root)
    unField.place(x=150, y=100)

    pwField = Entry(root, show='*')
    pwField.place(x=150, y=140)

    loginBtn = Button(root, text='Submit', relief=RIDGE, padx=40, command=lambda: unpwCheck(str(unField.get()), str(pwField.get())))
    loginBtn.place(x=150, y=200)


# Function that verifies the login Details
def unpwCheck(un, pw): # username, password
    # To access current login screen widgets
    widgets = [signinLabel, usernameLbl, passwLbl, unField, pwField, loginBtn]

    # Check Login Details
    if un != 'aecs' or pw != password:
        messagebox.showerror('Error', 'Invalid Login details')
    else:
        # Remove widgets as we're going out of login screen
        for i in widgets:
            i.destroy()
        
        # Here we call the main interface. If any error occurs during startup, the following if statements will handle it
        status = detailsWindow(pw)
        if status == 'error': # if there is a error while running detailsWindow()
            messagebox.showerror('Error', 'Please login again')
            main() # Return to login screen


# Function that handles the main window after login
def detailsWindow(passw) -> None:
    con = sql.connect(host='localhost', user='root', password=passw)

    if con.is_connected():
        root.geometry('700x500') # Resize window
        cur = con.cursor()
        cur.execute('use %s'%(db,))
        con.commit()

        text_1 = create_label(root, '| INITIALIZE', 40, 15, ('Franklin Gothic', 20))

        OutputLbl = create_label(root, 'Output', 40, 330, ('Arial', 8))
        OutputLbl.config(width=90, justify=LEFT, height=12, bg='white', highlightbackground="black", highlightthickness=1, padx=6)
      
        # A dictionary containing all color, border font stuff of buttons
        buttonLooks = {
             'relief':FLAT, 'padx':20, 'font':('Century Gothic', 15),
             'bg':'#808080', 'fg':'white', 'activebackground':'#808083', 'activeforeground':'white'
        }

        clearOutput = create_button(root, lambda: clearOpt(), 'CLEAR', 40, 290)
        intializeButton = create_button(root, lambda: checkTable(), 'Check Tables', 40, 65)
        createButton = create_button(root, lambda: createTable(), 'Create Tables', 240, 65)

        text_2 = create_label(root, '| COMMANDS', 40, 120, ('Franklin Gothic', 20))

        QueryBtn = create_button(root, lambda: Query(), 'Query', 40, 170)
        InsertBtn = create_button(root, lambda: Insert(), 'Insert Record', 160, 170)
        DeleteBtn = create_button(root, lambda: Destroy(), 'Delete Record', 349, 170)
        UpdateBtn = create_button(root, lambda: Update(), 'Update Record', 40, 215)

        def clearOpt(): OutputLbl['text'] = ''

        # Function to check if the tables Donor and Receiver already exist
        def checkTable():
            clearOpt()
            checkQuery = f"SHOW TABLES FROM {db} LIKE %s;"
            tables = [[False, 'Donor'], [False, 'Receiver']] # Storing the result here
            cur = con.cursor()

            for i in tables: # check both tables
                cur.execute(checkQuery, (i[1],)) # Execute the query with the table name as a parameter
                row = cur.fetchone() # return None if table doesn't exist, which evaluates to False
                if row == None:
                    OutputLbl['text'] += f'   {i[1]} table was not found     '
                else:
                    OutputLbl['text'] += f'   {i[1]} table was found     '

        # Function to create Donor and Receiver table
        def createTable():
            createQuery_1 = "create table if not exists Donor (DonorID int(3) primary key not null unique, DonorName char(20), DonorAge int(2), DonorAddress char(20), BloodType char(3))"
            createQuery_2 = "create table if not exists Receiver (ReceiverID int(3) primary key not null unique, DonorID int, foreign key (DonorID) references Donor(DonorID), ReceiverName char(20), ReceiverAge int(2), ReceiverAddress char(20), BloodGroup char(3), Date date)"

            cur.execute(createQuery_1)
            cur.execute(createQuery_2)
            
            OutputLbl['text'] = 'Donor and Receiver tables are ready'

        def Query():
            win_1 = Toplevel(root)
            win_1.geometry('500x300')
            win_1.title('')
            # win_1.iconphoto(False, img)
            win_1.resizable(False, False)

            heading = create_label(win_1, '| QUERY', 40, 15, ('Franklin Gothic', 20))

            lbl_1 = create_label(win_1, 'SELECT *', 40, 67, ('Candara', 17))
            lbl_2 = create_label(win_1, 'FROM', 40, 107, ('Candara', 17))
            lbl_3 = create_label(win_1, 'WHERE', 40, 147, ('Candara', 17))
            lbl_4 = create_label(win_1, 'ORDER BY', 40, 187, ('Candara', 17))
            
            # selectEntry_1 = create_entry(win_1, 10, 120, 70)
            selectEntry_2 = create_entry(win_1, 10, 110, 110)
            selectEntry_3 = create_entry(win_1, 30, 125, 150)
            selectEntry_4 = create_entry(win_1, 15, 150, 190)
            
            btn = Button(win_1, text='Submit', **buttonLooks, command= lambda: doQuery())
            btn.place(x=100, y=240)


            def doQuery():
                # statement = "SELECT %s FROM %s"%(selecEntry_1.get(), selectEntry_2.get())
                statement = "SELECT * FROM %s"%(selectEntry_2.get(),)
                if selectEntry_3.get() != '':
                    statement += ' WHERE %s'%(selectEntry_3.get(),)
                if selectEntry_4.get() != '':
                    statement += ' ORDER BY %s'%(selectEntry_4.get(),)

                try:
                    cur.execute(statement)
                except:
                    OutputLbl['text'] = 'Failed to run Query.'
                    return

                rows = cur.fetchall()
                t = '{:<10}{:<20}{:<10}{:<20}{:<10}'
                v = '{:<10}{:<12}{:<15}{:<12}{:<20}{:<10}{:<10}'

                if selectEntry_2.get().lower() == 'donor':
                    header = t.format('DonorID', 'DonorName', 'DonorAge', 'DonorAddress', 'BloodType')                        
                else:
                    header = v.format('DonorID', 'ReceiverID', 'ReceiverName', 'ReceiverAge', 'ReceiverAddress', 'BloodType', 'Date')

                output = [header]  # store the lines in a list

                for row in rows:
                    if selectEntry_2.get().lower() == 'donor':
                        line = t.format(*row)
                    else:
                        line = v.format(*[str(i) for i in row])
                    output.append(line)

                OutputLbl['text'] = '\n'.join(output)

        def Insert():
            win_2 = Toplevel(root)
            win_2.geometry('500x300')
            win_2.title('')
            # win_2.iconphoto(False, img)
            win_2.resizable(False, False)

            heading = create_label(win_2, '| INSERT', 40, 15, ('Franklin Gothic', 20))

            Lbl_1 = create_label(win_2, 'INSERT INTO', 40, 67, ('Candara', 17))
            Lbl_2 = create_label(win_2, 'VALUES (..)', 40, 107, ('Candara', 17))
            selectEntry_1 = create_entry(win_2, 15, 180, 70)
            selectEntry_2 = create_entry(win_2, 40, 40, 145)

            btn = create_button(win_2, lambda: doInsert(), 'Submit', 100, 240)

            def doInsert():
                statement = "INSERT INTO %s VALUES %s"%(selectEntry_1.get(), selectEntry_2.get())
                try:
                    cur.execute(statement)
                    con.commit()
                    OutputLbl['text'] = 'Successfully inserted record into %s table!\nValues: %s'%(selectEntry_1.get(), selectEntry_2.get())
                except:
                    OutputLbl['text'] = 'Failed to insert record.'
                    return

        def Destroy():
            win_3 = Toplevel(root)
            win_3.geometry('500x300')
            win_3.title('')
            # win_3.iconphoto(False, img)
            win_3.resizable(False, False)

            heading = create_label(win_3, '| DELETE', 40, 15, ('Franklin Gothic', 20))

            Lbl1 = create_label(win_3, 'DELETE FROM', 40, 67, ('Candara', 17))
            Lbl2 = create_label(win_3, 'WHERE', 40, 107, ('Candara', 17))
            selectEntry_1 = create_entry(win_3, 15, 190, 70)
            selectEntry_2 = create_entry(win_3, 40, 40, 145)

            btn = create_button(win_3, lambda: doDelete(), 'Submit', 100, 240)

            def doDelete():
                statement = "DELETE FROM %s WHERE %s" % (selectEntry_1.get(), selectEntry_2.get())
                try:
                    cur.execute(statement)
                    con.commit()
                    OutputLbl['text'] = f"Successfully removed record from {selectEntry_1.get()} table!"
                except:
                    OutputLbl['text'] = 'Failed to delete record.'
                    return

        def Update():
            win_4 = Toplevel(root)
            win_4.geometry('500x300')
            win_4.title('')
            # win_4.iconphoto(False, img)
            win_4.resizable(False, False)

            heading = create_label(win_4, '| UPDATE', 40, 15, ('Franklin Gothic', 20))

            global setField_2, setValue_2, setField_3, setValue_3, setField_3, setValue_3
            Lbl_1 = create_label(win_4, 'UPDATE', 40, 67, ('Candara', 17))
            selectEntry_1 = create_entry(win_4, 15, 130, 70)
            Lbl_2 = create_label(win_4, 'SET                           =', 40, 107, ('Candara', 17))
            setField_2 = create_entry(win_4, 10, 90, 107)
            setValue_2 = create_entry(win_4, 10, 240, 107)

            Lbl_3 = create_label(win_4, 'SET                           =', 40, 147, ('Candara', 17))
            setField_3 = create_entry(win_4, 10, 90, 147)
            setValue_3 = create_entry(win_4, 10, 240, 147)

            Lbl_4 = create_label(win_4, 'WHERE                          =', 40, 187, ('Candara', 17))
            setField_4 = create_entry(win_4, 10, 125, 187)
            setValue_4 = create_entry(win_4, 10, 265, 187)

            btn = create_button(win_4, lambda: doUpdate(), 'Submit', 100, 240)

            def doUpdate():
                setList = []

                for i in range(1,3):
                    a = eval('setField_' + str(i+1)).get()
                    b = eval('setValue_' + str(i+1)).get()

                    if a == '' and b == '' and i == 0:
                        OutputLbl['text'] = 'No SET values mentioned.'
                        return
                    elif a != '' and b!= '':
                        setList.append((a, b))
                statement = "UPDATE %s SET "%(selectEntry_1.get(),)

                for i in setList:
                    if statement[-1] == ' ':
                        statement += f"{i[0]} = '{i[1]}'"
                    statement += f", {i[0]} = '{i[1]}'"

                statement += " WHERE %s = '%s'"%(setField_4.get(), setValue_4.get())

                try:
                    cur.execute(statement)
                    con.commit()
                    OutputLbl['text'] = 'Successfully updated record!'
                except:
                    OutputLbl['text'] = 'Failed to update record.'
                    return
    else:
        return 'error'

if __name__ == '__main__':
    main()
    root.mainloop()
