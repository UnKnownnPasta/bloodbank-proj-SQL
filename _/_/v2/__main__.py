from tkinter import messagebox
from tkinter import *
import mysql.connector as sql
from re import findall
import os

current_dir = os.path.dirname(__file__)
import functions as f
import helper as h


#   TODO
#       - btn on menu 
#       - menu swap
#       - settings
#       - logout/login
#       - profile sys
#       - connect db each time a option is parked
#       - polish
#

def SignSubm(postCode, contact, hospName, passwrd):
    verf = h.pinVerify(postCode)
    if verf == False:
        messagebox.showerror('Failed', 'Invalid Pin Code.')
        return
    if hospName == 'Hospital Name' or len(hospName) == 0:
        messagebox.showerror('Failed', 'Invalid Hospital Name.')
        return
    if len(contact) == 0 or contact == 'Contact (Phone No./email)':
        messagebox.showerror('Failed', 'No Valid Contacts provided.')
        return
        
    try:
        vals = (hospName, passwrd, contact, postCode)
        query = "insert into Hospital (HospitalName, Password, Contact, PinCode) values (%s, %s, %s, %s)"
        f.cur.execute(query, vals)
        f.con.commit()
    except:
        messagebox.showerror('Error', 'Failed to signup. Try again.')
        return

    messagebox.showinfo('Success', 'Account created successfully! Login to it here')
    f.switchS_L()


def loginSubm(un, pw):
    for i in [un, pw]:
        if i == 'User Name' or i == 'Password' or len(i) == '' or i == ' ':
            messagebox.showerror('Error', 'Invalid login details')
            return
    query = "select * from hospital where HospitalName=%s and Password=%s"
    values = (un, pw)
    f.cur.execute(query, values)
    res = f.cur.fetchone()
    if res == None:
        messagebox.showerror('Error', 'Login details are not correct.')
        return
    f.cur.execute('select HospitalID, PinCode from Hospital where HospitalName=%s', (un,))
    hId, pc = [i for i in f.cur.fetchall()[0]]
    program(un, pw, hId, pc)


def DEL_EVENT(): 
    f.topRoot.withdraw();
    profCanvas.destroy()


def program(u, p, i, pc):
    ww = [f.canvasLi, f.userName, f.userPass, f.submBtnLi, f.signBtnLi]
    for x in ww:
        x.destroy()
    global img, title_bar, scrollbar
        
    title_bar = Frame(f.root, bg="#D22B2B", height=30)
    title_bar.pack(fill=X)
    title_bar.place(rely=0.045, relwidth=1)
    img = [PhotoImage(file=h.osDirFetch('src/menu.png')), PhotoImage(file=h.osDirFetch('src/cog.png'))]

    btnLooks = {
        "bg":"#D22B2B", "relief":"flat", "activebackground":"#D22B2B"
    }
    menu_btn = Button(title_bar, image=img[0], text='menu', **btnLooks, command= lambda: menu())
    menu_btn.pack(side=LEFT)
    logo_lbl = Label(title_bar, bg="#D22B2B", image=f.globalImg[2])
    logo_lbl.pack(side=LEFT, padx=10)

    title_label = Label(title_bar, text=u.title(), fg="white", bg="#D22B2B", font=('Josefin Sans', 17), pady=0)
    title_label.place(x=95, y=0)

    profile_btn = h.create_button(title_bar, '', 830, 0, bg='#d22b2b', activebackground='#d22b2b', image=f.globalImg[4], command= lambda: profile(u, i, pc))
    settings_btn = h.create_button(title_bar, '', 880, 0, bg='#d22b2b', activebackground='#d22b2b', image=img[1])

    global active

    f.scroll_text(f'   Welcome {u.title()}!   ')
    
    active = False
    def menu():
        global active, home_bar
        if active == True:
            home_bar.destroy()
            active = False; return
        else: active = True

        home_bar = Frame(f.root, bg="#D22B2B", highlightthickness=2, highlightbackground='black')
        home_bar.pack(fill=Y)
        home_bar.place(relx=0, rely=0.138, relheight=1, relwidth=0.25) # relwidth gives the fill to be 100%, rely keeps it 500*0.05 = 25 pixels from top

        optionLooks = {
            "font": ("Corbel", 15), "padx":10,
            "fg": "white", "underline": 4,
            "activeforeground":"white",
            "background":"#D22B2B", "activebackground":"#D22B2B"
        }
        option_1 = h.create_button(home_bar, '⦿    Donate Blood', 20, 30, **optionLooks, command= lambda: dntBld())
        option_2 = h.create_button(home_bar, '⦿    Retrieve Blood', 20, 100, **optionLooks, command= lambda: retrBld())
        option_3 = h.create_button(home_bar, '⦿    See Blood Bank', 20, 170, **optionLooks, command= lambda: bloodBnk())

        def dropFrame(txt):
            global active
            active = False; home_bar.destroy() # Make
            f.scroll_text(txt)
            try: frame_bb.destroy()
            except: pass

        def dntBld(): dropFrame('    Now Donating Blood    ')
        def retrBld(): dropFrame('    Now Retrieving Blood    ')

        def bloodBnk():
            dropFrame('    Now Managing Blood Database    ')

        #     global active, frame_bb
        #     frame_bb = Frame(f.root)
        #     frame_bb.pack(fill=BOTH, expand=True)
        #     frame_bb.place(rely=0.138)
            
        #     home_bar.destroy()
        #     active = False

        #     table_data = [
        #         ['BloodType', 'Units', 'Rh'],
        #         ['O', '12', '+'],
        #         ['O', '7', '-'],
        #         ['A', '8', '+'],
        #         ['A', '16', '-'],
        #     ]

        #     for row, data_row in enumerate(table_data, start=1):
        #         for column, data in enumerate(data_row):
        #             label = Label(frame_bb, text=data, relief=GROOVE, width=12)
        #             label.grid(row=row, column=column)
        #             # label.place(x=40 + column * 100, y=150 + row * 30)


