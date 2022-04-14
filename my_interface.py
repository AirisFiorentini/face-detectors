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

import my_support


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
        top.title("Lab2")  # top.title("Toplevel 0")
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
        self.LabelName.configure(text='''Separate Classification''')

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
        self.loadDataButton.configure(text='''Load Chosen''')

        self.chooseData = ttk.Combobox(self.root, state='readonly', width=25,
                                       values=["ORL face database 64x64", "ORL face database 112x92"])
        self.chooseData.place(relx=0.049, rely=0.084, relheight=0.121, relwidth=0.258)

        self.chosenMethod = ttk.Combobox(self.root, state='readonly', width=25,
                                         values=["histogram", "dft", "dct", "scale", "gradient"])
        self.chosenMethod.place(relx=0.049, rely=0.32, relheight=0.121, relwidth=0.258)

        self.Label1 = tk.Label(self.root)
        self.Label1.place(relx=0.049, rely=0.269, height=28, width=267)
        self.Label1.configure(activebackground="#f9f9f9")
        self.Label1.configure(activeforeground="#35c0d9")
        self.Label1.configure(anchor='w')
        self.Label1.configure(background="#58b3e9")
        self.Label1.configure(compound='left')
        self.Label1.configure(disabledforeground="#a3a3a3")
        self.Label1.configure(font="-family {Segoe UI Emoji} -size 12")
        self.Label1.configure(foreground="#000000")
        self.Label1.configure(highlightbackground="#d9d9d9")
        self.Label1.configure(highlightcolor="black")
        self.Label1.configure(text='''Choose method''')

        self.Label1_1 = tk.Label(self.root)
        self.Label1_1.place(relx=0.049, rely=0.471, height=28, width=267)
        self.Label1_1.configure(activebackground="#f9f9f9")
        self.Label1_1.configure(activeforeground="#35c0d9")
        self.Label1_1.configure(anchor='w')
        self.Label1_1.configure(background="#58b3e9")
        self.Label1_1.configure(compound='left')
        self.Label1_1.configure(disabledforeground="#a3a3a3")
        self.Label1_1.configure(font="-family {Segoe UI Emoji} -size 12")
        self.Label1_1.configure(foreground="#000000")
        self.Label1_1.configure(highlightbackground="#d9d9d9")
        self.Label1_1.configure(highlightcolor="black")
        self.Label1_1.configure(text='''Choose test data''')

        self.chooseClassification = ttk.Combobox(self.root, state='readonly', width=25,
                                                 values=["Training sample", "Not training sample", "Cross-validation", "Graph"])
        self.chooseClassification.place(relx=0.049, rely=0.539, relheight=0.121
                                        , relwidth=0.258)

        self.classifButton1 = tk.Button(self.root)
        self.classifButton1.place(relx=0.138, rely=0.69, height=44, width=77)
        self.classifButton1.configure(activebackground="#4b61f5")
        self.classifButton1.configure(activeforeground="white")
        self.classifButton1.configure(activeforeground="#4b61f5")
        self.classifButton1.configure(background="#4b61f5")
        self.classifButton1.configure(command=self.start_comp)
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

        self.accuracy = tk.Label(self.Frame2, font="Arial 10")
        self.accuracy.place(relx=0.063, rely=0.526, relheight=0.358, relwidth=0.362)

        self.bestParameter = tk.Label(self.Frame2, font="Arial 10")
        self.bestParameter.place(relx=0.571, rely=0.526, relheight=0.358
                                 , relwidth=0.362)

        self.Label2 = tk.Label(self.Frame2)
        self.Label2.place(relx=0.127, rely=0.105, height=31, width=74)
        self.Label2.configure(anchor='w')
        self.Label2.configure(background="#d9d9d9")
        self.Label2.configure(compound='left')
        self.Label2.configure(disabledforeground="#a3a3a3")
        self.Label2.configure(font="-family {Segoe UI Emoji} -size 12")
        self.Label2.configure(foreground="#000000")
        self.Label2.configure(text='''Accuracy''')

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

    def set_feature(self):
        try:
            if self.chosenMethod.get() == "histogram":
                self.method = get_histogram
            if self.chosenMethod.get() == "dft":
                self.method = get_dft
            if self.chosenMethod.get() == "dct":
                self.method = get_dct
            if self.chosenMethod.get() == "scale":
                self.method = get_scale
            if self.chosenMethod.get() == "gradient":
                self.method = get_gradient
        except Exception:
            messagebox.showinfo("Attention", "Please, select method")
            return

    def start_comp(self):
        if self.chooseClassification.get() == "Training sample":
            self.start_computing_1()
        elif self.chooseClassification.get() == "Not training sample":
            self.start_computing_2()
        elif self.chooseClassification.get() == "Cross-validation":
            self.start_computing_3()
        elif self.chooseClassification.get() == "Graph":
            self.draw_special_graph()
        else:
            messagebox.showinfo("Attention", "Please, select any sample")
            return

    def start_computing_1(self):
        if self.method is None:
            self.set_feature()
        result = teach_parameter(self.data, choose_n_from_data(self.data, 3), self.method)
        self.bestParameter.configure(text=str(result[0][0]))
        self.accuracy.configure(text=str(result[0][1]))
        # ГРАФИК ПО RESULT[1] (RESULT[1][0] B RESULT[1][1])
        plt.rcParams["font.size"] = "7"
        fig = plt.figure(figsize=(4.5, 3.5))
        ax = fig.add_subplot(111)
        ax.plot(result[1][0], result[1][1])
        # fig.title("Зависимость точности от параметра метода")
        ax.set(xlabel='Параметр метода',
               ylabel='Точность',
               title='Зависимость точности от параметра метода на обучающей выборке')
        # ax = plt.set
        buf = io.BytesIO()
        fig.savefig(buf)
        buf.seek(0)
        image = Image.open(buf)
        image = ImageTk.PhotoImage(image)
        self.stats[0].configure(image=image)
        self.stats[0].image = image

    def start_computing_2(self):
        if self.method is None:
            self.set_feature()
        new_data = split_data3(self.data, images_per_person_in_train=3)
        result = teach_parameter([new_data[0], new_data[2]], [new_data[1], new_data[3]], self.method)
        print(result)
        self.bestParameter.configure(text=str(result[0][0]))
        self.accuracy.configure(text=str(result[0][1]))
        # ГРАФИК ПО RESULT[1] (RESULT[1][0] B RESULT[1][1])
        plt.rcParams["font.size"] = "7"
        fig = plt.figure(figsize=(5, 4))
        ax = fig.add_subplot(111)
        ax.plot(result[1][0], result[1][1])
        ax.set(xlabel='Параметр метода',
               ylabel='Точность',
               title='Зависимость точности от параметра метода на тестовой выборке')
        buf = io.BytesIO()
        fig.savefig(buf)
        buf.seek(0)
        image = Image.open(buf)
        image = ImageTk.PhotoImage(image)
        self.stats[0].configure(image=image)
        self.stats[0].image = image

    def start_computing_3(self):
        if self.data is None:
            messagebox.showinfo("Attention", "Please, select database")
            return
        try:
            self.number_face_test = [10, 200]
        except Exception:
            messagebox.showinfo("Attention", "Please, input integer numbers in range [10, 200]")
            return

        lll1 = tk.Label(self.frame_stats, font="Arial 10")  # text="3 Folds",
        lll1.grid(row=0, column=1, padx=10)
        lll2 = tk.Label(self.frame_stats, font="Arial 10")  # text="5 Folds",
        lll2.grid(row=0, column=2, padx=10)
        lll4 = tk.Label(self.frame_stats, font="Arial 10")  # text="Best parameter and\ndifferent test sizes",
        lll4.grid(row=0, column=3, padx=10)

        if self.number_face_test[0] < 10:
            self.number_face_test[0] = 10
        if self.number_face_test[1] > 200:
            self.number_face_test[1] = 200
        if self.method is None:
            self.set_feature()
        results = [0, 0, 0]
        x_train, x_test, y_train, y_test = split_data3(self.data, images_per_person_in_test=5)
        train = mesh_data([x_train, y_train])
        test = mesh_data([x_test, y_test])
        print(self.method)
        count = 0
        for f in [3, 5]:  # ДОБАВИТЬ 5
            print(f)
            res = cross_validation3(self.data, self.method, folds=f)
            if res[0][1] > results[1]:
                results = [res[0][0], res[0][1], f]
            plt.rcParams["font.size"] = "7"
            fig = plt.figure(figsize=(4.3, 3.5))
            """gr"""
            ax = fig.add_subplot(111)
            ax.plot(res[1][0], res[1][1])  # статистика
            ax.set(xlabel='Параметр метода',
                   ylabel='Точность',
                   title=f'{f}' + ' folds')
            buf = io.BytesIO()
            fig.savefig(buf)
            plt.subplot(121)
            buf.seek(0)
            image = Image.open(buf)
            image = ImageTk.PhotoImage(image)
            self.stats[count].configure(image=image)
            self.stats[count].image = image
            count += 1
        # self.label_now_method.configure(text = str(self.method.__name__[4:]))
        self.bestParameter.configure(text=str(results[0]))
        self.accuracy.configure(text=str(results[1]))
        # self.bestFold.configure(text=str(results[2]))

        # sizes = range(int(self.number_face_test[0]), int(self.number_face_test[1]), 10)
        # test_results = [sizes, []]
        # for size in sizes:
        #     test_results[1].append(test_classifier(train, choose_n_from_data(test, size), self.method, results[0]))
        # plt.rcParams["font.size"] = "7"
        # fig = plt.figure(figsize=(4, 3.5))
        # ax.plot(test_results[0], test_results[1])
        # ax.set(xlabel='Размер тестовой выборки',
        #        ylabel='Точность',
        #        title='Зависимость точности от размера тестовой выборки')
        # buf = io.BytesIO()
        # fig.savefig(buf)
        # buf.seek(0)
        # image = Image.open(buf)
        # image = ImageTk.PhotoImage(image)
        # self.stats[count].configure(image=image)
        # self.stats[count].image = image


    def draw_special_graph(self):
        if self.method is None:
            self.set_feature()
        x_train0, x_test0, y_train0, y_test0 = split_data3(self.data, images_per_person_in_train=1, images_per_person_in_test=9)
        x_train1, x_test1, y_train1, y_test1 = split_data3(self.data, images_per_person_in_train=2, images_per_person_in_test=8)
        x_train2, x_test2, y_train2, y_test2 = split_data3(self.data, images_per_person_in_train=3, images_per_person_in_test=7)
        x_train3, x_test3, y_train3, y_test3 = split_data3(self.data, images_per_person_in_train=4, images_per_person_in_test=6)
        x_train4, x_test4, y_train4, y_test4 = split_data3(self.data, images_per_person_in_train=5, images_per_person_in_test=5)
        x_train5, x_test5, y_train5, y_test5 = split_data3(self.data, images_per_person_in_train=6, images_per_person_in_test=4)
        x_train6, x_test6, y_train6, y_test6 = split_data3(self.data, images_per_person_in_train=7, images_per_person_in_test=3)
        x_train7, x_test7, y_train7, y_test7 = split_data3(self.data, images_per_person_in_train=8, images_per_person_in_test=2)
        x_train8, x_test8, y_train8, y_test8 = split_data3(self.data, images_per_person_in_train=9, images_per_person_in_test=1)
        trains = [[x_train0, y_train0], [x_train1, y_train1], [x_train2, y_train2], [x_train3, y_train3],
                  [x_train4, y_train4], [x_train5, y_train5], [x_train6, y_train6], [x_train7, y_train7],
                  [x_train8, y_train8]]
        tests = [[x_test0, y_test0], [x_test1, y_test1], [x_test2, y_test2], [x_test3, y_test3],
                  [x_test4, y_test4], [x_test5, y_test5], [x_test6, y_test6], [x_test7, y_test7],
                  [x_test8, y_test8]]
        self.parameters = {'get_histogram': 28, 'get_dft': 88, 'get_dct': 3, 'get_gradient': 2, 'get_scale': 0.15000000000000002}
        # parameters = {'get_histogram': 28, 'get_dft': 88, 'get_dct': 3, 'get_gradient': 2,
        #               'get_scale': 0.15000000000000002}
        sizes = range(0, 9, 1)

        #for method in self.methods:
        test_results = [sizes, []]
        for size in sizes:
            test_results[1].append(test_classifier(trains[size],
                                                   tests[size],
                                                   self.method,
                                                   self.parameters[self.method.__name__]))  #

        plt.rcParams["font.size"] = "7"
        fig = plt.figure(figsize=(4, 3.5))
        ax = fig.add_subplot(111)
        test_results[0] = range(0, 360, 40)
        ax.plot(test_results[0], test_results[1])

        ax.set(xlabel='Размер обучающей выборки',
               ylabel='Точность',
               title='Зависимость точности от размера обучающей выборки')
        buf = io.BytesIO()
        fig.savefig(buf)
        buf.seek(0)
        image = Image.open(buf)
        image = ImageTk.PhotoImage(image)
        self.stats[0].configure(image=image)
        self.stats[0].image = image


        # 2 on test data
        x_train, x_test, y_train, y_test = split_data3(self.data, images_per_person_in_test=5)
        train = mesh_data([x_train, y_train])
        test = mesh_data([x_test, y_test])
        parameters = {'get_histogram': 28, 'get_dft': 88, 'get_dct': 3, 'get_gradient': 2,
                      'get_scale': 0.15000000000000002}
        sizes = range(int(self.number_face_test[0]), int(self.number_face_test[1]), 10)
        test_results = [sizes, []]
        for size in sizes:
            test_results[1].append(test_classifier(train, choose_n_from_data(test, size), self.method,
                                                   parameters[str(self.method.__name__)]))
        # print(parameters[str(self.method.__name__)])
        plt.rcParams["font.size"] = "7"
        fig = plt.figure(figsize=(4.5, 3.5))
        ax = fig.add_subplot(111)
        ax.plot(test_results[0], test_results[1])
        print(test_results[0], test_results[1])
        ax.set(xlabel='Размер тестовой выборки',
               ylabel='Точность',
               title='Зависимость точности от размера тестовой выборки')
        buf = io.BytesIO()
        fig.savefig(buf)
        buf.seek(0)
        image = Image.open(buf)
        image = ImageTk.PhotoImage(image)
        self.stats[1].configure(image=image)  # count
        self.stats[1].image = image

    def computing(self):
        if self.data is None:
            messagebox.showinfo("Attention", "Please, select database")
            return
        messagebox.showinfo("Attention", "Wait, while parameters will be computed")
        # self.parameters, self.size_train, self.best_score = cross_validation(self.data)
        self.parameters = {'get_histogram': 28, 'get_dft': 88, 'get_dct': 3, 'get_gradient': 2,
                           'get_scale': 0.15000000000000002}
        str = "[ "
        for method in self.methods:
            if method == get_scale:
                str += '{0:.2f}'.format(self.parameters[method.__name__])
            else:
                str += '{}'.format(self.parameters[method.__name__])
            str += ";  "
        str = str[:-3]
        str += " ]"
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

        image = cv2.cvtColor(cv2.imread(self.s_filename), cv2.COLOR_BGR2GRAY)
        x_train, x_test, y_train, y_test = split_data(self.data, self.size_train)
        x_test = []
        x_test.append(image / 255)
        messagebox.showinfo("Attention", "Wait, while classification will be computed")
        v = voting([x_train, y_train], x_test, self.parameters)

        example1 = x_test[0] * 255

        print(v[0])

        image = Image.fromarray(example1)
        image = ImageTk.PhotoImage(image)
        self.images_1[0].configure(image=image)
        self.images_1[0].image = image

        """graphs here"""
        hist, bins = get_histogram(example1 / 255, self.parameters["get_histogram"])
        hist = np.insert(hist, 0, 0.0)
        fig = plt.figure(figsize=(1.1, 1.1))
        ax = fig.add_subplot(111)
        ax.plot(bins, hist)
        plt.xticks(color='w')
        plt.yticks(color='w')
        buf = io.BytesIO()
        fig.savefig(buf)
        buf.seek(0)
        image = Image.open(buf)
        image = ImageTk.PhotoImage(image)
        self.images_1[1].configure(image=image)
        self.images_1[1].image = image

        lll1 = tk.Label(self.frame_stats, text="DFT")
        lll1.grid(row=0, column=1, padx=10)
        dft = get_dft(example1, self.parameters["get_dft"])
        fig = plt.figure(figsize=(5, 5))
        ax = fig.add_subplot(111)
        ax.pcolormesh(range(dft.shape[0]),
                      range(dft.shape[0]),
                      np.flip(dft, 0), cmap="Greys")
        """graphs here"""
        plt.xticks(color='w')
        plt.yticks(color='w')
        buf = io.BytesIO()
        fig.savefig(buf)
        buf.seek(0)
        image = Image.open(buf)
        image = ImageTk.PhotoImage(image)
        self.stats[0].configure(image=image)
        self.stats[0].image = image

        dct = get_dct(example1, self.parameters["get_dct"])
        fig = plt.figure(figsize=(1.1, 1.1))
        ax = fig.add_subplot(111)
        ax.pcolormesh(range(dct.shape[0]),
                      range(dct.shape[0]),
                      np.flip(dct, 0), cmap="Greys")
        plt.xticks(color='w')
        plt.yticks(color='w')
        buf = io.BytesIO()
        fig.savefig(buf)
        buf.seek(0)
        image = Image.open(buf)
        image = ImageTk.PhotoImage(image)
        self.images_1[3].configure(image=image)
        self.images_1[3].image = image

        hist = get_gradient(example1, self.parameters["get_gradient"])
        fig = plt.figure(figsize=(1.1, 1.1))
        ax = fig.add_subplot(111)
        ax.plot(range(0, len(hist)), hist)
        plt.xticks(color='w')
        plt.yticks(color='w')
        buf = io.BytesIO()
        fig.savefig(buf)
        buf.seek(0)
        image = Image.open(buf)
        image = ImageTk.PhotoImage(image)
        self.images_1[4].configure(image=image)
        self.images_1[4].image = image

        image = Image.fromarray(cv2.resize(example1,
                                           (int(self.parameters["get_scale"] * example1.shape[0]),
                                            int(self.parameters["get_scale"] * example1.shape[1])),
                                           interpolation=cv2.INTER_AREA))
        image = ImageTk.PhotoImage(image)
        self.images_1[5].configure(image=image)
        self.images_1[5].image = image

        image = Image.fromarray(self.data[0][10 * v[0]] * 255)
        image = ImageTk.PhotoImage(image)
        self.images_1[6].configure(image=image)
        self.images_1[6].image = image


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


#import platform


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
    my_support.main()


if __name__ == '__main__':
    my_support.main()
