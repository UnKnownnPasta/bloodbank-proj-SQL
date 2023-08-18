from utils import pathLoad, create_button, create_entry, create_images, wipe_page

# --------------------- Define some basics for login and general program ----------------------

def setText(entry, defaultText):
    if entry.get().strip() == defaultText:
        entry.delete(0, "end")

def restoreText(entry, defaultText):
    if entry.get().strip() == "":
        entry.insert(0, defaultText)

error_count = 0
images = create_images()

# --------------------------------- Welcome page handling -------------------------------------

from tkinter import Canvas, Button, messagebox, Label, Toplevel, Entry
from __main__ import x_coordinate, y_coordinate, cursor, connection
from random import randint

#               ------------------- Preliminary Functions ----------------------              

def create_canvas(control, img):
    canvas = Canvas(control, width=940, height=500, highlightthickness=0)
    canvas.pack(side="top", fill="both", expand=True)
    return canvas

def bind_focus_events(widget, text):
    widget.bind('<FocusIn>', lambda event: setText(widget, text))
    widget.bind('<FocusOut>', lambda event: restoreText(widget, text))


def display_entries(control, img):
    global temp_button
    temp_button.destroy()

    # Login button
    create_button(control, 'Login', 405, 360, command=lambda: validate_inputs(hospital.get(), user.get(), control))

    # Entry to enter hospital name
    hospital = create_entry(control, 240, 240, 'Hospital Name', width=70)
    bind_focus_events(hospital, 'Hospital Name')

    # Entry to enter Citizen's name
    user = create_entry(control, 240, 300, 'Your Name', width=70)
    bind_focus_events(user, 'Your Name')


def display_error():
    global error_count, error_text, canvas

    error_count = error_count + 1
    canvas.itemconfigure(error_text, fill='white', text=f'Invalid Login Details. [{error_count} Attempts]')


def log_out(control):
    # Remove normal login page
    wipe_page(control)
    # Switch to admin login page
    from views.admin_login import admin_login
    admin_login(control)

#              ------------------- Sql Handling Functions ----------------------              

def validate_inputs(hospname: str, usrname: str, control):
    hospname, usrname = hospname.strip(), usrname.strip()

    if len(hospname) == 0 or len(usrname) == 0:
        display_error(); return
    elif hospname.isdigit() or usrname.isdigit():
        display_error(); return

    # Check that the hospital exists
    cursor.execute(f"SELECT COUNT(*) FROM hospital WHERE HospitalName='{hospname}'")
    if cursor.fetchone()[0] == 0:
        display_error(); return

    # See that the Citizen's name does not already exist
    cursor.execute(f"SELECT COUNT(*) FROM recipient WHERE Name='{usrname}'")
    if cursor.fetchone()[0] == 0:
        # If it does, register the citizen
        register_user(control, usrname, hospname); return

    from views.user_view import user_window

    # Remove login screen, switch to user view
    wipe_page(control)
    user_window(hospname, usrname, control, images)


#             ------------------- Code for Registering User ----------------------              
def register_user(source, user, hopsital):
    sub_root_window = Toplevel(source)
    sub_root_window.title('Info Frame')
    sub_root_window.resizable(False, False)
    sub_root_window.iconphoto(False, images[6])
    sub_root_window.geometry(f'250x130+{x_coordinate + 200}+{y_coordinate + 100}')

    value_list = []

    def create_entry_popup(text):
        wipe_page(sub_root_window)

        Label(sub_root_window, text=text).pack()
        entry = create_entry(sub_root_window, 40, 20, '')
        create_button(sub_root_window, "Next", 70, 70, command=lambda:verify_details(entry))

    def verify_details(entry):
        nonlocal value_list
        if len(value_list) == 0 and not entry.get().isdigit() and entry.get() > '100': pass
        elif len(value_list) == 1 and (entry.get().lower() not in ['m', 'f', 'male', 'female']): pass
        elif len(value_list) == 2 and (entry.get()[0] not in ['A', 'B', 'O']): pass
        else:
            value_list.append(entry.get())
            process_entry()

    def process_entry():
        if len(value_list) < 3:
            create_entry_popup(["Enter your Sex:", "Enter your Blood Type:"][len(value_list)-1])
        else:
            # Store user details in the database
            cursor.execute(
                "INSERT INTO recipient VALUES (%s, %s, %s, %s, %s, 0, 0)",
                (randint(1000, 9999), user, int(value_list[0]), value_list[1], value_list[2])
            )
            connection.commit()

            sub_root_window.destroy()
            from views.user_view import user_window
            user_window(hopsital, user, source, images)

    create_entry_popup("Enter your Age:")



# --------------------------------- Opening Welcome Page! -------------------------------------

def welcome_screen(source):
    global canvas, error_text
    # Create the canvas to use
    canvas = create_canvas(source, images)
    canvas.create_image(0, 0, image=images[0], anchor='nw')

    # The "Login >" button
    global temp_button
    temp_button = create_button(source, " ", 310, 250, command=lambda: display_entries(source, images), image=images[2])

    canvas.create_text(377, 85, text='Welcome!!', font=('Hello Sunday', 56), anchor="nw", fill='#303030')
    canvas.create_text(380, 85, text='Welcome!!', font=('Hello Sunday', 55), anchor="nw", fill="#D22B2B")
    canvas.create_image(290, 70, image=images[6], anchor='nw')

    error_text = canvas.create_text(250, 200, text='', font=('Josefin Sans', 16), fill='', anchor="nw")

    # Button to switch to admin login page
    create_button(source, 'OR, LOGIN AS A ADMIN', 350, 450, padx=30, pady=0,
                  relief="solid", activebackground='#D22B2B', bg='#D22B2B', fg='white',
                  command= lambda: log_out(source), borderwidth=1, highlightcolor='black',
                  font=('Calibri Light', 12), activeforeground='white', height=1)