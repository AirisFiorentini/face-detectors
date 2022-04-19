import cv2
import os
import io
import random as rnd
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from face_classification import *
import tkinter.filedialog as fd


class PhotoBoothApp:
    def __init__(self):
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

        self.root = tk.Tk()
        self.root.geometry("1200x700")

        self.loadDataLabel = tk.Label(self.root, text="Load Data", font="Arial 14")
        self.loadDataLabel.place(x=5, y=5)

        self.chooseData = ttk.Combobox(self.root, state='readonly', width=25,
                                       values=["ORL face database 64x64", "ORL face database 112x92"])
        self.chooseData.place(x=25, y=35)

        self.loadDataButton = tk.Button(self.root, text="Load data", command=self.load_data)
        self.loadDataButton.place(x=220, y=32)

        self.loadDataCompleteLabel = tk.Label(self.root, font="Arial 9")
        self.loadDataCompleteLabel.place(x=290, y=34)

        self.classificationLabel = tk.Label(self.root, text="Classification", font="Arial 14")
        self.classificationLabel.place(x=5, y=70)
        self.clbl = tk.Label(self.root, text="Choose test data", font="Arial 10")
        self.clbl.place(x=25, y=100)
        self.chooseClassification = ttk.Combobox(self.root, state='readonly', width=25,
                                                 values=["Training sample", "Not training sample", "Cross-validation"])
        self.chooseClassification.place(x=25, y=120)
        self.clbl = tk.Label(text="Choose method", font="Arial 10")
        self.clbl.place(x=25, y=150)
        self.choosenMethod = ttk.Combobox(self.root, state='readonly', width=25,
                                          values=["histogram", "dft", "dct", "scale", "gradient"])
        self.choosenMethod.place(x=25, y=170)
        self.clbl = tk.Label(self.root, text="Enter number of test faces", font="Arial 10")
        self.clbl.place(x=220, y=100)
        self.lowEntry = tk.Entry(self.root, width=25)
        self.lowEntry.place(x=220, y=120)
        self.highEntry = tk.Entry(self.root, width=25)
        self.highEntry.place(x=220, y=170)

        self.classifButton1 = tk.Button(self.root, text="Start", width=8, command=self.start_comp)
        self.classifButton1.place(x=25, y=200)

        self.accuracyLabel = tk.Label(self.root, text="Accuracy", font="Arial 12")
        self.accuracyLabel.place(x=5, y=250)
        self.accuracy = tk.Label(self.root, font="Arial 10")
        self.accuracy.place(x=5, y=280)

        self.parameterLabel = tk.Label(self.root, text="Best parameter", font="Arial 12")
        self.parameterLabel.place(x=200, y=250)
        self.bestParameter = tk.Label(self.root, font="Arial 10")
        self.bestParameter.place(x=200, y=280)

        self.frame_stats = tk.Frame(self.root, width=1000)
        self.frame_stats.place(x=400, y=5)
        self.stats = [tk.Label(self.frame_stats), tk.Label(self.frame_stats), tk.Label(self.frame_stats),
                      tk.Label(self.frame_stats)]
        for i in range(len(self.stats)):
            self.stats[i].grid(row=1, column=i + 1, sticky='N', padx=10)

        self.classificationLabel = tk.Label(self.root, text="Classification with voiting", font="Arial 14")
        self.classificationLabel.place(x=5, y=350)
        self.btn_file = tk.Button(self.root, text="Выбрать файл", command=self.choose_file)
        self.btn_file.place(x=25, y=400)
        self.voitingButton = tk.Button(self.root, text="Start", width=8, command=self.computing)
        self.voitingButton.place(x=220, y=400)

        self.accuracyLabel = tk.Label(self.root, text="Accuracy", font="Arial 12")
        self.accuracyLabel.place(x=5, y=450)
        self.accuracyVoiting = tk.Label(self.root, font="Arial 10")
        self.accuracyVoiting.place(x=5, y=480)

        self.parameterLabel = tk.Label(self.root, text="Best parameter", font="Arial 12")
        self.parameterLabel.place(x=200, y=450)
        self.bestParameterVoiting = tk.Label(self.root, font="Arial 10")
        self.bestParameterVoiting.place(x=200, y=480)

        self.frame_example = tk.Frame(self.root, height=600)
        self.frame_example.place(x=0, y=550)

        # lbl5 = tk.Label(self.frame_example, text="Classification example:")
        # lbl5.grid(row=0, column=0, padx=10, sticky='NW')

        lbl6 = tk.Label(self.frame_example, text="Original image:")
        lbl6.grid(row=0, column=1, padx=10, sticky='NW')

        # lbl7 = tk.Label(self.frame_example, text="histogram:")
        # lbl7.grid(row=0, column=2, padx=10, sticky='NW')

        # lbl8 = tk.Label(self.frame_example, text="DFT:")
        # lbl8.grid(row=0, column=3, padx=10, sticky='NW')

        # lbl9 = tk.Label(self.frame_example, text="DCT:")
        # lbl9.grid(row=0, column=4, padx=10, sticky='NW')

        # lbl10 = tk.Label(self.frame_example, text="gradient:")
        # lbl10.grid(row=0, column=5, padx=10, sticky='NW')

        # lbl11 = tk.Label(self.frame_example, text="scale:")
        # lbl11.grid(row=0, column=6, padx=10, sticky='NW')

        lbl12 = tk.Label(self.frame_example, text="another image from class:")
        lbl12.grid(row=0, column=2, padx=10, sticky='NW')

        self.images_1 = [tk.Label(self.frame_example), tk.Label(self.frame_example), tk.Label(self.frame_example),
                         tk.Label(self.frame_example),
                         tk.Label(self.frame_example), tk.Label(self.frame_example), tk.Label(self.frame_example)]
        for i in range(len(self.images_1)):
            self.images_1[i].grid(row=1, column=i + 1, sticky='N', padx=10, pady=2)

    def choose_file(self):
        self.s_filename = fd.askopenfilename(title="Открыть файл", initialdir="/")

    def load_data(self):
        try:
            if (self.chooseData.get() == "ORL face database 64x64"):
                print("64x64")
                self.data = get_faces()
            if (self.chooseData.get() == "ORL face database 112x92"):
                self.data = read_faces_from_disk()
                print("112x92")
            self.loadDataCompleteLabel.config(text="Load completed")
        except Exception as e:
            print(e)
            messagebox.showinfo("Attention", "Can't load database")

    def set_feature(self):
        try:
            if (self.choosenMethod.get() == "histogram"):
                self.method = get_histogram
            if (self.choosenMethod.get() == "dft"):
                self.method = get_dft
            if (self.choosenMethod.get() == "dct"):
                self.method = get_dct
            if (self.choosenMethod.get() == "scale"):
                self.method = get_scale
            if (self.choosenMethod.get() == "gradient"):
                self.method = get_gradient
        except Exception:
            messagebox.showinfo("Attention", "Please, select method")
            return

    # def start_comp(self):
    #     if self.chooseClassification.get() == "Training sample":
    #         self.start_computing_1()
    #     elif self.chooseClassification.get() == "Not training sample":
    #         self.start_computing_2()
    #     elif self.chooseClassification.get() == "Cross-validation":
    #         self.start_computing_3()
    #     else:
    #         messagebox.showinfo("Attention", "Please, select any sample")
    #         return

    # def start_computing_1(self):
    #     if self.method is None:
    #         self.set_feature()
    #     result = teach_parameter(self.data, choose_n_from_data(self.data, 3), self.method)
    #     self.bestParameter.configure(text=str(result[0][0]))
    #     self.accuracy.configure(text=str(result[0][1]))
    #     # ГРАФИК ПО RESULT[1] (RESULT[1][0] B RESULT[1][1])
    #     plt.rcParams["font.size"] = "5"
    #     fig = plt.figure(figsize=(2.5, 2))
    #     ax = fig.add_subplot(111)
    #     ax.plot(result[1][0], result[1][1])
    #     fig.title("Зависимость точности от параметра метода")
    #     ax.set(xlabel='Параметр метода',
    #            ylabel='Точность',
    #            title='Зависимость точности от параметра метода')
    #     buf = io.BytesIO()
    #     fig.savefig(buf)
    #     buf.seek(0)
    #     image = Image.open(buf)
    #     image = ImageTk.PhotoImage(image)
    #     self.stats[0].configure(image=image)
    #     self.stats[0].image = image
    #     plt.show()
    #
    # def start_computing_2(self):
    #     if self.method is None:
    #         self.set_feature()
    #     new_data = split_data3(self.data, images_per_person_in_train=3)
    #     result = teach_parameter([new_data[0], new_data[2]], [new_data[1], new_data[3]], self.method)
    #     print(result)
    #     self.bestParameter.configure(text=str(result[0][0]))
    #     self.accuracy.configure(text=str(result[0][1]))
    #     # ГРАФИК ПО RESULT[1] (RESULT[1][0] B RESULT[1][1])
    #     plt.rcParams["font.size"] = "5"
    #     fig = plt.figure(figsize=(2.5, 2))
    #     ax = fig.add_subplot(111)
    #     ax.plot(result[1][0], result[1][1])
    #     buf = io.BytesIO()
    #     fig.savefig(buf)
    #     buf.seek(0)
    #     image = Image.open(buf)
    #     image = ImageTk.PhotoImage(image)
    #     self.stats[0].configure(image=image)
    #     self.stats[0].image = image
    #
    # def start_computing_3(self):
    #     if self.data is None:
    #         messagebox.showinfo("Attention", "Please, select database")
    #         return
    #     try:
    #         self.number_face_test = [int(self.lowEntry.get()), int(self.highEntry.get())]
    #     except Exception:
    #         messagebox.showinfo("Attention", "Please, input integer numbers in range [10, 200]")
    #         return
    #
    #     lll1 = tk.Label(self.frame_stats, text="3 Folds", font="Arial 10")
    #     lll1.grid(row=0, column=1, padx=10)
    #     lll2 = tk.Label(self.frame_stats, text="5 Folds", font="Arial 10")
    #     lll2.grid(row=0, column=2, padx=10)
    #     lll4 = tk.Label(self.frame_stats, text="Best parameter and\ndifferent test sizes", font="Arial 10")
    #     lll4.grid(row=0, column=3, padx=10)
    #
    #     if self.number_face_test[0] < 10:
    #         self.number_face_test[0] = 10
    #         self.lowEntry.delete(0, "end")
    #         self.lowEntry.insert(0, self.number_face_test[0])
    #     if self.number_face_test[1] > 200:
    #         self.number_face_test[1] = 200
    #         self.highEntry.delete(0, "end")
    #         self.highEntry.insert(0, self.number_face_test[1])
    #     if self.method is None:
    #         self.set_feature()
    #     results = [0, 0, 0]
    #     x_train, x_test, y_train, y_test = split_data3(self.data, images_per_person_in_test=5)
    #     train = mesh_data([x_train, y_train])
    #     test = mesh_data([x_test, y_test])
    #     print(self.method)
    #     count = 0
    #     for f in [3, 5]:  # ДОБАВИТЬ 5
    #         print(f)
    #         res = cross_validation3(self.data, self.method, folds=f)
    #         if res[0][1] > results[1]:
    #             results = [res[0][0], res[0][1], f]
    #         plt.rcParams["font.size"] = "5"
    #         fig = plt.figure(figsize=(2.5, 2))
    #         ax = fig.add_subplot(111)
    #         ax.plot(res[1][0], res[1][1])  # статистика
    #         buf = io.BytesIO()
    #         fig.savefig(buf)
    #         plt.subplot(121)
    #         buf.seek(0)
    #         image = Image.open(buf)
    #         image = ImageTk.PhotoImage(image)
    #         self.stats[count].configure(image=image)
    #         self.stats[count].image = image
    #         count += 1
    #
    #     # self.label_now_method.configure(text = str(self.method.__name__[4:]))
    #     self.bestParameter.configure(text=str(results[0]))
    #     self.accuracy.configure(text=str(results[1]))
    #     # self.bestFold.configure(text=str(results[2]))
    #
    #     sizes = range(int(self.number_face_test[0]), int(self.number_face_test[1]), 10)
    #     test_results = [sizes, []]
    #     for size in sizes:
    #         test_results[1].append(test_classifier(train, choose_n_from_data(test, size), self.method, results[0]))
    #     plt.rcParams["font.size"] = "5"
    #     fig = plt.figure(figsize=(2.5, 2))
    #     ax = fig.add_subplot(111)
    #     ax.plot(test_results[0], test_results[1])
    #     buf = io.BytesIO()
    #     fig.savefig(buf)
    #     buf.seek(0)
    #     image = Image.open(buf)
    #     image = ImageTk.PhotoImage(image)
    #     self.stats[count].configure(image=image)
    #     self.stats[count].image = image

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


pba = PhotoBoothApp()
pba.root.mainloop()

