import os
from pathlib import Path

import cv2
import numpy as np
from PIL import Image


__all__ = ("FaceTrainer",)


class FaceTrainer(object):
    @staticmethod
    def get_images_and_labels(
        datapath,
        enable_window: bool,
        window_time: int,
    ):
        face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + "haarcascade_frontalface_default.xml",
        )
        image_path1 = [
            Path(datapath / f)
            for f in os.listdir(str(datapath))
            if ".gitkeep" not in f
        ]
        if not image_path1:
            return "Error", "no data in dataSet/"
        image_paths = []
        for i in image_path1:
            for j in os.listdir(i):
                image_paths.append(os.path.join(str(datapath), i, j))
        images = []
        labels = []
        for image_path in image_paths:
            image_pil = Image.open(image_path).convert("L")
            image = np.array(image_pil, "uint8")
            nbr = int(
                os.path.split(image_path)[1].split(".")[0].replace("face", ""),
            )
            faces = face_cascade.detectMultiScale(image)
            for x, y, w, h in faces:
                images.append(image[y : y + h, x : x + w])
                labels.append(nbr)
                if enable_window:
                    cv2.imshow(
                        "Adding faces to traning set...",
                        image[y : y + h, x : x + w],
                    )
                    cv2.waitKey(window_time)
        return images, labels

    def start_training(self, show_window: bool, frame_time: int):
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        path = Path(os.path.abspath(__file__)).parent
        data_path = Path(str(path) + "/dataSet")

        images, labels = self.get_images_and_labels(
            data_path,
            show_window,
            frame_time,
        )
        if images == "Error":
            return "Error"
        recognizer.train(images, np.array(labels))
        recognizer.save(str(path) + "/trainer/trainer.yml")
        cv2.destroyAllWindows()
        return str(path) + "/trainer/trainer.yml"


if __name__ == "__main__":
    Obj = FaceTrainer()
    Obj.start_training(True, 1)
