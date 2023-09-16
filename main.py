import logging
from face_gen import FaceGen
from face_train import FaceTrainer
from checker import Checker
from work_with_db import DbWorker

# логика логгера
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
logger.addHandler(handler)
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(module)s - %(funcName)s: %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

obj = DbWorker()


def get_new_photos():
    person_id = input('Enter person id: ')
    number_of_photos = int(input('Enter number of photos u required: '))
    additional = True if input('Additional? y/n: ') == 'y' else False
    show_window = True
    frame_time = 1
    if additional:
        show_window = True if input('Show window? y/n: ') == 'y' else False
        frame_time = int(input('Enter pause between frames: '))
    print('Start recording')
    FaceGen().create_or_update_person_dataset(person_id, number_of_photos, show_window, frame_time)
    print('End recording')
    return


def base_asker():
    print('\nChoose Option:\n'
          '1 Work with model\n'
          '2 Work with db\n'
          '3 exit')
    answer = int(input('Choose option number: '))
    match answer:
        case 1:
            model_asker()
        case 2:
            db_asker()
        case 3:
            exit()
    base_asker()


def model_asker():
    print(
        '\n1 Get New Photos\n'
        '2 Train Photos\n'
        '3 Start Checker\n'
        '4 exit')
    answer = int(input('Choose option number: '))
    match answer:
        case 1:
            get_new_photos()
        case 2:
            show_window, frame_time = True, 1
            additional = True if input('Additional? y/n: ') == 'y' else False
            if additional:
                show_window = True if input('Show window? y/n: ') == "y" else False
                frame_time = int(input('Enter pause between frames: '))
            print('Start training')
            FaceTrainer().start_training(show_window, frame_time)
            print('End training')
        case 3:
            print('Start checker')
            print('Press ESC to exit')
            Checker().checker()
        case 4:
            base_asker()
    model_asker()


def db_asker():
    print(
        '\n1 Get all users\n'
        '2 Get user info\n'
        '3 Add User\n'
        '4 Delete User\n'
        '5 Edit user\n'
        "6 Get number of id's\n"
        "7 Create db\n"
        "8 Clear db\n"
        '10 exit')
    answer = int(input('Choose option number: '))
    match answer:
        case 1:
            print('\n')
            response = obj.get_all_users()
            print('--- ' * 5)
            for i in response:
                print(i)
            print('--- ' * 5)
        case 2:
            print('\n')
            user_id = input('Enter user id: ')
            print('--- ' * 5)
            print(obj.get_one_user(user_id))
            print('--- ' * 5)
        case 3:
            print('\n')
            username = input('Enter user name: ')
            path = input('Enter path to photo: ')
            obj.add_user(username, path)
        case 4:
            print('\n')
            id = int(input('Enter user id: '))
            obj.delete_user(id)
        case 5:
            print('\n')
            change_name, change_path = False, False
            user_name, photo_path = '', ''
            user_id = int(input('Enter user id: '))
            if input('Change username? 1/0 ') == '1':
                change_name = True
                user_name = input('Enter username: ')
            if input('Change photo path? 1/0 ') == '1':
                change_path = True
                photo_path = input('Enter new path for photo: ')
            if change_path or change_name:
                obj.edit_user_info(user_id, user_name, photo_path, change_name, change_path)
            else:
                print('Hmmm okeey :/')
        case 6:
            print("Number of id's in db:", obj.get_number_of_users())
        case 7:
            db_name = input('Enter name for db: ')
            obj.create_db(db_name)
        case 8:
            db_name = input('Enter name of db: ')
            obj.clear_db(db_name)
        case 10:
            base_asker()
    db_asker()


if __name__ == '__main__':
    base_asker()
