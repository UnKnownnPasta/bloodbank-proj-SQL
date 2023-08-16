from utils import pathLoad, create_button, create_entry, create_images

# --------------------- Define some basics for login and general program ----------------------

def setText(entry, defaultText):
    if entry.get().strip() == defaultText:
        entry.delete(0, "end")

def restoreText(entry, defaultText):
    if entry.get().strip() == "":
        entry.insert(0, defaultText)

count = 0

images = create_images()

# --------------------------------- Welcome page handling -------------------------------------

from tkinter import Canvas, Button, messagebox, Label, Toplevel, Entry
import random
from __main__ import x_coordinate, y_coordinate

def create_canvas(src, img):
    canvas = Canvas(src, width=940, height=500, highlightthickness=0)
    canvas.pack(side="top", fill="both", expand=True)
    return canvas

def bind_events(widget, text):
    widget.bind('<FocusIn>', lambda event: setText(widget, text))
    widget.bind('<FocusOut>', lambda event: restoreText(widget, text))

def switch_to_entry(src, img):
    global temporary_button, hospital_name, user_name
    temporary_button.destroy()
    submit = create_button(src, 'Login', 405, 360,
                    command=lambda: validate(hospital_name.get(), user_name.get(), src))

    hospital_name = create_entry(src, 240, 240, 'Hospital Name', width=70)
    bind_events(hospital_name, 'Hospital Name')

    user_name = create_entry(src, 240, 300, 'Your Name', width=70)
    bind_events(user_name, 'Your Name')

def display_error():
    global count, error_text
    count += 1
    canvas.itemconfigure(error_text, fill='white', text=f'Invalid Login Details. [{count}]')


def validate(hospname, usrname, r):
    from views.user_view import user_window
    from __main__ import cursor, connection

    if any(len(value.strip()) == 0 or value in ['Hospital Name', 'Your Name'] or value.isdigit() for value in [hospname, usrname]):
        display_error()
        return

    cursor.execute(f"SELECT COUNT(*) FROM hospital WHERE HospitalName='{hospname}'")
    data = cursor.fetchone()[0]
    if data == 0: display_error(); return

    cursor.execute(f"SELECT COUNT(*) FROM recipient WHERE Name='{usrname}'")
    data = cursor.fetchone()[0]
    print(data)
    if data == 0: open_entry_popup(r=r, cr=cursor, cn=connection, un=usrname, hn=hospname); return

    for widget in list(r.__dict__['children'].values()):
        try: widget.destroy()
        except: pass

    user_window(hospname, usrname, r, images)


def open_entry_popup(r, cr, cn, un, hn):
    global entries, images

    popup = Toplevel(r)
    popup.geometry(f'250x130+{int(x_coordinate)+200}+{int(y_coordinate)+100}')

    entries = []

    def create_entry_popup(text):
        for w in popup.winfo_children():
            w.destroy()

        lbl = Label(popup, text=text); lbl.pack()
        entry = create_entry(popup, 0, 20, ''); entry.pack()
        submit_button = create_button(popup, "Submit", 0, 50, command=lambda:(entries.append(entry.get()), process_entry()))
        submit_button.pack()

    def process_entry():
        if len(entries) < 3:
            create_entry_popup(["Enter your Sex:", "Enter your Blood Type:"][len(entries)-1])
        else:
            cr.execute(
                'INSERT INTO recipient VALUES (%s, %s, %s, %s, %s, 0, 0)',
                (random.randint(1000, 9999), un, int(entries[0]), entries[1], entries[2])
            )
            cn.commit()

            for widget in r.winfo_children():
                try:
                    widget.destroy()
                except:
                    pass
            
            popup.destroy()
            from views.user_view import user_window
            user_window(hn, un, r, images)

    create_entry_popup("Enter your Age:")



def log_out(r):
    # Later admin login part will be added
    a = list(r.__dict__['children'].values())
    for widget in a:
        widget.destroy()

    from views.admin_login import admin_login
    admin_login(r)



# -- The main function that handles the page
def welcome_screen(src):
    global images, canvas, temporary_button, error_text

    canvas = create_canvas(src, images)
    canvas.create_image(0, 0, image=images[7], anchor='nw')

    temporary_button = Button(src, command=lambda: switch_to_entry(src, images),
                              bd=0, activebackground='#D22B2B', bg='#EE4B2B', relief="flat", image=images[8])
    temporary_button.place(x=310, y=250)

    canvas.create_text(377, 85, text='Welcome!!', font=('Hello Sunday', 56), anchor="nw", fill='#303030')
    canvas.create_text(380, 85, text='Welcome!!', font=('Hello Sunday', 55), anchor="nw", fill="#D22B2B")
    canvas.create_image(290, 70, image=images[3], anchor='nw')

    error_text = canvas.create_text(250, 200, text='', font=('Josefin Sans', 16), fill='', anchor="nw")

    switch_label = Button(src, text='Or, Login as an Admin'.upper(), padx=30, pady=0,
                          relief="solid", activebackground='#D22B2B', bg='#D22B2B', fg='white',
                          command= lambda: log_out(src), borderwidth=1, highlightcolor='black',
                          font=('Calibri Light', 12), activeforeground='white', height=1)
    switch_label.place(x=350, y=450)