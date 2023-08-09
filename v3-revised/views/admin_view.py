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
    img = [PhotoImage(file=pathLoad('resources/icons/menu.png')), PhotoImage(file=pathLoad('resources/icons/cog.png'))]

    btnLooks = {
        "bg":"#D22B2B", "relief":"flat", "activebackground":"#D22B2B"
    }
    menu_btn = Button(title_bar, image=img[0], **btnLooks, command= lambda: side_bar())
    menu_btn.pack(side=LEFT)
    logo_lbl = Label(title_bar, bg="#D22B2B", image=globalImages[2])
    logo_lbl.pack(side=LEFT, padx=10)

    title_label = Label(title_bar, text=hosp_name.title(), fg="white", bg="#D22B2B", font=('Josefin Sans', 17), pady=0)
    title_label.place(x=95, y=0)

    profile_btn = create_button(title_bar, '', 830, 0, background='#d22b2b', activebackground='#d22b2b',
        image=globalImages[4], command= lambda: sub_profile_view()
    )
    settings_btn = create_button(title_bar, '', 880, 0, background='#d22b2b', activebackground='#d22b2b', image=img[1])

    scroll_text(f'   Welcome {hosp_name.title()}!   ')
    active = False # Whether side-menu is open or not


# ------------------------ Side Bar -------------------------

def side_bar():
    global home_bar, active, root
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
    option_1 = Button(home_bar, text='⦿    Donate Blood', **optionLooks, command= lambda: dntBld())
    option_2 = Button(home_bar, text='⦿    Retrieve Blood', **optionLooks, command= lambda: retrBld())
    option_3 = Button(home_bar, text='⦿    See Blood Bank', **optionLooks, command= lambda: bloodBnk())
    option_4 = Button(home_bar, text='EXIT', **optionLooks, command= lambda: opt_4())

    option_1.place(x=16, y=30)
    option_2.place(x=16, y=100)
    option_3.place(x=16, y=170)
    option_4.place(x=10, y=380)

    def dropFrame(txt):
        global active
        active = False; home_bar.destroy()
        scroll_text(txt)
        try: frame_bb.destroy()
        except: pass

    def dntBld(): dropFrame('    Now Donating Blood    ')
    def retrBld(): dropFrame('    Now Retrieving Blood    ')
    def bloodBnk():dropFrame('    Now Managing Blood Database    ')
    # To be continued

    def opt_4():
        a = list(root.__dict__['children'].values())
        for widget in a:
            widget.destroy()
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
        query = "update hospital set PinCode=%s where HospitalID=%s"
        pinVal = pinEntry.get()

        if pinVerify(pinVal) == True:
            values = (pinVal, hosp_id)
            app.cursor.execute(query, values)
            app.connection.commit(); 

            pincode = pinVal
            profCanvas.itemconfigure(Pin, text=f'Pin Code: {pincode}')
        profileStopEdit()


# ------------------ Close Profile Function ------------------

def DEL_EVENT():
    global topRoot, profCanvas
    topRoot.withdraw()
    profCanvas.destroy()