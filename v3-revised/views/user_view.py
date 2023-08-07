from tkinter import *

def top_frame(ctrl):
    global titleFrame
    titleFrame = Frame(root, width=920, height=45, bg='#c85038')
    titleFrame.place(x=10, y=10)

    home_logo = Label(titleFrame, image=img[2], bg='#c85038')
    home_logo.place(x=10, y=0)

    logout_button = Button(titleFrame, image=img[9],
        bg='#c85038', relief=FLAT, bd=0, activebackground='#c85038', command=lambda: destroy()
    )
    logout_button.place(x=870, y=4)

    Name = Label(titleFrame, text=hosp, bg='#c85038', font=('Calibri Light', 24), fg='white')
    Name.place(x=55)

def user_window(hosp, usr, root, img):
    root.configure(bg='#710302')

    # Create top frame
    top_frame(root)

    # Main visible frame
    mainFrame = Frame(root, bg='#7B1818', width=920, height=425)
    mainFrame.place(x=10, y=65)

def destroy():
    for w in list(root.__dict__['children'].values()):
        w.destroy()
    from views.welcome import welcome_screen
    welcome_screen(root)