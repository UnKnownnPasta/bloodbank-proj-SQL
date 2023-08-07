import os

# --- Function to fetch absolute path to a file
def pathLoad(path): 
    return os.path.join(os.path.dirname(__file__), path)

# --- Custom functions to create entries/buttons 
def create_entry(control, varx, vary, text, **kwargs):
    from tkinter import Entry
    kwargs.setdefault('bd', 16)
    kwargs.setdefault('relief', 'flat')
    
    entry = Entry(control, **kwargs)
    entry.place(x=varx, y=vary)
    entry.insert(0, text)
    return entry

def create_button(control, text, varx, vary, **kwargs):
    from tkinter import Button
    kwargs.setdefault('activebackground', '#FF5733')
    kwargs.setdefault('background', '#EE4B2B')

    button = Button(control, text=text, padx=35, pady=10, font=('Century Gothic', 11), bd=0, **kwargs)
    button.pack()
    button.place(x=varx, y=vary)
    return button


# --- Preload all images and icons
def create_images():
    from tkinter import PhotoImage
    images = dict()
    image_paths = [
        'backgrounds/bg-blur-v2.png',   'backgrounds/bg-unblur.png',
        'icons/logo-80.png',            'icons/logo-120.png',
        'icons/profile.png',            ['icons/arrow.png', 'icons/arrow_2.png'],
        'icons/box.png',                'backgrounds/bg-auth.png',
        'backgrounds/button.png',       'icons/lg.png'
    ]

    for index, path in enumerate(image_paths):
        if isinstance(path, str):
            images[index] = PhotoImage(file=pathLoad('resources/' + path))
        else:
            images[index] = []
            images[index].append(PhotoImage(file=pathLoad('resources/' + path[0])))
            images[index].append(PhotoImage(file=pathLoad('resources/' + path[1])))
    
    return images