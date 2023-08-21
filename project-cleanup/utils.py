import os

# --- Function to fetch absolute path to a file
def pathLoad(path): 
    return os.path.join(os.path.dirname(__file__), path)


# -- Function to delete ALL Labels, images, entries, canvases
def wipe_page(source):
    # Get all widgets
    widget_list = list(source.__dict__['children'].values())
    for widget in widget_list:
        widget.destroy()


# -- Function to verify given pin code
def pinVerify(pin):
    if pin[0] == '0' or len(pin) != 6:
        return False
    elif int(pin[:2]) in [29, 35, 54, 55, 65, 66]:
        return False
    else: return True


# --- Custom function to create entries
def create_entry(control, x_position, y_position, text, **kwargs):
    from tkinter import Entry
    
    # Set default values for the appearance of the input field
    kwargs.setdefault('bd', 16)
    kwargs.setdefault('relief', 'flat')
    
    entry = Entry(control, **kwargs)
    entry.place(x=x_position, y=y_position)
    entry.insert(0, text)
    return entry


# --- Custom function to create buttons
def create_button(control, text, x_position, y_position, **kwargs):
    from tkinter import Button

    # Set default values for the appearance of the button
    defaults = (['activebackground', '#FF5733'], ['background', '#EE4B2B'],
    ['font', ('Century Gothic', 11)], ['bd', 0], ['padx', 35], ['pady', 10])
    for setting in defaults:
        kwargs.setdefault(setting[0], setting[1])

    # Then create the button with all parameters
    button = Button(control, text=text, **kwargs)
    button.pack()
    button.place(x=x_position, y=y_position)
    return button


# --- Custom functions to create labels
def create_label(control, text, x_position, y_position, **kwargs):
    from tkinter import Label

    label = Label(control, text=text, **kwargs)
    label.pack()
    label.place(x=x_position, y=y_position)
    return label


# --- Preload all images and icons
def create_images():
    from tkinter import PhotoImage
    images = {}

    image_paths = [
        'backgrounds/bg-blurred.png',   'backgrounds/bg-login.png',
        'backgrounds/button-login.png', 'backgrounds/profile-page.png',
        'backgrounds/admin_welcome.png',

        'icons/logo-80.png',            'icons/icon.png',
        'icons/profile.png',            'icons/lg.png',
        'icons/menu.png',               'icons/home.png',
    ]

    for index, path in enumerate(image_paths):
        images[index] = PhotoImage(file=pathLoad('resources/' + path))
    
    return images