def profile(user, hid, pin):
    f.topRoot.deiconify()
    global profBg, profCanvas
    profBg = PhotoImage(file=h.osDirFetch('bg/profile-page.png'))

    profCanvas = Canvas(f.topRoot, width=500, height=400)
    profCanvas.pack(fill=BOTH,)
    profCanvas.create_image(0, 0, image=profBg, anchor=NW)
    profCanvas.create_image(53, 53, image=f.globalImg[4], anchor=NW)

    fonval = ('Josefin Sans', 27)
    profCanvas.create_text(60, 90, text=f'{user.title()}', font=fonval+('bold',), fill='white', anchor=NW)
    profCanvas.create_text(60, 130, text=f'Reg. ID: ' + f'{hid}'.zfill(4), font=fonval, fill='white', anchor=NW)
    profCanvas.create_text(60, 170, text=f'Pin Code: {pin}', font=fonval, fill='white', anchor=NW)

    editBtn = h.create_button(f.topRoot, 'Edit Pin Code', 60, 300, command= lambda: editProfile())
    editBtn_leave = h.create_button(f.topRoot, 'Stop Editing', 60, 300, command= lambda: ep_1())
    editBtn_save = h.create_button(f.topRoot, 'Save Pin Code', 180, 300, command= lambda: ep_2())
    
    negCoord = {"x":-100, "y":-100} # Out of plane
    editBtn_leave.place(**negCoord) # This places it out of view
    editBtn_save.place(**negCoord)
    global pinEntry
    pinEntry = h.create_entry(f.topRoot, -200, -180, '')

    def editProfile():
        pinEntry.place(x=200, y=180)
        editBtn.place(**negCoord)
        editBtn_leave.place(x=60, y=300)
        editBtn_save.place(x=180, y=300)

    def ep_1():
        editBtn.place(x=60, y=300)
        editBtn_leave.place(**negCoord)
        editBtn_save.place(**negCoord)
        pinEntry.place(**negCoord)

    def ep_2():
        query = "update hospital set PinCode=%s where HospitalID=%s"
        pinVal = pinEntry.get()
        if h.pinVerify(pinVal) == True:
            values = (pinVal, hid)
            f.cur.execute(query, values)
            f.con.commit()
            pin = pinVal
            profCanvas.itemconfigure(Pin, text=f'Pin Code: {pin}')
        ep_1()


if __name__ == '__main__':
    # Start program
    f.init()
    # program('abc', 'abc', '234', '4534534')
    f.root.mainloop()