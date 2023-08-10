from tkinter import Frame, Label, Button, font

# To store hospital and user names
HOPSITAL = ""
USER = ""


def top_frame(ctrl, img):
    global titleFrame, HOPSITAL
    titleFrame = Frame(ctrl, width=920, height=45, bg='#c85038')
    titleFrame.place(x=10, y=10)

    home_logo = Label(titleFrame, image=img[2], bg='#c85038')
    home_logo.place(x=10, y=0)

    logout_button = Button(titleFrame, image=img[9],
        bg='#c85038', relief="flat", bd=0, activebackground='#c85038', command= lambda: destroy(ctrl)
    )
    logout_button.place(x=870, y=4)


def display_info(frame, text1, text2, x1, y1, x2, y2, ):
    small_text = Label(frame, bg='#7B1818', text=text1, font=('Bahnscrift', 12), fg='white')
    small_text.place(x=x1, y=y1)

    underlined_font = font.Font(family='Josefin Sans', size=25, underline=True)
    sub_text = Label(frame, text=text2, font=underlined_font, fg='white', bg='#7B1818')
    sub_text.place(x=x2, y=y2)

    small_text.lift()


def main_info_frame(ctrl, img):
    global con, USER

    infoFrame = Frame(ctrl, bg='#7B1818', width=435, height=425)
    infoFrame.place(x=10, y=65)

    hospitalFrame = Frame(ctrl, bg='#7B1818', width=475, height=425)
    hospitalFrame.place(x=455, y=65)

    cur = con.cursor()
    cur.execute(f"select * from recipient where Name='{USER}'")
    data = cur.fetchone()
    if data == None:
        data = [0000, '', 00, '-', '-', 0]
    cur.execute(f"select count(*) from record where ID={data[0]}")

    name = Label(ctrl, bg='#7B1818', width=10, height=1, text=USER, fg='white', anchor="center",
                 font=font.Font(family='Josefin Sans', size=25, underline=True))
    name.place(x=70, y=90)

    profile_icon = Label(infoFrame, image=img[4], bg='#7B1818')
    profile_icon.place(x=20, y=40)

    display_info(infoFrame, 'AGE', data[2], 23, 120, 23, 130)
    display_info(infoFrame, 'SEX', data[3].title(), 150, 120, 150, 130)
    display_info(infoFrame, 'BLOOD TYPE', data[4], 23, 200, 23, 210)
    display_info(infoFrame, 'TOTAL DONATION/TRANSFUSION COUNT', cur.fetchone()[0], 23, 280, 23, 290)

def user_window(hosp, usr, root, img):
    global HOPSITAL, USER
    HOPSITAL, USER = hosp, usr
    root.configure(bg='#710302')

    from __main__ import connection
    global con
    con = connection

    # Create top frame
    top_frame(root, img)

    # Main visible frame
    main_info_frame(root, img)

def destroy(src):
    for w in list(src.__dict__['children'].values()):
        w.destroy()

    from views.welcome import welcome_screen
    welcome_screen(src)
