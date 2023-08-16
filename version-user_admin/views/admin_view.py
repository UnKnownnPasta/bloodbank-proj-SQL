from tkinter import *
from utils import pathLoad, create_button, create_entry, create_images, pinVerify

globalImages = create_images()


def admin_view(user, passw, hid, pin, s):
    global hosp_name, password, hosp_id, pincode
    global root, topRoot, storage, scrollbar
    hosp_name = user
    password = passw
    hosp_id = hid
    pincode = pin

    s.configure(bg='white')
    root = s

    topRoot = Toplevel(s)
    topRoot.withdraw()
    topRoot.protocol('WM_DELETE_WINDOW', DEL_EVENT)
    storage = ["", 0]

    scrollbar = Label(root, font=("Arial", 12), anchor=NE, bg="black", fg="white", width=104)
    scrollbar.place(x=0, y=0)
    main_frame_handle()


# ------------------ Scrolling Text (top) ------------------

def scroll_text(txt):
    global storage, scrollbar
    storage[0] += txt
    if len(storage[0]) > 140:
        storage[0] = '  '.join(storage[0].split('  ')[7:])
    scrollbar.configure(text=storage[0])

    def rotate(): # Text Capacity = 187 + word length
        text = scrollbar.cget("text")
        if len(text) >= 187+len(storage[0]):
            storage[0] = ""
        scrollbar.config(text=text + "  ")
        scrollbar.after(100, rotate)

    if not storage[1]:
        storage[1] = 1; rotate()


# ---------------------- Main Program ----------------------

def main_frame_handle():
    global img, scrollbar, storage, root, globalImages
    global hosp_name, password, hosp_id, pincode, active

    title_bar = Frame(root, bg="#D22B2B", height=30)
    title_bar.pack(fill=X)
    title_bar.place(rely=0.045, relwidth=1)
    img = [PhotoImage(file=pathLoad('resources/icons/menu.png')), PhotoImage(file=pathLoad('resources/icons/home.png'))]

    btnLooks = {
        "bg":"#D22B2B", "relief":"flat", "activebackground":"#D22B2B"
    }
    menu_btn = Button(title_bar, image=img[0], **btnLooks, command= lambda: side_bar(hosp_id))
    menu_btn.pack(side=LEFT)
    logo_lbl = Label(title_bar, bg="#D22B2B", image=globalImages[2])
    logo_lbl.pack(side=LEFT, padx=10)

    title_label = Label(title_bar, text=hosp_name.title(), fg="white", bg="#D22B2B", font=('Josefin Sans', 17), pady=0)
    title_label.place(x=95, y=0)

    profile_btn = create_button(title_bar, '', 830, 2, background='#D22B2B', activebackground='#D22B2B',
        image=globalImages[4], command= lambda: sub_profile_view())

    home_btn = create_button(title_bar, '', 880, 2, background='#D22B2B', activebackground='#D22B2B',
        image=img[1], command=lambda: home_page())

    scroll_text(f'   Welcome {hosp_name.title()}!   ')
    active = False # Whether side-menu is open or not

    global ttl, visible_frame

    visible_frame = Frame(root, width=root.winfo_screenwidth(), height=440)
    visible_frame.place(x=0, y=69)

    ttl = Label(visible_frame, text='|    Hospital Management System', font=('Cascadia Code', 22), width=55, bg='#FBFCF8', height=1, anchor='w')
    ttl.place(x=0, y=20)

    def home_page():
        for i in list(visible_frame.__dict__['children'].values()):
            if isinstance(i, Label):
                if not i['text'].startswith('|'): i.destroy()
            else: i.destroy()

        bg = Label(visible_frame, image=globalImages[11])
        bg.place(x=-2, y=-2)
        bg.lower()

        xxx = Label(visible_frame, width=140, bg='#FBFCF8', height=8, font=('Cascadia Code', 17), anchor=NW, justify=LEFT)
        xxx.place(x=-1, y=230)
        xxx['text'] = '\n|   App Guide:\n\n1.     ≡ is to navigate the menu\n2.     Profile button is to update hosptial details'

    home_page()

# ------------------------ Side Bar -------------------------

