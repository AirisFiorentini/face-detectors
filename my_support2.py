import sys
import tkinter as tk
import tkinter.ttk as ttk
from tkinter.constants import *

import my_interface2


def main(*args):
    """Main entry point for the application."""
    global root
    root = tk.Tk()
    root.title("Главное окно")
    root.protocol('WM_DELETE_WINDOW', root.destroy)
    # Creates a toplevel widget.
    global _top1, _w1

    _top1 = root
    _w1 = my_interface2.Toplevel1(_top1)
    root.mainloop()


def Load_Data(*args):
    print('my_support.Load Data')
    for arg in args:
        print('another arg:', arg)
    sys.stdout.flush()


def START(*args):
    print('my_support.START')
    for arg in args:
        print('another arg:', arg)
    sys.stdout.flush()


if __name__ == '__main__':
    my_interface2.start_up()
