import cv2
import os
import io
import random as rnd
from PIL import Image, ImageTk

import sys
import tkinter as tk
import tkinter.ttk as ttk
from tkinter.constants import *

from tkinter import messagebox
from face_classification import *
import tkinter.filedialog as fd

import platform

import my_support2


class Toplevel1:
    def __init__(self, top=None):
        """This class configures and populates the toplevel window.
           top is the toplevel containing window."""
        self.outputPath = os.path.dirname(os.path.abspath(__file__)) + "/data"
        self.thread = None
        self.stopEvent = None
        self.s_filename = None
        self.data = None
        self.number_face_test = [10, 200]
        self.method = None

        self.methods = [get_histogram, get_dft, get_dct, get_gradient, get_scale]
        self.parameters = None
        self.size_train = None
        self.best_score = 0

        _bgcolor = '#d9d9d9'  # X11 color: 'gray85'
        _fgcolor = '#000000'  # X11 color: 'black'
        _compcolor = '#d9d9d9'  # X11 color: 'gray85'
        _ana1color = '#d9d9d9'  # X11 color: 'gray85'
        _ana2color = '#ececec'  # Closest X11 color: 'gray92'
        self.style = ttk.Style()
        if sys.platform == "win32":
            self.style.theme_use('winnative')
        self.style.configure('.', background=_bgcolor)
        self.style.configure('.', foreground=_fgcolor)
        self.style.configure('.', font="TkDefaultFont")
        self.style.map('.', background=[('selected', _compcolor), ('active', _ana2color)])

        top.geometry("1015x594+261+141")
        top.minsize(120, 1)
        top.maxsize(1540, 845)
        top.resizable(1, 1)
        top.title("Lab2.2")  # top.title("Toplevel 0")
        top.configure(background="#58b3e9")
        top.configure(highlightbackground="#4b61f5")
        top.configure(highlightcolor="black")

        self.root = top

        self.LabelName = tk.Label(self.root)
        self.LabelName.place(relx=0.039, rely=0.0, height=41, width=981)
        self.LabelName.configure(activebackground="#f9f9f9")
        self.LabelName.configure(activeforeground="black")
        self.LabelName.configure(anchor='w')
        self.LabelName.configure(background="#58b3e9")
        self.LabelName.configure(compound='center')
        self.LabelName.configure(disabledforeground="#a3a3a3")
        self.LabelName.configure(font="-family {Segoe UI Emoji} -size 19 -weight bold")
        self.LabelName.configure(foreground="#ffffff")
        self.LabelName.configure(highlightbackground="#d9d9d9")
        self.LabelName.configure(highlightcolor="black")
        self.LabelName.configure(text='''Voting Classification''')

        self.menubar = tk.Menu(top, font="TkMenuFont", bg=_bgcolor, fg=_fgcolor)
        top.configure(menu=self.menubar)

        self.frame_stats = tk.Frame(self.root)
        self.frame_stats.place(relx=0.355, rely=0.034, relheight=0.929, relwidth=0.628)
        self.frame_stats.configure(relief='groove')
        self.frame_stats.configure(borderwidth="2")
        self.frame_stats.configure(relief="groove")
        self.frame_stats.configure(background="#d9d9d9")
        self.frame_stats.configure(highlightbackground="#d9d9d9")
        self.frame_stats.configure(highlightcolor="black")

        self.stats = [tk.Label(self.frame_stats), tk.Label(self.frame_stats), tk.Label(self.frame_stats),
                      tk.Label(self.frame_stats)]
        for i in range(len(self.stats)):
            self.stats[i].grid(row=i, column=(i + 1), sticky='N', padx=10)

        self.loadDataButton = tk.Button(self.root)
        self.loadDataButton.place(relx=0.118, rely=0.219, height=24, width=127)
        self.loadDataButton.configure(activebackground="#ececec")
        self.loadDataButton.configure(activeforeground="#000000")
        self.loadDataButton.configure(background="#d9d9d9")
        self.loadDataButton.configure(command=self.load_data)
        self.loadDataButton.configure(compound='left')
        self.loadDataButton.configure(disabledforeground="#a3a3a3")
        self.loadDataButton.configure(foreground="#000000")
        self.loadDataButton.configure(highlightbackground="#d9d9d9")
        self.loadDataButton.configure(highlightcolor="black")
        self.loadDataButton.configure(pady="0")
        self.loadDataButton.configure(text='''Choose database''')

        self.loadFileButton = tk.Button(self.root)
        self.loadFileButton.place(relx=0.118, rely=0.3, height=24, width=127)
        self.loadFileButton.configure(activebackground="#ececec")
        self.loadFileButton.configure(activeforeground="#000000")
        self.loadFileButton.configure(background="#d9d9d9")
        self.loadFileButton.configure(command=self.choose_file)
        self.loadFileButton.configure(compound='left')
        self.loadFileButton.configure(disabledforeground="#a3a3a3")
        self.loadFileButton.configure(foreground="#000000")
        self.loadFileButton.configure(highlightbackground="#d9d9d9")
        self.loadFileButton.configure(highlightcolor="black")
        self.loadFileButton.configure(pady="0")
        self.loadFileButton.configure(text='''Choose file''')

        self.chooseData = ttk.Combobox(self.root, state='readonly', width=25,
                                       values=["ORL face database 64x64", "ORL face database 112x92"])
        self.chooseData.place(relx=0.049, rely=0.084, relheight=0.121, relwidth=0.258)

        self.classifButton1 = tk.Button(self.root)
        self.classifButton1.place(relx=0.138, rely=0.69, height=44, width=77)
        self.classifButton1.configure(activebackground="#4b61f5")
        self.classifButton1.configure(activeforeground="white")
        self.classifButton1.configure(activeforeground="#4b61f5")
        self.classifButton1.configure(background="#4b61f5")
        self.classifButton1.configure(command=self.computing)
        self.classifButton1.configure(compound='left')
        self.classifButton1.configure(disabledforeground="#a3a3a3")
        self.classifButton1.configure(foreground="#000000")
        self.classifButton1.configure(highlightbackground="#d9d9d9")
        self.classifButton1.configure(highlightcolor="black")
        self.classifButton1.configure(pady="0")
        self.classifButton1.configure(text='''START''')

        self.Frame2 = tk.Frame(self.root)
        self.Frame2.place(relx=0.02, rely=0.808, relheight=0.16, relwidth=0.31)
        self.Frame2.configure(relief='groove')
        self.Frame2.configure(borderwidth="2")
        self.Frame2.configure(relief="groove")
        self.Frame2.configure(background="#d9d9d9")

        self.TSeparator1 = ttk.Separator(self.Frame2)
        self.TSeparator1.place(relx=0.508, rely=0.0, relheight=0.958)
        self.TSeparator1.configure(orient="vertical")

        self.Label2 = tk.Label(self.Frame2)
        self.Label2.place(relx=0.127, rely=0.105, height=31, width=74)
        self.Label2.configure(anchor='w')
        self.Label2.configure(background="#d9d9d9")
        self.Label2.configure(compound='left')
        self.Label2.configure(disabledforeground="#a3a3a3")
        self.Label2.configure(font="-family {Segoe UI Emoji} -size 12")
        self.Label2.configure(foreground="#000000")
        self.Label2.configure(text='''Accuracy''')

        self.bestParameterVoiting = tk.Label(self.Frame2, font="Arial 10")
        self.bestParameterVoiting.place(relx=0.571, rely=0.526, relheight=0.358, relwidth=0.362)

        self.accuracyVoiting = tk.Label(self.Frame2, font="Arial 10")
        self.accuracyVoiting.place(relx=0.063, rely=0.526, relheight=0.358, relwidth=0.362)

        self.Label2_1 = tk.Label(self.Frame2)
        self.Label2_1.place(relx=0.571, rely=0.105, height=31, width=124)
        self.Label2_1.configure(activebackground="#f9f9f9")
        self.Label2_1.configure(activeforeground="black")
        self.Label2_1.configure(anchor='w')
        self.Label2_1.configure(background="#d9d9d9")
        self.Label2_1.configure(compound='left')
        self.Label2_1.configure(cursor="fleur")
        self.Label2_1.configure(disabledforeground="#a3a3a3")
        self.Label2_1.configure(font="-family {Segoe UI Emoji} -size 12")
        self.Label2_1.configure(foreground="#000000")
        self.Label2_1.configure(highlightbackground="#d9d9d9")
        self.Label2_1.configure(highlightcolor="black")
        self.Label2_1.configure(text='''Best parameter''')



        # lbl5 = tk.Label(self.frame_example, text="Classification example:")
        # lbl5.grid(row=0, column=0, padx=10, sticky='NW')
        #
        lbl6 = tk.Label(self.frame_stats, text="Original image:")
        lbl6.grid(row=0, column=1, padx=10, sticky='NW')

        # lbl7 = tk.Label(self.frame_example, text="histogram:")
        # lbl7.grid(row=0, column=2, padx=10, sticky='NW')
        #
        # lbl8 = tk.Label(self.frame_example, text="DFT:")
        # # lbl8.grid(row=0, column=3, padx=10, sticky='NW')
        #
        # lbl9 = tk.Label(self.frame_example, text="DCT:")
        # lbl9.grid(row=0, column=4, padx=10, sticky='NW')
        #
        # lbl10 = tk.Label(self.frame_example, text="gradient:")
        # lbl10.grid(row=0, column=5, padx=10, sticky='NW')
        #
        # lbl11 = tk.Label(self.frame_example, text="scale:")
        # lbl11.grid(row=0, column=6, padx=10, sticky='NW')
        #
        lbl12 = tk.Label(self.frame_stats, text="Another image from class:")
        lbl12.grid(row=0, column=2, padx=10, sticky='NW')

        self.images_1 = [tk.Label(self.frame_stats), tk.Label(self.frame_stats), tk.Label(self.frame_stats),
                         tk.Label(self.frame_stats),
                         tk.Label(self.frame_stats), tk.Label(self.frame_stats), tk.Label(self.frame_stats)]
        for i in range(len(self.images_1)):
            self.images_1[i].grid(row=1, column=i + 1, sticky='N', padx=10, pady=2)

    def choose_file(self):
        self.s_filename = fd.askopenfilename(title="Открыть файл", initialdir="/")

    def load_data(self):
        try:
            if self.chooseData.get() == "ORL face database 64x64":
                print("64x64")
                self.data = get_faces()
            if self.chooseData.get() == "ORL face database 112x92":
                self.data = read_faces_from_disk()
                print("112x92")
            self.loadDataButton.configure(text="Load completed")
        except Exception as e:
            print(e)
            self.loadDataButton.configure(text="Load failed")
            messagebox.showinfo("Attention", "Can't load database")

    def computing(self):
        if self.data is None:
            messagebox.showinfo("Attention", "Please, select database")
            return
        messagebox.showinfo("Attention", "Wait, while parameters will be computed")
        # self.parameters, self.size_train, self.best_score = cross_validation(self.data)
        self.parameters = {'get_histogram': 28, 'get_dft': 88, 'get_dct': 3, 'get_gradient': 2,
                           'get_scale': 0.15000000000000002}
        str = "["
        for method in self.methods:
            if method == get_scale:
                str += '{0:.2f}'.format(self.parameters[method.__name__])
            else:
                str += '{}'.format(self.parameters[method.__name__])
            str += "; "
        str = str[:-3]
        str += "]"
        self.size_train = 6
        self.best_score = 1
        self.bestParameterVoiting.configure(text=str)
        self.accuracyVoiting.configure(text="{0:.4f}".format(self.best_score))
        print(self.parameters)
        print(self.size_train)
        print(self.best_score)
        self.classif()

    def classif(self):
        if self.parameters is None or self.size_train is None:
            messagebox.showinfo("Attention", "Please, start training first")
            return

        self.data = read_faces_from_disk_2(self)

        for im in self.data:
            image = cv2.cvtColor(cv2.imread(im), cv2.COLOR_BGR2GRAY)
            x_train, x_test, y_train, y_test = split_data(self.data, self.size_train)
            x_test = []
            x_test.append(image / 255)
            messagebox.showinfo("Attention", "Wait, while classification will be computed")
            v = voting([x_train, y_train], x_test, self.parameters)
            example1 = x_test[0] * 255
            image = Image.fromarray(example1)
            image = ImageTk.PhotoImage(image)
            self.images_1[0].configure(image=image)
            self.images_1[0].image = image

            """histogram"""
            hist, bins = get_histogram(example1 / 255, self.parameters["get_histogram"])
            hist = np.insert(hist, 0, 0.0)
            # fig = plt.figure(figsize=(1.1, 1.1))
            # ax = fig.add_subplot(111)
            # ax.plot(bins, hist)
            # plt.xticks(color='w')
            # plt.yticks(color='w')
            # buf = io.BytesIO()
            # fig.savefig(buf)
            # buf.seek(0)
            # image = Image.open(buf)
            # image = ImageTk.PhotoImage(image)
            # self.images_1[1].configure(image=image)
            # self.images_1[1].image = image


            """dft"""
            # lll1 = tk.Label(self.frame_stats, text="DFT")
            # lll1.grid(row=0, column=1, padx=10)
            dft = get_dft(example1, self.parameters["get_dft"])
            # fig = plt.figure(figsize=(5, 5))
            # ax = fig.add_subplot(111)
            # ax.pcolormesh(range(dft.shape[0]),
            #               range(dft.shape[0]),
            #               np.flip(dft, 0), cmap="Greys")
            # """graphs here"""
            # plt.xticks(color='w')
            # plt.yticks(color='w')
            # buf = io.BytesIO()
            # fig.savefig(buf)
            # buf.seek(0)
            # image = Image.open(buf)
            # image = ImageTk.PhotoImage(image)
            # self.stats[0].configure(image=image)
            # self.stats[0].image = image

            """dct"""
            dct = get_dct(example1, self.parameters["get_dct"])
            # fig = plt.figure(figsize=(1.1, 1.1))
            # ax = fig.add_subplot(111)
            # ax.pcolormesh(range(dct.shape[0]),
            #               range(dct.shape[0]),
            #               np.flip(dct, 0), cmap="Greys")
            # plt.xticks(color='w')
            # plt.yticks(color='w')
            # buf = io.BytesIO()
            # fig.savefig(buf)
            # buf.seek(0)
            # image = Image.open(buf)
            # image = ImageTk.PhotoImage(image)
            # self.images_1[3].configure(image=image)
            # self.images_1[3].image = image

            """gradient"""
            hist = get_gradient(example1, self.parameters["get_gradient"])
            # fig = plt.figure(figsize=(1.1, 1.1))
            # ax = fig.add_subplot(111)
            # ax.plot(range(0, len(hist)), hist)
            # plt.xticks(color='w')
            # plt.yticks(color='w')
            # buf = io.BytesIO()
            # fig.savefig(buf)
            # buf.seek(0)
            # image = Image.open(buf)
            # image = ImageTk.PhotoImage(image)
            # self.images_1[4].configure(image=image)
            # self.images_1[4].image = image

            """scale"""
            image = Image.fromarray(cv2.resize(example1,
                                               (int(self.parameters["get_scale"] * example1.shape[0]),
                                                int(self.parameters["get_scale"] * example1.shape[1])),
                                               interpolation=cv2.INTER_AREA))
            # image = ImageTk.PhotoImage(image)
            # self.images_1[5].configure(image=image)
            # self.images_1[5].image = image

            image = Image.fromarray(self.data[0][10 * v[0]] * 255)
            image = ImageTk.PhotoImage(image)
            self.images_1[1].configure(image=image)
            self.images_1[1].image = image