def side_bar(id):
    global home_bar, active, root, ttl, visible_frame
    if active == True:
        home_bar.destroy()
        active = False; return
    else: active = True

    home_bar = Frame(root, bg="#D22B2B", highlightthickness=2, highlightbackground='black')
    home_bar.pack(fill=Y)
    home_bar.place(relx=0, rely=0.138, relheight=1, relwidth=0.25)

    optionLooks = {
        "font": ("Corbel", 15), "padx":10, "relief": "flat", "fg": "white", "underline": 4,
        "activeforeground":"white", "background":"#D22B2B", "activebackground":"#D22B2B"
    }
    create_button(home_bar, '⦿    Donate/Recieve\nBlood', 16, 30, **optionLooks, command= lambda: menu_options(1))
    create_button(home_bar, '⦿    See Blood Bank', 16, 100, **optionLooks, command= lambda: menu_options(2))
    # create_button(home_bar, '⦿    Add User', 16, 170, **optionLooks, command= lambda: menu_options(3))
    create_button(home_bar, 'EXIT', 10, 380, **optionLooks, command= lambda: menu_options(3))

    def dropFrame(txt):
        global active
        active = False; home_bar.destroy()
        scroll_text(txt)

    def menu_options(c):
        if c == 1:
            dropFrame('    Now Donating Blood    ')
            from views.admin_windows.admin_option_1 import donation_choice
            donation_choice(visible_frame, id, ttl)
            ttl['text'] = '|    Choose an option'

        elif c == 2: 
            dropFrame('    Now Managing Blood Storage    ')
            ttl['text'] = '|    Viewing Blood Storage'
            from views.admin_windows.admin_option_2 import table_data
            table_data(visible_frame, ttl)

        elif c == 3:
            for widget in list(root.__dict__['children'].values()): widget.destroy()

            from views.welcome import welcome_screen
            welcome_screen(root)


# ---------------------- Profile View ----------------------

def sub_profile_view():
    global topRoot, profCanvas, root, globalImages

    topRoot.deiconify()

    profCanvas = Canvas(topRoot, width=500, height=400)
    profCanvas.pack(fill=BOTH)
    profCanvas.create_image(0, 0, image=globalImages[10], anchor=NW)
    profCanvas.create_image(53, 53, image=globalImages[4], anchor=NW)

    vals = {"font":('Josefin Sans', 27), "fill":"white", "anchor": "nw"}

    profCanvas.create_text(60, 90, text=f'{hosp_name.title()}', **vals)
    profCanvas.create_text(60, 130, text=f'Reg. ID: ' + f'{hosp_id}'.zfill(4), **vals)
    Pin = profCanvas.create_text(60, 170, text=f'Pin Code: {pincode}', **vals)

    editBtn = create_button(topRoot, 'Edit Pin Code', 60, 300, command= lambda: editProfile())
    editBtn_leave = create_button(topRoot, 'Stop Editing', 60, 300, command= lambda: profileStopEdit())
    editBtn_save = create_button(topRoot, 'Save Pin Code', 60, 300, command= lambda: profileSaveEdit())

    pinEntry = create_entry(topRoot, -200, -180, '')

    def placeNegative(widget: list):
        for i in widget:
            i.place(x=-50, y=-50)

    def placeWidgets(widget: list):
        for i in widget:
            i[0].place(x=i[1][0], y=i[1][1])

    placeNegative([editBtn_leave, editBtn_save])

    def editProfile():
        placeWidgets([[pinEntry, [200, 180]], [editBtn_leave, [60, 300]], [editBtn_save, [240, 300]]])
        placeNegative([editBtn])

    def profileStopEdit():
        placeWidgets([[editBtn, [60, 300]]])
        placeNegative([editBtn_leave, editBtn_save, pinEntry])

    def profileSaveEdit():
        query = "update hospital set PinCode=%s where HospitalName=%s"
        pinVal = pinEntry.get()

        if pinVerify(pinVal) == True:
            values = (pinVal, hosp_name)
            cursor.execute(query, values)
            connection.commit()

            pincode = pinVal
            profCanvas.itemconfigure(Pin, text=f'Pin Code: {pincode}')
        profileStopEdit()


# ------------------ Close Profile Function ------------------

def DEL_EVENT():
    global topRoot, profCanvas
    topRoot.withdraw()
    profCanvas.destroy()