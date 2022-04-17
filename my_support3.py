import sys
import tkinter as tk
import tkinter.ttk as ttk
from tkinter.constants import *

import lab3_interface


def main(*args):
    """Main entry point for the application."""
    global root
    root = tk.Tk()
    root.title("Главное окно")
    root.protocol('WM_DELETE_WINDOW', root.destroy)
    # Creates a toplevel widget.
    global _top1, _w1

    _top1 = root
    _w1 = lab3_interface.Toplevel1(_top1)
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
    lab3_interface.start_up()
