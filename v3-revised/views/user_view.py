from tkinter import Frame, Label, Button


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


def main_frame(ctrl, img):
    global con, USER

    mainFrame = Frame(ctrl, bg='#7B1818', width=920, height=425)
    mainFrame.place(x=10, y=65)    

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
    main_frame(root, img)

def destroy(src):
    for w in list(src.__dict__['children'].values()):
        w.destroy()

    from views.welcome import welcome_screen
    welcome_screen(src)