# The following code is added to facilitate the Scrolled widgets you specified.
class AutoScroll(object):
    """Configure the scrollbars for a widget."""

    def __init__(self, master):
        #  Rozen. Added the try-except clauses so that this class
        #  could be used for scrolled entry widget for which vertical
        #  scrolling is not supported. 5/7/14.
        try:
            vsb = ttk.Scrollbar(master, orient='vertical', command=self.yview)
        except:
            pass
        hsb = ttk.Scrollbar(master, orient='horizontal', command=self.xview)
        try:
            self.configure(yscrollcommand=self._autoscroll(vsb))
        except:
            pass
        self.configure(xscrollcommand=self._autoscroll(hsb))
        self.grid(column=0, row=0, sticky='nsew')
        try:
            vsb.grid(column=1, row=0, sticky='ns')
        except:
            pass
        hsb.grid(column=0, row=1, sticky='ew')
        master.grid_columnconfigure(0, weight=1)
        master.grid_rowconfigure(0, weight=1)
        # Copy geometry methods of master  (taken from ScrolledText.py)
        methods = tk.Pack.__dict__.keys() | tk.Grid.__dict__.keys() | tk.Place.__dict__.keys()
        for meth in methods:
            if meth[0] != '_' and meth not in ('config', 'configure'):
                setattr(self, meth, getattr(master, meth))

    @staticmethod
    def _autoscroll(sbar):
        """Hide and show scrollbar as needed."""

        def wrapped(first, last):
            first, last = float(first), float(last)
            if first <= 0 and last >= 1:
                sbar.grid_remove()
            else:
                sbar.grid()
            sbar.set(first, last)

        return wrapped

    def __str__(self):
        return str(self.master)


