from pathlib import Path

import cv2


__all__ = ("FaceGen",)


class FaceGen(object):
    @staticmethod
    def create_or_update_person_dataset(
        person_id: str,
        number_of_photos_required: int,
        *window_setting,
    ) -> None:
        is_directory_avaliable = Path("dataSet/" + str(person_id)).is_dir()
        if not is_directory_avaliable:
            Path("dataSet/" + str(person_id)).mkdir()

        enable_window, window_time = window_setting
        detector = cv2.CascadeClassifier(
            cv2.data.haarcascades + "haarcascade_frontalface_default.xml",
        )
        number_of_photos_made = 0
        offset = 50
        video = cv2.VideoCapture(0)

        while True:
            ret, im = video.read()
            gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
            faces = detector.detectMultiScale(
                gray,
                scaleFactor=1.2,
                minNeighbors=5,
                minSize=(100, 100),
            )
            for x_coord, y_coord, width, high in faces:
                number_of_photos_made = number_of_photos_made + 1
                cv2.imwrite(
                    f"dataSet/{person_id}/face{person_id}"
                    f".{str(number_of_photos_made)}.jpg",
                    gray[
                        y_coord - offset : y_coord + high + offset,
                        x_coord - offset : x_coord + width + offset,
                    ],
                )
                cv2.rectangle(
                    im,
                    (x_coord - 50, y_coord - 50),
                    (x_coord + width + 50, y_coord + high + 50),
                    (225, 0, 0),
                    2,
                )
                if enable_window:
                    cv2.imshow(
                        "im",
                        im[
                            y_coord - offset : y_coord + high + offset,
                            x_coord - offset : x_coord + width + offset,
                        ],
                    )
                cv2.waitKey(window_time)
            if number_of_photos_made >= number_of_photos_required:
                video.release()
                cv2.destroyAllWindows()
                break
        return


if __name__ == "__main__":
    Obj = FaceGen()
    Obj.create_or_update_person_dataset(
        input("Enter person id: "),
        20,
        True,
        1,
    )
