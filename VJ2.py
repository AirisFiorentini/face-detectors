import cv2
import os


def violaJones(pathToImage, index):
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

    width = 3
    faceColor = (0, 0, 255)
    eyesColor = (0, 255, 0)
    scale = 1.3
    neighbours = 3
    minSize = (10, 10)
    image = cv2.imread(pathToImage)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, scale, neighbours)
    for x, y, w, h in faces:
        img = cv2.rectangle(image, (x, y), (x + w, y + h), faceColor, width)
        gray = gray[y:y + h, x:x + w]
        color = img[y:y + h, x:x + w]

        eyes = eye_cascade.detectMultiScale(gray)
        for ex, ey, ew, eh in eyes:
            cv2.rectangle(color, (ex, ey), (ex + ew, ey + eh), eyesColor, width)

    cv2.imshow('img', image)
    cv2.imwrite(os.path.join('results', f'{index}.jpg'), image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def run(file_directory, imageFormat='jpg'):
    images = [os.path.join(file_directory, f'{i}.{imageFormat}') for i in range(1, 11)]
    for i in range(0, 11):
        print(f'detecting {images[i]}')
        violaJones(images[i], i)


if __name__ == '__main__':
    run('test', 'jpg')
