from __main__ import app, globalImages, pathLoad
from helper import pinVerify, create_button, create_entry
from tkinter import *
from tkinter import messagebox


class AdminApp:
    def __init__(self, user, passw, hid, pin):
        self.hosp_name = user
        self.password = passw
        self.hosp_id = hid
        self.pincode = pin

        self.topRoot = Toplevel(app.root)
        self.topRoot.withdraw()
        self.topRoot.protocol('WM_DELETE_WINDOW', self.DEL_EVENT)
        self.storage = ["", 0]
    
        self.scrollbar = Label(app.root, font=("Arial", 12), anchor=NE, bg="black", fg="white", width=104)
        self.scrollbar.place(x=0, y=0)
        self.program()


    # ------------------ Scrolling Text (top) ------------------

    def scroll_text(self, txt):
        self.storage[0] += txt
        if len(self.storage[0]) > 140:
            self.storage[0] = '  '.join(self.storage[0].split('  ')[7:])
        self.scrollbar.configure(text=self.storage[0])

        def rotate(): # Text Capacity = 187 + word length
            text = self.scrollbar.cget("text")
            if len(text) >= 187+len(self.storage[0]):
                self.storage[0] = ""
            self.scrollbar.config(text=text + "  ")
            self.scrollbar.after(100, rotate)

        if not self.storage[1]:
            self.storage[1] = 1; rotate()


    # ---------------------- Main Program ----------------------

    def program(self):
        global img, scrollbar

        self.title_bar = Frame(app.root, bg="#D22B2B", height=30)
        self.title_bar.pack(fill=X)
        self.title_bar.place(rely=0.045, relwidth=1)
        img = [PhotoImage(file=pathLoad('src/menu.png')), PhotoImage(file=pathLoad('src/cog.png'))]

        btnLooks = {
            "bg":"#D22B2B", "relief":"flat", "activebackground":"#D22B2B"
        }
        menu_btn = Button(self.title_bar, image=img[0], **btnLooks, command= lambda: self.menu())
        menu_btn.pack(side=LEFT)
        logo_lbl = Label(self.title_bar, bg="#D22B2B", image=globalImages[2])
        logo_lbl.pack(side=LEFT, padx=10)

        title_label = Label(self.title_bar, text=self.hosp_name.title(), fg="white", bg="#D22B2B", font=('Josefin Sans', 17), pady=0)
        title_label.place(x=95, y=0)

        profile_btn = create_button(self.title_bar, '', 830, 0, background='#d22b2b', activebackground='#d22b2b',
            image=globalImages[4], command= lambda: self.profile()
        )
        settings_btn = create_button(self.title_bar, '', 880, 0, background='#d22b2b', activebackground='#d22b2b', image=img[1])

        self.scroll_text(f'   Welcome {self.hosp_name.title()}!   ')
        self.active = False


    # ------------------------ Menu View ------------------------

    def menu(self):
        if self.active == True:
            self.home_bar.destroy()
            self.active = False; return
        else: self.active = True

        self.home_bar = Frame(app.root, bg="#D22B2B", highlightthickness=2, highlightbackground='black')
        self.home_bar.pack(fill=Y)
        self.home_bar.place(relx=0, rely=0.138, relheight=1, relwidth=0.25)

        optionLooks = {
            "font": ("Corbel", 15), "padx":10, "relief": "flat", "fg": "white", "underline": 4,
            "activeforeground":"white", "background":"#D22B2B", "activebackground":"#D22B2B"
        }
        option_1 = Button(self.home_bar, text='⦿    Donate Blood', **optionLooks, command= lambda: dntBld())
        option_2 = Button(self.home_bar, text='⦿    Retrieve Blood', **optionLooks, command= lambda: retrBld())
        option_3 = Button(self.home_bar, text='⦿    See Blood Bank', **optionLooks, command= lambda: bloodBnk())

        option_1.place(x=20, y=30)
        option_2.place(x=20, y=100)
        option_3.place(x=20, y=170)

        def dropFrame(txt):
            self.active = False; self.home_bar.destroy() # Make
            self.scroll_text(txt)
            try: frame_bb.destroy()
            except: pass

        def dntBld(): dropFrame('    Now Donating Blood    ')
        def retrBld(): dropFrame('    Now Retrieving Blood    ')

        def bloodBnk():
            dropFrame('    Now Managing Blood Database    ')



    # ---------------------- Profile View ----------------------

    def profile(self):
        self.topRoot.deiconify()
        self.profBg = PhotoImage(file=pathLoad('bg/profile-page.png'))

        self.profCanvas = Canvas(self.topRoot, width=500, height=400)
        self.profCanvas.pack(fill=BOTH)
        self.profCanvas.create_image(0, 0, image=self.profBg, anchor=NW)
        self.profCanvas.create_image(53, 53, image=globalImages[4], anchor=NW)

        vals = {"font":('Josefin Sans', 27), "fill":"white", "anchor": "nw"}

        self.profCanvas.create_text(60, 90, text=f'{self.hosp_name.title()}', **vals)
        self.profCanvas.create_text(60, 130, text=f'Reg. ID: ' + f'{self.hosp_id}'.zfill(4), **vals)
        Pin = self.profCanvas.create_text(60, 170, text=f'Pin Code: {self.pincode}', **vals)

        editBtn = create_button(self.topRoot, 'Edit Pin Code', 60, 300, command= lambda: editProfile())
        editBtn_leave = create_button(self.topRoot, 'Stop Editing', 60, 300, command= lambda: profileStopEdit())
        editBtn_save = create_button(self.topRoot, 'Save Pin Code', 60, 300, command= lambda: profileSaveEdit())

        self.pinEntry = create_entry(self.topRoot, -200, -180, '')

        def placeNegative(widget: list):
            for i in widget:
                i.place(x=-50, y=-50)

        def placeWidgets(widget: list):
            for i in widget:
                i[0].place(x=i[1][0], y=i[1][1])

        placeNegative([editBtn_leave, editBtn_save])

        def editProfile():
            placeWidgets([[self.pinEntry, [200, 180]], [editBtn_leave, [60, 300]], [editBtn_save, [240, 300]]])
            placeNegative([editBtn])

        def profileStopEdit():
            placeWidgets([[editBtn, [60, 300]]])
            placeNegative([editBtn_leave, editBtn_save, self.pinEntry])

        def profileSaveEdit():
            query = "update hospital set PinCode=%s where HospitalID=%s"
            pinVal = self.pinEntry.get()

            if pinVerify(pinVal) == True:
                values = (pinVal, self.hosp_id)
                app.cursor.execute(query, values)
                app.connection.commit(); 

                self.pincode = pinVal
                self.profCanvas.itemconfigure(Pin, text=f'Pin Code: {self.pincode}')
            profileStopEdit()


    # ------------------ Close Profile Function ------------------

    def DEL_EVENT(self): 
        self.topRoot.withdraw()
        self.profCanvas.destroy()