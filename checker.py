import time

import app_welcome
from colorama import Fore, Style
import cv2
from work_with_db import DbWorker


__all__ = ("Checker",)


class Checker(object):
    def __init__(self):
        self.confidence_dictionary = {}

    def init_checker(self) -> dict:
        self.recognizer = cv2.face.LBPHFaceRecognizer_create()
        try:
            self.recognizer.read("trainer/trainer.yml")
        except cv2.error:
            return {"error": "no data"}
        print("Loaded", Style.BRIGHT + Fore.BLUE + "trainer.yml")
        self.face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + "haarcascade_frontalface_default.xml",
        )
        print("Loaded", Style.BRIGHT + Fore.BLUE + "haarcascade_frontalface")
        self.font = cv2.FONT_HERSHEY_SIMPLEX
        self.obj = DbWorker()
        self.names = self.obj.get_all_users(names=True)
        self.names.insert(0, ("Unknown",))
        for i in self.names:
            self.confidence_dictionary[i[0]] = []
        self.cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        self.cam.set(3, 640)
        self.cam.set(4, 480)
        print(Style.BRIGHT + Fore.BLUE + "Camera is ready")
        return self.runner()

    def runner(self):
        app_welcome.welcome_app_starter()
        return self.checker_launch()

    def checker_launch(self):
        self.start = time.time()
        self.ret, self.img = self.cam.read()
        while time.time() < self.start + 5:
            self.ret, self.img = self.cam.read()
            self.gray = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
            self.faces = self.face_cascade.detectMultiScale(
                self.gray,
                scaleFactor=1.2,
                minNeighbors=5,
                minSize=(10, 10),
            )
            for x, y, w, h in self.faces:
                cv2.rectangle(self.img, (x, y), (x + w, y + h), (0, 255, 0), 2)
                prediction_id, prediction_confidence = self.recognizer.predict(
                    self.gray[y : y + h, x : x + w],
                )

                # Проверяем, что лицо распознано
                if prediction_confidence < 100:
                    username_by_id = self.names[prediction_id]
                    self.confidence_dictionary[
                        self.names[prediction_id][0]
                    ].append(
                        round(100 - prediction_confidence),
                    )
                    prediction_confidence = "  {0}%".format(
                        round(100 - prediction_confidence),
                    )
                else:
                    username_by_id = "Unknown"
                    self.confidence_dictionary["Unknown"].append(
                        round(100 - prediction_confidence),
                    )
                    prediction_confidence = "  {0}%".format(
                        round(100 - prediction_confidence),
                    )

                cv2.putText(
                    self.img,
                    str(username_by_id),
                    (x + 5, y - 5),
                    self.font,
                    1,
                    (255, 255, 255),
                    2,
                )
                cv2.putText(
                    self.img,
                    str(prediction_confidence),
                    (x + 5, y + h - 5),
                    self.font,
                    1,
                    (255, 255, 0),
                    1,
                )

            cv2.imshow("camera", self.img)
            k = cv2.waitKey(10) & 0xFF  # 'ESC' для Выхода
            if k == 27:
                break
        self.cam.release()
        cv2.destroyAllWindows()
        return self.confidence_dictionary


if __name__ == "__main__":
    Obj = Checker()
    Obj.init_checker()
