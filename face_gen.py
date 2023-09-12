import cv2
import os


def create_or_update_person_dataset(person_id, number_of_photos):
    path = os.path.dirname(os.path.abspath(__file__))
    # указываем, что мы будем искать лица по примитивам Хаара
    detector = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    # счётчик изображений
    i = 0
    # расстояния от распознанного лица до рамки
    offset = 50
    # получаем доступ к камере
    video = cv2.VideoCapture(0)


    while True:
        # берём видеопоток
        ret, im = video.read()
        # переводим всё в ч/б для простоты
        gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        # настраиваем параметры распознавания и получаем лицо с камеры
        faces = detector.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5, minSize=(100, 100))
        # обрабатываем лица
        for (x, y, w, h) in faces:
            # увеличиваем счётчик кадров
            i = i + 1
            # записываем файл на диск
            cv2.imwrite("dataSet/face-" + person_id + '.' + str(i) + ".jpg",
                        gray[y - offset:y + h + offset, x - offset:x + w + offset])
            # формируем размеры окна для вывода лица
            cv2.rectangle(im, (x - 50, y - 50), (x + w + 50, y + h + 50), (225, 0, 0), 2)
            # показываем очередной кадр, который мы запомнили
            cv2.imshow('im', im[y - offset:y + h + offset, x - offset:x + w + offset])
            # делаем паузу
            cv2.waitKey(100)
        # если у нас хватает кадров
        if i > number_of_photos:
            # освобождаем камеру
            video.release()
            # удалаяем все созданные окна
            cv2.destroyAllWindows()
            # останавливаем цикл
            break


create_or_update_person_dataset(input('Enter person id: '), 50)