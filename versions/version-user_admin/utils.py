import os


# --- Function to fetch absolute path to a file
def pathLoad(path): 
    return os.path.join(os.path.dirname(__file__), path)


# -- Function to verify given pin code
def pinVerify(pin) -> True:
    if isinstance(pin, str):
        return False
    elif str(pin)[0] == '0' or len(str(pin)) != 6:
        return False
    elif int(str(pin)[:2]) in [29, 35, 54, 55, 65, 66]:
        return False


# --- Custom function to create entries
def create_entry(control, varx, vary, text, **kwargs):
    from tkinter import Entry
    
    # Set default values for the appearance of the input field
    kwargs.setdefault('bd', 16)           # Border thickness
    kwargs.setdefault('relief', 'flat')   # Border style
    
    # Create the input field using the provided parameters and default values
    entry = Entry(control, **kwargs)
    entry.place(x=varx, y=vary)
    entry.insert(0, text)
    return entry


# --- Custom function to create buttons
def create_button(control, text, varx, vary, **kwargs):
    from tkinter import Button

    # Set default values for the appearance of the button
    defaults = (['activebackground', '#FF5733'], ['background', '#EE4B2B'],
    ['font', ('Century Gothic', 11)], ['bd', 0], ['padx', 35], ['pady', 10])
    for i in defaults:
        kwargs.setdefault(i[0], i[1])

    # Create the button using the provided parameters and default values
    button = Button(control, text=text, **kwargs)
    button.pack()
    button.place(x=varx, y=vary)
    return button


# --- Custom functions to create labels
def create_label(control, text, varx, vary, **kwargs):
    from tkinter import Label

    # Create the button using the provided parameters and default values
    label = Label(control, text=text, **kwargs)
    label.pack()
    label.place(x=varx, y=vary)
    return label


# --- Preload all images and icons
def create_images():
    from tkinter import PhotoImage
    images = {}

    image_paths = [
        'backgrounds/bg-blurred.png',   'backgrounds/bg-login.png',
        'backgrounds/button-login.png', 'backgrounds/profile-page.png',
        'backgrounds/admin_welcome.png',

        'icons/logo-80.png',            'icons/logo-120.png',
        'icons/profile.png',            'icons/lg.png',
        'icons/menu.png',               'icons/home.png',
    ]

    for index, path in enumerate(image_paths):
        images[index] = PhotoImage(file=pathLoad('resources/' + path))
    
    return images

