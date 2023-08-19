from tkinter import *
from utils import create_button, create_entry, pinVerify
from __main__ import cursor, connection

def load_page(root, images, data):
    global topRoot, globalImages, admin
    topRoot = root
    globalImages = images
    admin = data

    sub_profile_view()

def sub_profile_view():
    global topRoot, profCanvas, globalImages, admin

    topRoot.deiconify()

    profCanvas = Canvas(topRoot, width=500, height=400)
    profCanvas.pack(fill=BOTH)
    profCanvas.create_image(0, 0, image=globalImages[3], anchor=NW)
    profCanvas.create_image(53, 53, image=globalImages[7], anchor=NW)

    text_style  = {"font":('Josefin Sans', 27), "fill":"white", "anchor": "nw"}

    profCanvas.create_text(60, 90, text=f'{admin["Name"].title()}', **text_style )
    profCanvas.create_text(60, 130, text=f'Reg. ID: ' + f'{admin["ID"]}'.zfill(4), **text_style )
    Pin = profCanvas.create_text(60, 170, text=f'Pin Code: {admin["Pin"]}', **text_style )

    editBtn = create_button(topRoot, 'Edit Pin Code', 60, 300, command= lambda: edit_profile())
    editBtn_stop = create_button(topRoot, 'Stop Editing', 60, 300, command= lambda: stop_profile_edit())
    editBtn_save = create_button(topRoot, 'Save Pin Code', 60, 300, command= lambda: save_profile_edit())

    pinEntry = create_entry(topRoot, -200, -180, '')

    def place_at_negative(widget_list: list):
        for widget in widget_list:
            widget.place(x=-50, y=-50)

    def place_widgets(widget_list: list):
        for widget in widget_list:
            widget[0].place(x=widget[1][0], y=widget[1][1])

    place_at_negative([editBtn_stop, editBtn_save])

    def edit_profile():
        place_widgets([[pinEntry, [200, 180]], [editBtn_stop, [60, 300]], [editBtn_save, [240, 300]]])
        place_at_negative([editBtn])

    def stop_profile_edit():
        place_widgets([[editBtn, [60, 300]]])
        place_at_negative([editBtn_stop, editBtn_save, pinEntry])

    def save_profile_edit():
        query = "update hospital set PinCode=%s where HospitalName=%s"
        pinVal = pinEntry.get()

        if pinVerify(pinVal) == True:
            values = (pinVal, hosp_name)
            cursor.execute(query, values)
            connection.commit()

            profCanvas.itemconfigure(Pin, text=f'Pin Code: {pinVal}')
        stop_profile_edit()


def DEL_EVENT():
    global topRoot, profCanvas
    topRoot.withdraw()
    profCanvas.destroy()