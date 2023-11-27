from tkinter import *
from tkinter import messagebox
import mysql.connector as sql

root = Tk()

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
    root.iconphoto(False, PhotoImage(file='./plus.png'))
    root.geometry('400x300')
    root.resizable(False, False)
    
    signinLabel = create_label(root, 'LOG IN', 165, 10, ('Bahnschrift', 20, 'bold'))
    usernameLbl = create_label(root, 'Username', 50, 100, ('Cascadia Code', 10, 'italic'))
    passwLbl = create_label(root, 'Password', 50, 140, ('Cascadia Code', 10, 'italic'))

    unField = Entry(root)
    unField.place(x=150, y=100)

    pwField = Entry(root, show='*')
    pwField.place(x=150, y=140)

    loginBtn = Button(root, text='Submit', relief=RIDGE, padx=40, command=lambda: unpwCheck(unField.get(), pwField.get()))
    loginBtn.place(x=150, y=200)


# Function that verifies the login Details
def unpwCheck(un, pw): # username, password
    # To access current login screen widgets
    widgets = [signinLabel, usernameLbl, passwLbl, unField, pwField, loginBtn]

    # Check Login Details
    if (un != '' or pw !=''):
        return messagebox.showerror('Error', 'Invalid Login details')
    elif un == '' and pw == '':
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
    con = sql.connect(host='localhost', user='root', password='root')

    if con.is_connected():
        root.geometry('700x500') # Resize window
        cur = con.cursor()
        cur.execute('use school')
        con.commit()

        text_1 = create_label(root, '| INITIALIZE', 40, 15, ('Franklin Gothic', 20))

        OutputLbl = create_label(root, 'Output', 40, 360, ('Courier New', 8))
        OutputLbl.config(width=90, justify=LEFT, height=6, bg='white', highlightbackground="black", highlightthickness=1)
      
        # A dictionary containing all color, border font stuff of buttons
        buttonLooks = {
             'relief':FLAT, 'padx':20, 'font':('Century Gothic', 15),
             'bg':'#808080', 'fg':'white', 'activebackground':'#808083', 'activeforeground':'white'
        }

        clearOutput = create_button(root, lambda: clearOpt(), 'CLEAR', 40, 320)
        intializeButton = create_button(root, lambda: checkTable(), 'Check Tables', 40, 65)
        createButton = create_button(root, lambda: createTable(), 'Create Tables', 240, 65)

        text_2 = create_label(root, '| COMMANDS', 40, 120, ('Franklin Gothic', 20))

        QueryBtn = Button(root, command= lambda: Query(), text='Query',  **buttonLooks)
        QueryBtn.place(x=40, y=170)
        InsertBtn = Button(root, command= lambda: Insert(), text='Insert Record',  **buttonLooks)
        InsertBtn.place(x=160, y=170)
        DeleteBtn = Button(root, command= lambda: Destroy(), text='Delete Record',  **buttonLooks)
        DeleteBtn.place(x=350, y=170)

        def clearOpt(): OutputLbl['text'] = ''

        # Function to check if the tables Donor and Receiver already exist
        def checkTable():
            clearOpt()
            checkQuery = "SHOW TABLES FROM school LIKE %s"
            tables = [[False, 'Donor'], [False, 'Receiver']] # Storing the result here
            cur = con.cursor()

            for i in tables: # check both tables
                cur.execute(checkQuery, (i[1],)) # [1] gives the table name
                row = cur.fetchone() # return None if table doesn't exist, which evaluates to False
                if row: # 
                    OutputLbl['text'] += f'   {i[1]} table was found     '
                else:
                    OutputLbl['text'] += f'   {i[1]} table was not found     '

        # Function to create Donor and Receiver tabke
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
            win_1.iconphoto(False, PhotoImage(file='plus.png'))
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

                cur.execute(statement)

                rows = cur.fetchall()
                t = '{:<10}{:<20}{:<10}{:<20}{:<10}'
                v = '{:<10}{:<10}{:<15}{:<10}{:<15}{:<10}{:<10}'

                if selectEntry_2.get() == 'Donor':
                    header = t.format('DonorID', 'DonorName', 'DonorAge', 'DonorAddress', 'BloodType')                        
                else:
                    header = v.format('DonorID', 'RID', 'RName', 'RAge', 'RAddress', 'BloodType', 'Date')

                output = [header]  # store the lines in a list

                for row in rows:
                    if selectEntry_2.get() == 'Donor':
                        line = t.format(*row)
                    else:
                        line = v.format(*[str(i) for i in row])
                    output.append(line)

                OutputLbl['text'] = '\n'.join(output)

        def Insert():
            win_2 = Toplevel(root)
            win_2.geometry('500x300')
            win_2.title('')
            win_2.iconphoto(False, PhotoImage(file='plus.png'))
            win_2.resizable(False, False)

            heading = create_label(win_1, '| INSERT', 40, 15, ('Franklin Gothic', 20))

            Lbl_1 = create_label(win_2, 'INSERT INTO', 40, 67, ('Candara', 17))
            Lbl_2 = create_label(win_2, 'VALUES (..)', 40, 107, ('Candara', 17))
            selectEntry_1 = create_entry(win_2, 15, 180, 70)
            selectEntry_2 = create_entry(win_2, 40, 40, 145)

            btn = Button(win_2, text='Submit', **buttonLooks, command= lambda: doInsert())
            btn.place(x=100, y=240)


            def doInsert():
                statement = "INSERT INTO %s VALUES %s"%(selectEntry_1.get(), selectEntry_2.get())
                try:
                    cur.execute(statement)
                    con.commit()
                    OutputLbl['text'] = 'Successfully inserted record into %s table!\nValues: %s'%(selectEntry_1.get(), selectEntry_2.get())
                except:
                    OutputLbl['text'] = 'Failed to insert record.'

        def Destroy():
            win_3 = Toplevel(root)
            win_3.geometry('500x300')
            win_3.title('')
            win_3.iconphoto(False, PhotoImage(file='plus.png'))
            win_3.resizable(False, False)

            heading = create_label(win_1, '| DELETE', 40, 15, ('Franklin Gothic', 20))

            Lbl1 = create_label(win_3, 'DELETE FROM', 40, 67, ('Candara', 17))
            Lbl2 = create_label(win_3, 'WHERE', 40, 107, ('Candara', 17))
            selectEntry_1 = create_entry(win_3, 15, 190, 70)
            selectEntry_2 = create_entry(win_3, 40, 40, 145)

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