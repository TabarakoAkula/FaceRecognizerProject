import cv2


class Checker(object):
    @staticmethod
    def checker() -> None:
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        recognizer.read('trainer/trainer.yml')
        faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
        # Тип шрифта
        font = cv2.FONT_HERSHEY_SIMPLEX
        # Список имен для id
        names = ['None', 'Misha', "Katya", 'Egor']

        cam = cv2.VideoCapture(0)
        cam.set(3, 640)  # set video width
        cam.set(4, 480)  # set video height

        while True:
            ret, img = cam.read()
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            faces = faceCascade.detectMultiScale(
                gray,
                scaleFactor=1.2,
                minNeighbors=5,
                minSize=(10, 10),
            )

            for (x, y, w, h) in faces:
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
                id, confidence = recognizer.predict(gray[y:y + h, x:x + w])

                # Проверяем что лицо распознано
                if (confidence < 100):
                    id = names[id]
                    confidence = "  {0}%".format(round(100 - confidence))
                    print('Name:', id, 'Conf:', confidence, end='\r')
                else:
                    id = "unknown"
                    confidence = "  {0}%".format(round(100 - confidence))
                    print('Unknown', end='\r')
                cv2.putText(img, str(id), (x + 5, y - 5), font, 1, (255, 255, 255), 2)
                cv2.putText(img, str(confidence), (x + 5, y + h - 5), font, 1, (255, 255, 0), 1)

            cv2.imshow('camera', img)

            k = cv2.waitKey(10) & 0xff  # 'ESC' для Выхода
            if k == 27:
                break

        cam.release()
        cv2.destroyAllWindows()
        return


if __name__ == '__main__':
    Obj = Checker()
    Obj.checker()
