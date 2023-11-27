import functions as f
import __main__ as m

from tkinter import Entry, Button, FLAT, Label
from re import findall
import os

#
#   This module stores helper functions such as
#       - pinVerify() to verify if the entered pin is a valid one
#           * used in SignUp()
#           * used in profile editing
#       - functions to switch from login to sign up and vis. a vis.
#       
#       - QOL Functions:
#           create_entry() to create a Entry() with default params
#           create_button() to create a Button() with default params
#           osDirFetch() to get absolute os path using function modules os.<absolute_path> with join(<relative_path>)
#

def pinVerify(pin) -> True:
    if not pin.isdigit() or pin[0] == '0' or len(pin) != 6:
        return False
    invalid = [29, 35, 54, 55, 65, 66]
    if pin[:2] in invalid:
        return False
    # reg = open(os.path.join(f.current_dir, 'validrange.txt'))
    # status = False
    # for i in range(8):
    #     regx = reg.readline().strip().replace('/', '')
    #     m = findall(regx, pin)
    #     if len(m) != 0:
    #         status = True
    return status


def switchS_L(): # Signup to Login
    w = [f.hospName, f.pinCode, f.Contact, f.submBtnSu, f.canvasSu, f.swchBtnSu, f.PassWord]
    for i in w:
        i.destroy()
    f.Login()
def switchL_S(): # Login to Signup
    w = [f.canvasLi, f.userName, f.userPass, f.submBtnLi, f.signBtnLi]
    for i in w:
        i.destroy()
    f.SignUp()


def create_entry(control, varx, vary, text, *args, **kwargs):
    entry = Entry(control, args,  bd=16, relief=FLAT, **kwargs)
    entry.place(x=varx, y=vary)
    entry.insert(0, text)
    return entry

def create_button(control, text, varx, vary, **kwargs):
    abg = '#6CB4EE' if not kwargs.get('activebackground') else kwargs.get('activebackground')
    bg = '#6CB4EE' if not kwargs.get('background') else kwargs.get('background')
    px = 10 if not kwargs.get('padx') else kwargs.get('padx')
    for i in ['activebackground', 'background', 'padx']:
        kwargs.pop(i, None)
    button = Button(control, text=text, background=bg, relief='flat', padx=px, pady=10, activebackground=abg, **kwargs)
    button.pack()
    button.place(x=varx, y=vary)
    return button

def osDirFetch(path):
    return os.path.join(f.current_dir, path)