def _create_container(func):
    """Creates a ttk Frame with a given master, and use this new frame to
    place the scrollbars and the widget."""

    def wrapped(cls, master, **kw):
        container = ttk.Frame(master)
        container.bind('<Enter>', lambda e: _bound_to_mousewheel(e, container))
        container.bind('<Leave>', lambda e: _unbound_to_mousewheel(e, container))
        return func(cls, container, **kw)

    return wrapped


class ScrolledListBox(AutoScroll, tk.Listbox):
    """A standard Tkinter Listbox widget with scrollbars that will
    automatically show/hide as needed."""

    @_create_container
    def __init__(self, master, **kw):
        tk.Listbox.__init__(self, master, **kw)
        AutoScroll.__init__(self, master)

    def size_(self):
        sz = tk.Listbox.size(self)
        return sz


def _bound_to_mousewheel(event, widget):
    child = widget.winfo_children()[0]
    if platform.system() == 'Windows' or platform.system() == 'Darwin':
        child.bind_all('<MouseWheel>', lambda e: _on_mousewheel(e, child))
        child.bind_all('<Shift-MouseWheel>', lambda e: _on_shiftmouse(e, child))
    else:
        child.bind_all('<Button-4>', lambda e: _on_mousewheel(e, child))
        child.bind_all('<Button-5>', lambda e: _on_mousewheel(e, child))
        child.bind_all('<Shift-Button-4>', lambda e: _on_shiftmouse(e, child))
        child.bind_all('<Shift-Button-5>', lambda e: _on_shiftmouse(e, child))


