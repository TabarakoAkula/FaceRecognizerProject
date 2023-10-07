import os

from PIL import Image

import cv2

import numpy as np


class FaceTrainer(object):
    @staticmethod
    def get_images_and_labels(datapath: str,
                              enable_window: bool,
                              window_time: int):
        face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        )
        image_path1 = [os.path.join(datapath, f)
                       for f in os.listdir(datapath)]
        image_paths = []
        for i in image_path1:
            for j in os.listdir(i):
                image_paths.append(os.path.join(datapath, i, j))
        images = []
        labels = []
        for image_path in image_paths:
            image_pil = Image.open(image_path).convert('L')
            image = np.array(image_pil, 'uint8')
            nbr = int(os.path.split(image_path)[1].split('.')
                      [0].replace('face-', ''))
            faces = face_cascade.detectMultiScale(image)
            for x, y, w, h in faces:
                images.append(image[y: y + h, x: x + w])
                labels.append(nbr)
                if enable_window:
                    cv2.imshow(
                        'Adding faces to traning set...',
                        image[y: y + h, x: x + w],
                    )
                    cv2.waitKey(window_time)
        return images, labels

    def start_training(self, show_window: bool, frame_time: int):
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        path = os.path.dirname(os.path.abspath(__file__))
        data_path = path + r'/dataSet'

        images, labels = self.get_images_and_labels(data_path,
                                                    show_window,
                                                    frame_time)
        recognizer.train(images, np.array(labels))
        recognizer.save(path + r'/trainer/trainer.yml')
        cv2.destroyAllWindows()
        return


if __name__ == '__main__':
    Obj = FaceTrainer()
    Obj.start_training(True, 1)
