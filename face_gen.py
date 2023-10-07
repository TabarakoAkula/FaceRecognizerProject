import cv2
import os


class FaceGen(object):
    @staticmethod
    def create_or_update_person_dataset(
        person_id: str, number_of_photos_required: int, *window_setting
    ) -> None:
        is_directory_avaliable = os.path.isdir("dataSet/" + str(person_id))
        if not is_directory_avaliable:
            os.mkdir("dataSet/" + str(person_id))

        enable_window, window_time = window_setting
        # указываем, что мы будем искать лица по примитивам Хаара
        detector = cv2.CascadeClassifier(
            cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
        )
        # счётчик изображений
        number_of_photos_made = 0
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
            faces = detector.detectMultiScale(
                gray, scaleFactor=1.2, minNeighbors=5, minSize=(100, 100)
            )
            # обрабатываем лица
            for x_coord, y_coord, width, high in faces:
                # увеличиваем счётчик кадров
                number_of_photos_made = number_of_photos_made + 1
                # записываем файл на диск
                cv2.imwrite(
                    "dataSet/"
                    + person_id
                    + "/face-"
                    + person_id
                    + "."
                    + str(number_of_photos_made)
                    + ".jpg",
                    gray[
                        y_coord - offset : y_coord + high + offset,
                        x_coord - offset : x_coord + width + offset,
                    ],
                )
                # формируем размеры окна для вывода лица
                cv2.rectangle(
                    im,
                    (x_coord - 50, y_coord - 50),
                    (x_coord + width + 50, y_coord + high + 50),
                    (225, 0, 0),
                    2,
                )
                # показываем очередной кадр, который мы запомнили
                cv2.imshow(
                    "im",
                    im[
                        y_coord - offset : y_coord + high + offset,
                        x_coord - offset : x_coord + width + offset,
                    ],
                )
                # делаем паузу
                cv2.waitKey(window_time)
            # если у нас хватает кадров
            if number_of_photos_made >= number_of_photos_required:
                # освобождаем камеру
                video.release()
                # удалаяем все созданные окна
                cv2.destroyAllWindows()
                # останавливаем цикл
                break
        return


if __name__ == "__main__":
    Obj = FaceGen()
    Obj.create_or_update_person_dataset(
        input("Enter person id: "), 20, True, 1
    )
