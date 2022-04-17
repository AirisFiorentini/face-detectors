import numpy as np
import random as rnd
import cv2
import matplotlib.pyplot as plt
from skimage.filters import sobel as sob  # there is sobel in cv2
from skimage.filters import hessian, laplace, sato
import time
from skimage.measure import moments
from skimage.feature import hog
from mahotas import dog, euler, gaussian_filter, label, otsu
from mahotas.features import lbp, haralick, roundness
# import face_classification


def Euler(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    T_otsu = otsu(gray)
    gray = gray > T_otsu
    eulr = np.abs(euler(gray))
    return eulr, eulr


def sobel(img):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    edges = sob(img)
    # edges[edges > 0.05] = 1
    # edges[edges <= 0.05] = 0
    return edges, edges


def Laplace(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # h, w = gray.shape
    # new_size = (int(w * 0.5), int(h * 0.5))
    # gray = cv2.resize(gray, new_size, interpolation=cv2.INTER_AREA)
    edges = laplace(gray)
    # edges[edges > 0.05] = 1
    # edges[edges <= 0.05] = 0
    return edges, edges


def DOG(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # h, w = gray.shape
    # new_size = (int(w * 0.5), int(h * 0.5))
    # gray = cv2.resize(gray, new_size, interpolation=cv2.INTER_AREA)
    edges = dog(gray)
    return edges.astype(int), edges


def hough(img):
    res = np.copy(img)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    h, w = gray.shape
    # new_size = (int(w * 0.5), int(h * 0.5))
    # gray = cv2.resize(gray, new_size, interpolation=cv2.INTER_AREA)
    circles_img = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 10,
                                   param1=200, param2=50, minRadius=10, maxRadius=0)
    feature = 0
    if circles_img is not None:
        feature = circles_img.shape[1]
        circles_img = np.uint16(np.around(circles_img))
        for i in circles_img[0, :]:
            cv2.circle(res, (i[0], i[1]), i[2], (0, 255, 0), 2)
            cv2.circle(res, (i[0], i[1]), 2, (0, 0, 255), 3)
    return res, res


def gabor(img):
    # cv2.getGaborKernel(ksize, sigma, theta, lambda, gamma, psi, ktype)
    # ksize - size of gabor filter (n, n)
    # sigma - standard deviation of the gaussian function
    # theta - orientation of the normal to the parallel stripes
    # lambda - wavelength of the sunusoidal factor
    # gamma - spatial aspect ratio
    # psi - phase offset
    # ktype - type and range of values that each pixel in the gabor kernel can hold
    filters = []
    ksize = 51
    for theta in np.arange(0, np.pi, np.pi / 8):
        kern = cv2.getGaborKernel(ksize=(ksize, ksize), sigma=4.0, theta=theta, lambd=10.0,
                                  gamma=0.5, psi=0, ktype=cv2.CV_32F)
        kern /= 1.5 * kern.sum()
        filters.append(kern)
    accum = np.zeros_like(img)
    for kern in filters:
        fimg = cv2.filter2D(img, cv2.CV_8UC3, kern)
    np.maximum(accum, fimg, accum)
    return accum, accum


def get_methods():
    return [Euler, sobel, Laplace, DOG, hough, gabor]


def create_feature(images, method):
    return [method(image)[0] for image in images]


def distance(el1, el2):
    return np.linalg.norm(np.array(el1) - np.array(el2))


def classifier(data, new_elements, method):
    if method not in [Euler, sobel, Laplace, DOG, hough, gabor]:
        return []
    featured_data = create_feature(data[0], method)
    featured_elements = create_feature(new_elements, method)
    result = []
    for element in featured_elements:
        min_el = [1000, -1]
        for i in range(len(featured_data)):
            dist = distance(element, featured_data[i])
            if dist < min_el[0]:
                min_el = [dist, i]
        if min_el[1] < 0:
            result.append(0)
        else:
            result.append(data[1][min_el[1]])
    return result


def voting(data, new_elements):
    methods = [Euler, sobel, Laplace, DOG, hough, gabor]
    res = {}
    for method in methods:
        res[method.__name__] = classifier(data, new_elements, method)
    tmp = []
    for i in range(len(new_elements)):
        temp = {}
        for method in res:
            t = res[method][i]
            if t in temp:
                temp[t] += 1
            else:
                temp[t] = 1
        best_size = sorted(temp.items(), key=lambda item: item[1], reverse=True)[0]
        tmp.append(best_size[0])
    return tmp, res


def split_data(data, images_per_person_in_train=5):
    images_per_person = 10
    images_all = len(data[0])

    x_train, x_test, y_train, y_test = [], [], [], []

    for i in range(0, images_all, images_per_person):
        x_train.extend(data[0][i: i + images_per_person_in_train])
        y_train.extend(data[1][i: i + images_per_person_in_train])

        x_test.extend(data[0][i + images_per_person_in_train: i + images_per_person])
        y_test.extend(data[1][i + images_per_person_in_train: i + images_per_person])

    return x_train, x_test, y_train, y_test


def test_voting(train, test):
    res, _ = voting(train, test[0])
    sum = 0
    for i in range(len(test[0])):
        if test[1][i] == res[i]:
            sum += 1
    return sum / len(test[0])


def test_methods(train, test):
    res = {}
    for method in [Euler, sobel, Laplace, DOG, hough, gabor]:
        answers = classifier(train, test[0], method)
        correct_answers = 0
        for i in range(len(answers)):
            if answers[i] == test[1][i]:
                correct_answers += 1
        res[method.__name__] = correct_answers / len(answers)
    return res