def _unbound_to_mousewheel(event, widget):
    if platform.system() == 'Windows' or platform.system() == 'Darwin':
        widget.unbind_all('<MouseWheel>')
        widget.unbind_all('<Shift-MouseWheel>')
    else:
        widget.unbind_all('<Button-4>')
        widget.unbind_all('<Button-5>')
        widget.unbind_all('<Shift-Button-4>')
        widget.unbind_all('<Shift-Button-5>')


def _on_mousewheel(event, widget):
    if platform.system() == 'Windows':
        widget.yview_scroll(-1 * int(event.delta / 120), 'units')
    elif platform.system() == 'Darwin':
        widget.yview_scroll(-1 * int(event.delta), 'units')
    else:
        if event.num == 4:
            widget.yview_scroll(-1, 'units')
        elif event.num == 5:
            widget.yview_scroll(1, 'units')


def _on_shiftmouse(event, widget):
    if platform.system() == 'Windows':
        widget.xview_scroll(-1 * int(event.delta / 120), 'units')
    elif platform.system() == 'Darwin':
        widget.xview_scroll(-1 * int(event.delta), 'units')
    else:
        if event.num == 4:
            widget.xview_scroll(-1, 'units')
        elif event.num == 5:
            widget.xview_scroll(1, 'units')


def start_up():
    my_support2.main()


if __name__ == '__main__':
    my_support2.main()
