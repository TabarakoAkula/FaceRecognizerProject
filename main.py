import logging
from face_gen import FaceGen
from face_train import FaceTrainer
from checker import Checker

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
logger.addHandler(handler)
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(module)s - %(funcName)s: %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')


def get_new_photos():
    person_id = input('Enter person id: ')
    number_of_photos = int(input('Enter number of photos u required: '))
    additional = True if input('Additional? y/n: ') == 'y' else False
    show_window = True
    frame_time = 1
    if additional:
        show_window = True if input('Show window? y/n: ') == 'y' else False
        frame_time = int(input('Enter pause between frames: '))
    logger.info('Start recording')
    FaceGen().create_or_update_person_dataset(person_id, number_of_photos, show_window, frame_time)
    logger.info('End recording')
    return


def asker():
    print('\nChoose option:\n'
          '1 Get new photos\n'
          '2 Train photos\n'
          '3 Start checker\n'
          '4 exit')
    answer = int(input('Choose option number: '))
    if answer == 1:
        get_new_photos()
    elif answer == 2:
        show_window, frame_time = True, 1
        additional = True if input('Additional? y/n: ') == 'y' else False
        if additional:
            show_window = True if input('Show window? y/n: ') == "y" else False
            frame_time = int(input('Enter pause between frames: '))
        logger.info('Start training')
        FaceTrainer().start_training(show_window, frame_time)
        logger.info('End training')
    elif answer == 3:
        logger.info('Start checker')
        logger.info('Press ESC to exit')
        Checker().checker()
    elif answer == 4:
        exit()
    else:
        logger.info('Error!')
    asker()

if __name__ == '__main__':
    asker()
