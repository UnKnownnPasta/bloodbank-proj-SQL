# -- Function to delete ALL Labels, images, entries, canvases
def wipe_page(source):
    # Get all widgets
    widget_list = list(source.winfo_children())
    for widget in widget_list:
        widget.destroy()
        

# --- Custom function to create entries with default values
def create_entry(control, X, Y, text, **kwargs):
    from tkinter import Entry
    
    kwargs.setdefault('bd', 16)
    kwargs.setdefault('relief', 'flat')
    
    entry = Entry(control, **kwargs)
    entry.place(x=X, y=Y)
    entry.insert(0, text)
    return entry


# --- Custom function to create buttons with default values
def create_button(control, text, X, Y, **kwargs):
    from tkinter import Button

    defaults = {
        'activebackground': '#FF5733',
        'background': '#EE4B2B',
        'font': ('Century Gothic', 11),
        'bd': 0,
        'padx': 35,
        'pady': 10
    }
    for option, value in defaults.items():
        kwargs.setdefault(option, value)

    button = Button(control, text=text, **kwargs)
    button.pack()
    button.place(x=X, y=Y)
    return button


# --- Custom functions to create labels
def create_label(control, text, X, Y, **kwargs):
    from tkinter import Label

    label = Label(control, text=text, **kwargs)
    label.pack()
    label.place(x=X, y=Y)
    return label


# -- Create a Label, Entry combo
def create_entry_label(ctrl, text, x1, y1, x2, y2, w):
    nm = create_entry(ctrl, x1, y1, '', width=w)
    lbl = create_label(ctrl, text, x2, y2, font=('Josefin Sans', 18))
    return nm

# --- Preload all images and Icon
def create_images():
    from tkinter import PhotoImage

    image_paths_dict = {
        0: 'Icon/reload.png',      1: 'Background/bg.png',
        2: 'Background/shadow_bg.png',  

        3: 'Icon/home.png',      4: 'Icon/icon_shadow.png',   5: 'Icon/logo-80.png',
        6: 'Icon/logo-shadow.png',    7: 'Icon/logout.png',   8: 'Icon/menu.png',
        9: 'Icon/profile.png',     10: 'Icon/profile-big.png'
    }

    for index, path in image_paths_dict.items():
        image_paths_dict[index] = PhotoImage(file= './Assets/' + path)
    
    return image_paths_dict