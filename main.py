from tkinter import Tk, PhotoImage
import mysql.connector as sql

def start_app():
    root = Tk()
    root.withdraw()

    root.title('Blood Bank System')
    root.iconphoto(False, PhotoImage( file='Assets/Icon/logo-80.png' ))
    root.resizable(False, False)

    x_pos = (root.winfo_screenwidth() - 940) // 2
    y_pos = (root.winfo_screenheight() - 500) // 2
    root.geometry("940x500+" + str(x_pos) +"+" + str(y_pos))

    from database import create_tables
    connection, cursor = create_tables()

    root.deiconify()
    return connection, cursor, root

if __name__ == "__main__":
    con, cur, app = start_app()

    from Scripts import login
    login.show_choice(cur, con, app)

    app.mainloop()