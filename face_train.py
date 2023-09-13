import cv2
import os
import numpy as np
from PIL import Image


class FaceTrainer(object):
    # получаем картинки и подписи из датасета
    @staticmethod
    def get_images_and_labels(datapath: str, enable_window: bool, window_time: int):
        # указываем, что мы будем искать лица по примитивам Хаара
        faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
        # путь к датасету с фотографиями пользователей
        # получаем путь к картинкам
        image_paths = [os.path.join(datapath, f) for f in os.listdir(datapath)]
        # списки картинок и подписей на старте пустые
        images = []
        labels = []
        # перебираем все картинки в датасете
        for image_path in image_paths:
            # читаем картинку и сразу переводим в ч/б
            image_pil = Image.open(image_path).convert('L')
            # переводим картинку в numpy-массив
            image = np.array(image_pil, 'uint8')
            # получаем id пользователя из имени файла
            nbr = int(os.path.split(image_path)[1].split(".")[0].replace("face-", ""))
            # определяем лицо на картинке
            faces = faceCascade.detectMultiScale(image)
            # если лицо найдено
            for (x, y, w, h) in faces:
                # добавляем его к списку картинок
                images.append(image[y: y + h, x: x + w])
                # добавляем id пользователя в список подписей
                labels.append(nbr)
                if enable_window:
                    # выводим текущую картинку на экран
                    cv2.imshow("Adding faces to traning set...", image[y: y + h, x: x + w])
                    # делаем паузу
                    cv2.waitKey(window_time)
        # возвращаем список картинок и подписей
        return images, labels

    def start_training(self, show_window: bool, frame_time: int):
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        path = os.path.dirname(os.path.abspath(__file__))
        dataPath = path + r'/dataSet'

        images, labels = self.get_images_and_labels(dataPath, show_window, frame_time)
        # обучаем модель распознавания на наших картинках и учим сопоставлять её лица и подписи к ним
        recognizer.train(images, np.array(labels))
        # сохраняем модель
        recognizer.save(path + r'/trainer/trainer.yml')
        # удаляем из памяти все созданные окна
        cv2.destroyAllWindows()
        return


if __name__ == '__main__':
    Obj = FaceTrainer()
    Obj.start_training()
