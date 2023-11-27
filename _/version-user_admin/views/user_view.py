from tkinter import *
from tkinter import font, ttk, messagebox
from utils import create_button, create_entry

# To store hospital and user names
HOPSITAL = ""
USER = ""


def top_frame(ctrl, img):
    global titleFrame, HOPSITAL
    titleFrame = Frame(ctrl, width=920, height=45, bg='#c85038')
    titleFrame.place(x=10, y=10)

    home_logo = Label(titleFrame, image=img[10], bg='#c85038')
    home_logo.place(x=10, y=0)

    logout_button = Button(titleFrame, image=img[8],
        bg='#c85038', relief="flat", bd=0, activebackground='#c85038', command= lambda: destroy(ctrl)
    )
    logout_button.place(x=870, y=4)

# --------------- Helper function
def display_info(frame, text1, text2, x1, y1, x2, y2, ):
    small_text = Label(frame, bg='#7B1818', text=text1, font=('Bahnscrift', 12), fg='white')
    small_text.place(x=x1, y=y1)

    underlined_font = font.Font(family='Josefin Sans', size=25, underline=True)
    sub_text = Label(frame, text=text2, font=underlined_font, fg='white', bg='#7B1818')
    sub_text.place(x=x2, y=y2)

    small_text.lift()


# -------------- Left and right side of page
def main_info_frame(ctrl, img):
    global cur, USER, b1, b2, data

    # ----------------- Left Side
    infoFrame = Frame(ctrl, bg='#7B1818', width=435, height=425)
    infoFrame.place(x=10, y=65)

    cur.execute(f"select * from recipient where Name='{USER}'")
    data = cur.fetchone()
    if data == None: data = [0000, '', 00, '-', '-', 0]

    iflbl = Label(infoFrame, text='Your Information ', bg='#841d1d', fg='white', padx=3, width=27, height=1, font=('Josefin Sans', 20))
    iflbl.place(x=10, y=15)

    name = Label(ctrl, bg='#7B1818', width=10, height=1, text=USER, fg='white', anchor="center",
                 font=font.Font(family='Josefin Sans', size=25, underline=True))
    name.place(x=70, y=150)

    profile_icon = Label(infoFrame, image=img[7], bg='#7B1818')
    profile_icon.place(x=20, y=100)

    display_info(infoFrame, 'AGE', data[2], 23, 160, 23, 170)
    display_info(infoFrame, 'SEX', data[3].title(), 150, 160, 150, 170)
    display_info(infoFrame, 'BLOOD TYPE', data[4], 280, 160, 280, 170)

    # ----------------- Right Side
    global hospitalFrame
    hospitalFrame = Frame(ctrl, bg='#7B1818', width=475, height=425)
    hospitalFrame.place(x=455, y=65)

    hplbl = Label(hospitalFrame, text='Request services', bg='#841d1d', fg='white', width=30, height=1, font=('Josefin Sans', 20))
    hplbl.place(x=10, y=15)

    def reset():
        global b1, b2, hospitalFrame
        for i in list(hospitalFrame.__dict__['children'].values()):
            if i['text'] != 'Request services': i.destroy()

        b1 = create_button(hospitalFrame, 'Donate Blood (Transfusion)', 55, 100, padx=80, command= lambda: appoint())
        b2 = create_button(hospitalFrame, 'Request Blood', 55, 200, padx=124, command= lambda: request())
    reset()


    # ---------- Functionality buttons
    def request():
        global b1, b2, hosptialFrame, data
        b1.destroy(); b2.destroy()

        blood_qty_label = Label(hospitalFrame, text="Enter Quantity of Blood Required:", bg='#7B1818', font=('Josefin Sans', 17), fg='white')
        blood_qty_label.place(x=20, y=80)

        blood_qty_entry = create_entry(hospitalFrame, 350, 80, "", width=10)

        hospital_label = Label(hospitalFrame, text="Hospital:", bg='#7B1818', font=('Josefin Sans', 17), fg='white')
        hospital_label.place(x=20, y=130)

        hospitals = ['Hospital A', 'Hospital B', 'Hospital C']  # Replace with actual hospital names
        selected_hospital = StringVar()
        hospital_combobox = ttk.Combobox(hospitalFrame, textvariable=selected_hospital, values=hospitals, state="readonly")
        hospital_combobox.place(x=120, y=145)

        pref_date_label = Label(hospitalFrame, text="Preferred Date of Appointment:", bg='#7B1818', font=('Josefin Sans', 17), fg='white')
        pref_date_label.place(x=20, y=180)
        pref_date_entry = create_entry(hospitalFrame, 20, 230, "")

        def validate_info():
            if '' not in [selected_hospital.get().strip(), blood_qty_entry.get().strip(), pref_date_entry.get().strip()]:
                messagebox.showinfo('Successful', f'Arranged a appointment in {selected_hospital.get().title()}!')
                reset()
            else: messagebox.showerror('Error', 'Choose all required options')
        
        create_button(hospitalFrame, "Request", 100, 310, command=lambda:validate_info())
        create_button(hospitalFrame, "Back", 260, 310, command=lambda: reset())


    def appoint():
        global b1, b2, cur, con
        b1.destroy(); b2.destroy()

        hospital_label = Label(hospitalFrame, text="Hospital:", bg='#7B1818', font=('Josefin Sans', 17), fg='white')
        hospital_label.place(x=20, y=65)

        hospitals = ['Hospital A', 'Hospital B', 'Hospital C']  # Replace with actual hospital names
        selected_hospital = StringVar()
        hospital_combobox = ttk.Combobox(hospitalFrame, textvariable=selected_hospital, values=hospitals, state="readonly")
        hospital_combobox.place(x=120, y=80)

        illness_label = Label(hospitalFrame, text="Info on any current/past illness:", bg='#7B1818', font=('Josefin Sans', 17), fg='white')
        illness_label.place(x=20, y=100)

        illness_entry = create_entry(hospitalFrame, 20, 150, "", width=67)

        pref_date_label = Label(hospitalFrame, text="Preferred Date of Appointment:", bg='#7B1818', font=('Josefin Sans', 17), fg='white')
        pref_date_label.place(x=20, y=210)
        pref_date_entry = create_entry(hospitalFrame, 20, 260, "")

        def validate_info():
            if '' not in [selected_hospital.get().strip(), illness_entry.get().strip(), pref_date_entry.get().strip()]:
                messagebox.showinfo('Successful', f'Arranged a appointment in {selected_hospital.get().title()}!')
                cur.execute(f'update bloodtable set Units = Units+1 where concat(BloodType, RhFactor)="{data[4]}"')
                con.commit()
                reset()
            else: messagebox.showerror('Error', 'Choose all required options')
        
        create_button(hospitalFrame, "Donate", 100, 350, command=lambda:validate_info())
        create_button(hospitalFrame, "Back", 260, 350, command=lambda: reset())



# --------------- Main functions
def user_window(hosp, usr, root, img):
    global HOPSITAL, USER
    HOPSITAL, USER = hosp, usr
    root.configure(bg='#710302')

    from __main__ import cursor, connection
    global cur, con
    cur, con = cursor, connection

    # Create top frame
    top_frame(root, img)

    # Main visible frame
    main_info_frame(root, img)

def destroy(src):
    for w in list(src.__dict__['children'].values()):
        w.destroy()

    from views.welcome import welcome_screen
    welcome_screen(src)
