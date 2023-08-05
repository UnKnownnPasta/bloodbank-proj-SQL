from tkinter import Entry, Button, Label, messagebox

def pinVerify(pin) -> True:
    if not pin.isdigit() or pin[0] == '0' or len(pin) != 6:
        return False
    invalid = [29, 35, 54, 55, 65, 66]
    if pin[:2] in invalid:
        return False
    return True

from __main__ import signup_var, login_var

# -------------------------------- Switch between Login and Signup (Admin) --------------------------------

# def switchS_L():
#     from authenticate import AdminLogin

#     for widget in signup_var:
#         widget.destroy()
#     data = AdminLogin()
#     login_var = list(data.__dict__.values())

# def switchL_S():
#     from authenticate import AdminSignUp

#     for widget in login_var:
#         widget.destroy()
#     data = AdminSignUp()
#     signup_var = list(data.__dict__.values())


# ------------------ Custom functions to create entries/buttons to reduce boilerplate code ------------------

def create_entry(control, varx, vary, text, *args, **kwargs):
    entry = Entry(control, args,  bd=16, relief="flat", **kwargs)
    entry.place(x=varx, y=vary)
    entry.insert(0, text)
    return entry

def create_button(control, text, varx, vary, **kwargs):
    if 'activebackground' not in kwargs: kwargs['activebackground'] = '#FF5733'
    if 'background' not in kwargs: kwargs['background'] = '#EE4B2B'      # Add bg color if it's not mentioned

    button = Button(control, text=text, relief="flat", padx=35, pady=10, font=('Century Gothic', 11), bd=0, **kwargs)
    button.pack()
    button.place(x=varx, y=vary)
    return button


# ---------------------------------- Handling submitting From Login/Signup ----------------------------------

# for verifying info from signup screen (admin) and adding to database
def Verify_Credentials(postCode, contact, hospName, passwrd):
    verf = pinVerify(postCode)

#     if verf == False:
#         messagebox.showerror('Failed', 'Invalid Pin Code.')
#         return

#     if hospName == 'Hospital Name' or len(hospName) == 0:
#         messagebox.showerror('Failed', 'Invalid Hospital Name.')
#         return

#     if len(contact) == 0 or contact == 'Contact (Phone No./email)':
#         messagebox.showerror('Failed', 'No Valid Contacts provided.')
#         return
        
#     try:
#         vals = (hospName.replace(' ', '_'), passwrd.replace(' ', '_'), contact, postCode)
#         query = "insert into Hospital (HospitalName, Password, Contact, PinCode) values (%s, %s, %s, %s)"

#         app.cursor.execute(query, vals)
#         app.connection.commit()
#     except:
#         messagebox.showerror('Error', 'Failed to signup. Try again.')
#     else:
#         messagebox.showinfo('Success', 'Account created successfully! Login to it here')
#         switchS_L()


# # for verifying info from login screen (admin)
# def Admin_SignIn(un, pw):
#     un, pw = un.replace(' ', '_'), pw.replace(' ', '_')
#     for i in [un, pw]:
#         accessFilter = ['User Name', 'Password', ' ']

#         if i in accessFilter or len(i) == '' or isinstance(i, int):
#             messagebox.showerror('Error', 'Invalid login details')
#             return

#     query = "select * from hospital where HospitalName=%s and Password=%s"
#     values = (un, pw)

#     app.cursor.execute(query, values)
#     res = app.cursor.fetchone()

#     if res == None:
#         messagebox.showerror('Error', 'Login details are not correct.')
#         return

#     app.cursor.execute('select HospitalID, PinCode from Hospital where HospitalName="%s"' % ( un, ))
    
#     info_list = [un, pw] + [i for i in app.cursor.fetchall()[0]]

#     from adminpages import AdminApp
#     app.launchAdminApp(*info_list)