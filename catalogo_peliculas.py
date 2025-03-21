import tkinter as tk
from client.gui_app import Frame, barra__menu


def main ():
    root = tk.Tk()
    root.title('Mis Peliculas')
    root.iconbitmap('img/icono.ico')
    barra__menu(root)

    app = Frame (root = root)

    root.mainloop()


if __name__ == '__main__':
    main()