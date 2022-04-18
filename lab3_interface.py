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
import tkinter.filedialog as fd

import platform

import my_support3
from Filters import *



class Toplevel1:
    def __init__(self, top=None):
        """This class configures and populates the toplevel window.
           top is the toplevel containing window."""

        self.outputPath = os.path.dirname(os.path.abspath(__file__)) + "/база уменьшенная"
        self.thread = None
        self.stopEvent = None
        self.s_filename = None
        self.data = None
        # self.number_face_test = [10, 200]
        self.method = None
        self.methods = [Euler, sobel, Laplace, DOG, hough, gabor]
        self.parameters = None
        self.size_train = None
        self.best_score = 0
        self.authors = {0: "Шишкин", 1: "Дали",
                        2: "Клод Моне", 3: "Пикассо", 4: "Айвазовский"}

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
        top.title("Lab3")  # top.title("Toplevel 0")
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
        self.LabelName.configure(text='''Authors Classification''')

        self.menubar = tk.Menu(top, font="TkMenuFont", bg=_bgcolor, fg=_fgcolor)
        top.configure(menu=self.menubar)

        self.frame_stats = tk.Frame(self.root)
        self.frame_stats.place(relx=0.355, rely=0.034, relheight=0.929, relwidth=0.628)
        self.frame_stats.configure(relief='groove')
        self.frame_stats.configure(borderwidth="2")
        self.frame_stats.configure(relief="groove")
        self.frame_stats.configure(background="#d9d9d9")
        self.frame_stats.configure(highlightbackground="#d9d9d9")
        self.frame_stats.configure(highlightcolor="orange")

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

        # self.chooseData = ttk.Combobox(self.root, state='readonly', width=25,
        #                                values=["Artists"])
        # self.chooseData.place(relx=0.049, rely=0.084, relheight=0.121, relwidth=0.258)


        # self.Label1 = tk.Label(self.root)
        # self.Label1.place(relx=0.049, rely=0.269, height=28, width=267)
        # self.Label1.configure(activebackground="#f9f9f9")
        # self.Label1.configure(activeforeground="#35c0d9")
        # self.Label1.configure(anchor='w')
        # self.Label1.configure(background="#58b3e9")
        # self.Label1.configure(compound='left')
        # self.Label1.configure(disabledforeground="#a3a3a3")
        # self.Label1.configure(font="-family {Segoe UI Emoji} -size 12")
        # self.Label1.configure(foreground="#000000")
        # self.Label1.configure(highlightbackground="#d9d9d9")
        # self.Label1.configure(highlightcolor="black")
        # self.Label1.configure(text='''Choose method''')

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

        lbl6 = tk.Label(self.frame_stats, text="Original image:")
        lbl6.grid(row=0, column=1, padx=10, sticky='NW')

        lbl12 = tk.Label(self.frame_stats, text="")
        lbl12.grid(row=0, column=2, padx=10, sticky='NW')

        self.images_1 = [tk.Label(self.frame_stats), tk.Label(self.frame_stats),
                         tk.Label(self.frame_stats), tk.Label(self.frame_stats), tk.Label(self.frame_stats),
                         tk.Label(self.frame_stats), tk.Label(self.frame_stats), tk.Label(self.frame_stats)]

        self.images_1[0].grid(row=1, column=1, sticky='N', padx=10, pady=2)
        for i in range(1, 4):
            self.images_1[i].grid(row=2, column=i + 1, sticky='N', padx=10, pady=2)
        for i in range(4, len(self.images_1)):
            self.images_1[i].grid(row=3, column=i - 4 + 1 + 1, sticky='N', padx=10, pady=2)
        self.images_2 = [tk.Label(self.frame_stats), tk.Label(self.frame_stats), tk.Label(self.frame_stats),
                         tk.Label(self.frame_stats), tk.Label(self.frame_stats), tk.Label(self.frame_stats)]

        for i in range(0, 3):
            self.images_2[i].grid(row=4, column=i + 2, sticky='N', padx=10, pady=2)
        for i in range(3, len(self.images_2)):
            self.images_2[i].grid(row=5, column=i - 3 + 2, sticky='N', padx=10, pady=2)

    def choose_file(self):
        self.s_filename = fd.askopenfilename(title="Открыть файл", initialdir="Artists")

    def read_faces_from_disk(self):
        data_faces = []
        data_target = []
        # data_folder = os.path.dirname(os.path.abspath(__file__)) + "\\faces\s"
        data_folder = r".\Artists\s"
        for i in range(1, 6):
            for j in range(1, 11):
                # image = cv2.cvtColor(cv2.imread(data_folder + str(i) + "\\" + str(j) + ".pgm"), cv2.COLOR_BGR2GRAY)
                image = cv2.imread(data_folder + str(i) + "\\" + str(j) + ".jpg")
                data_faces.append(image)
                data_target.append(i - 1)
        return [data_faces, data_target]

    def load_data(self):
        try:
            print("Artisits")
            self.data = self.read_faces_from_disk()
            messagebox.showinfo("Info", "Load is completed")
        except Exception as e:
            print(e)
            self.loadDataButton.configure(text="Load failed")
            messagebox.showinfo("Attention", "Can't load database")

    def computing(self):
        if self.data is None:
            messagebox.showinfo("Attention", "Please, select database")
            return
        # messagebox.showinfo("Attention", "Wait, while parameters will be computed")
        # self.parameters, self.size_train, self.best_score = cross_validation(self.data)
        self.size_train = 6
        self.classif()



    def classif(self):
        input_image = cv2.imread(self.s_filename)
        x_train, x_test, y_train, y_test = split_data(self.data, self.size_train)
        messagebox.showinfo("Attention", "Wait, while classification will be computed")
        vote_answer, methods_answer = voting([x_train, y_train], [input_image])

        image = Image.fromarray(cv2.cvtColor(input_image, cv2.COLOR_BGR2RGB))

        image = ImageTk.PhotoImage(image)
        self.images_1[0].configure(image=image)
        self.images_1[0].image = image

        for i in range(len(self.methods)):
            fig = plt.figure(figsize=(1.1, 1.1))
            ax = fig.add_subplot(111)
            ax.text(0, 0.5,
                    f'{self.methods[i].__name__}' + ':\n\n' + self.authors[methods_answer[self.methods[i].__name__][0]],
                    transform=plt.gca().transAxes, fontdict={'size': 10})
            # ax.title(f'{self.methods[i].__name__}')  # , title=f'{self.methods[i].__name__}'
            plt.axis("off")
            buf = io.BytesIO()
            fig.savefig(buf)
            buf.seek(0)
            image = Image.open(buf)
            image = ImageTk.PhotoImage(image)
            self.images_1[i + 1].configure(image=image)
            self.images_1[i + 1].image = image
        # vote res
        fig = plt.figure(figsize=(1.1, 1.1))
        ax = fig.add_subplot(111)
        ax.text(0, 0.5,
                'Voting' + ':\n\n' + self.authors[vote_answer[0]],
                transform=plt.gca().transAxes, fontdict={'size': 10})
        plt.axis("off")
        buf = io.BytesIO()
        fig.savefig(buf)
        buf.seek(0)
        image = Image.open(buf)
        image = ImageTk.PhotoImage(image)
        self.images_1[7].configure(image=image)
        self.images_1[7].image = image

        for i, method in enumerate(self.methods):
            print(i)
            to_draw = method(input_image)[1]
            fig = plt.figure(figsize=(1.1, 1.1))
            ax = fig.add_subplot(111)
            if method == Euler:
                ax.text(0, 0.5,
                        str(method.__name__) + '\n\n' + str(to_draw),
                        transform=plt.gca().transAxes, fontdict={'size': 10})
                # ax.set(title=str(method.__name__))
            elif len(to_draw.shape) == 2:
                ax.imshow(to_draw, cmap="gray")
            else:
                ax.imshow(cv2.cvtColor(to_draw, cv2.COLOR_BGR2RGB))

            plt.axis("off")
            if method != Euler:
                ax.set(title=str(method.__name__))
            buf = io.BytesIO()
            fig.savefig(buf)
            buf.seek(0)
            image = Image.open(buf)
            image = ImageTk.PhotoImage(image)
            self.images_2[i].configure(image=image)
            self.images_2[i].image = image

        """Graphs"""
        """Vote"""
        # count = 0
        # summ = 0
        # result = []
        # for test_image, true_answer in zip(x_test, y_test):
        #     res, methods_answer = voting([x_train, y_train], [test_image])
        #     # res = classifier(train, test, color_hist)
        #     if true_answer == res[0]:
        #         summ += 1
        #     else:
        #         print(f"return {self.authors[res[0]]} but true is {self.authors[true_answer]}")
        #         # res = {}
        #         # for method in get_methods():
        #         #     answers = classifier(train, [[test_image], [true_answer]], method)
        #         #     print(f"method {method.name} found {classes[answers[0]]}")
        #         # print(test_methods(train, [[test_image], [true_answer]]))
        #         # plt.imshow(cv2.cvtColor(test_image, cv2.COLOR_BGR2RGB)), plt.axis("off")
        #         # plt.show()
        #     count += 1
        #     result.append(summ / count)
        #     print(f"{count} images --> {summ / count}")
        # plt.plot(range(1, len(result) + 1), result), plt.xlabel("amount of test images"), plt.ylabel(
        #     "score"), plt.title("Voting")
        # plt.show()

        # stats = {}
        # for size in range(1, 10):
        #     x_train, x_test, y_train, y_test = split_data(self.data, size)
        #     train = [x_train, y_train]
        #     test = [x_test, y_test]
        #     res = test_methods(train, test)
        #     classf = test_voting(train, test)
        #     for method in [Euler, sobel, Laplace, DOG, hough, gabor]:
        #         if method.__name__ in stats:
        #             stats[method.__name__].append(res[method.__name__])
        #         else:
        #             stats[method.__name__] = [res[method.__name__]]
        #     if "voting" in stats:
        #         stats["voting"].append(classf)
        #     else:
        #         stats["voting"] = [classf]
        #     # if classf >= 0.6:
        # for method, stat in stats.items():
        #     plt.plot(range(1, len(stat) + 1), stat, label=method)
        # plt.title(f"score=score(train_size)"), plt.legend(loc='best'), plt.xlabel("train_size"), plt.ylabel("score")
        # plt.show()


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
    my_support3.main()


if __name__ == '__main__':
    my_support3.main()
