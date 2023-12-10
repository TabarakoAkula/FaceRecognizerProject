import os
import sqlite3
from statistics import mean

import app_info
from checker import Checker
from colorama import Fore, init
from colorama import Style
from face_gen import FaceGen
from face_train import FaceTrainer
from pick import pick
from prettytable import PrettyTable
from work_with_db import DbWorker

__all__ = ()

database = DbWorker()
init(autoreset=True)
start_checker = False


def clear_console():
    if os.name == "posix":
        _ = os.system("clear")
    else:
        _ = os.system("cls")


def success(input_required=True):
    print(Style.BRIGHT + Fore.GREEN + "\nSuccessful      ")
    if input_required:
        input("\nPress enter....")


class ModelMethods:
    @staticmethod
    def get_photos():
        clear_console()
        try:
            person_id = int(input("Enter person id: "))
        except ValueError:
            print(
                Style.BRIGHT + Fore.RED + "\nERROR:",
                "please, enter int id:",
            )
            input("\nPress enter....")
            return
        person_id = str(person_id)
        try:
            if not database.get_one_user(person_id):
                print(
                    Style.BRIGHT + Fore.RED + "\nERROR:",
                    "no user with id:",
                    Style.BRIGHT + Fore.MAGENTA + person_id,
                    "in db",
                )
                input("\nPress enter....")
                return
        except sqlite3.OperationalError:
            print(
                Style.BRIGHT + Fore.RED + "\nERROR:",
                "please fix your database",
            )
            input("\nPress enter....")
            return
        number_of_photos = abs(
            int(input("Enter number of photos u required: ")),
        )
        frame_time = 10
        show_window = (
            True if input("Show window? Y/N: ").lower() == "y" else False
        )
        print("\n" + Style.BRIGHT + Fore.BLUE + "Start recording", end="\r")
        FaceGen().create_or_update_person_dataset(
            person_id,
            number_of_photos,
            show_window,
            frame_time,
        )
        success(input_required=False)
        print(f"{number_of_photos} photos have been created")
        input("\nPress enter....")
        return

    @staticmethod
    def start_training():
        clear_console()
        show_window = (
            True if input("Show window? Y/N: ").lower() == "y" else False
        )
        print("\n" + Style.BRIGHT + Fore.BLUE + "Start recording", end="\r")
        yml_path = FaceTrainer().start_training(show_window, 1)
        if yml_path == "Error":
            print(
                Style.BRIGHT + Fore.RED + "\nERROR:",
                "please, get new photos",
            )
            input("\nPress enter....")
            return
        success(input_required=False)
        print("Saved .yml file at:", Style.BRIGHT + Fore.MAGENTA + yml_path)
        input("\nPress enter....")
        return

    def checker_analyzer(self, data):
        try:
            if data["error"]:
                print(
                    Style.BRIGHT + Fore.RED + "\nERROR:",
                    "please, get new photos",
                )
                input("\nPress enter....")
                return None
        except KeyError:
            pass
        data = {i: data[i] for i in data if len(data[i]) >= 3}
        data = {i: data[i][1:-1] for i in data}
        data = {i: round(mean(data[i]), 1) for i in data}
        return data

    def start_checker(self):
        clear_console()
        try:
            is_users = database.get_all_users()
        except sqlite3.OperationalError:
            print(
                Style.BRIGHT + Fore.RED + "\nERROR:",
                "please fix your database",
            )
            input("\nPress enter....")
            return
        if not is_users:
            print(
                Style.BRIGHT + Fore.RED + "ERROR:",
                "no users in db",
            )
            input("\nPress enter....")
            return
        print(Style.BRIGHT + Fore.BLUE + "Checker is activated")
        checker_object = Checker()
        confidence_dictionary_clear = checker_object.init_checker()
        maximum_match = max(
            self.checker_analyzer(confidence_dictionary_clear).items(),
            key=lambda x: x[1],
        )
        predicted_user = maximum_match[0]
        data = {
            "predicted_user": predicted_user,
            "confidence": maximum_match[1],
        }
        app_info.info_app_starter(data)

        print(
            "predicted user:" + Style.BRIGHT + Fore.MAGENTA + maximum_match[0],
        )
        print(
            "confidence:"
            + Style.BRIGHT
            + Fore.MAGENTA
            + str(maximum_match[1]),
        )
        input("\nPress enter....")
        return


class TerminalMenu:
    def base_asker(self):
        options = ["Dataset", "Model", "Checker", "Exit"]
        answer, index = pick(options=options)
        match answer:
            case "Dataset":
                self.model_asker()
            case "Model":
                self.db_asker()
            case "Checker":
                ModelMethods().start_checker()
                self.base_asker()
            case "Exit":
                exit()

    def model_asker(self):
        options = ["Get New", "Training", "Checker", "Back"]
        answer, index = pick(options=options)
        match answer:
            case "Get New":
                ModelMethods.get_photos()
            case "Training":
                ModelMethods.start_training()
            case "Checker":
                ModelMethods().start_checker()
                self.model_asker()
            case "Back":
                self.base_asker()
        self.model_asker()

    def db_asker(self):
        options = [
            "Get all users",
            "Get one user",
            "Add user",
            "Edit user",
            "Delete user",
            "Clear database",
            "Create table",
            "Back",
        ]
        answer, index = pick(options=options)

        clear_console()
        match answer:
            case "Get all users":
                response = ""
                try:
                    response = database.get_all_users()
                except sqlite3.OperationalError:
                    print(
                        Style.BRIGHT + Fore.RED + "\nERROR:",
                        "Please check tables in your db",
                    )
                else:
                    if response:
                        tab = PrettyTable(["ID", "NAME"], hrules=True)
                        tab.align = "l"
                        tab.add_rows(response)
                        print(tab)
                    else:
                        print(
                            Style.BRIGHT
                            + Fore.BLUE
                            + "No data in table now :(",
                        )
                input("\nPress enter....")
            case "Get one user":
                try:
                    user_id = int(input("Enter user id: "))
                except ValueError:
                    print(
                        Style.BRIGHT + Fore.RED + "\nERROR:",
                        "Enter integer please",
                    )
                else:
                    tab = PrettyTable(["ID", "NAME"])
                    user_info = ""
                    try:
                        user_info = database.get_one_user(str(user_id))
                    except sqlite3.OperationalError:
                        print(
                            Style.BRIGHT + Fore.RED + "\nERROR:",
                            "Please check tables in your db",
                        )
                    else:
                        if user_info:
                            tab.add_rows(user_info)
                            print(tab)
                        else:
                            print(
                                "\n" + Style.BRIGHT + Fore.RED + "ERROR:",
                                "unknown id",
                                Style.BRIGHT + Fore.MAGENTA + str(user_id),
                            )
                input("\nPress enter....")
            case "Add user":
                username = input("Enter user name: ")
                try:
                    database.add_user(username)
                except sqlite3.OperationalError:
                    print(
                        Style.BRIGHT + Fore.RED + "\nERROR:",
                        "Please check tables in your db",
                    )
                    input("\nPress enter....")
                else:
                    success()
            case "Edit user":
                change_name = False
                user_name = ""
                try:
                    user_id = int(input("Enter user id: "))
                except ValueError:
                    print(
                        Style.BRIGHT + Fore.RED + "\nERROR:",
                        "Enter integer please",
                    )
                else:
                    try:
                        if database.get_one_user(str(user_id)):
                            if input("Change username? Y/N: ").lower() == "y":
                                change_name = True
                                user_name = input("Enter new username: ")
                            if change_name:
                                database.edit_user_info(
                                    user_id,
                                    user_name,
                                )
                                success(input_required=False)
                            else:
                                print(
                                    "\n"
                                    + Style.BRIGHT
                                    + Fore.BLUE
                                    + "Nothing changed :/",
                                )
                                success(input_required=False)
                        else:
                            print(
                                Style.BRIGHT + Fore.RED + "\nERROR:",
                                "unknown user with id",
                                Style.BRIGHT + Fore.MAGENTA + str(user_id),
                            )
                    except sqlite3.OperationalError:
                        print(
                            Style.BRIGHT + Fore.RED + "\nERROR:",
                            "Please check tables in your db",
                        )
                        input("\nPress enter....")
                input("\nPress enter....")
            case "Delete user":
                try:
                    user_id = int(input("Enter user id: "))
                except ValueError:
                    print(
                        Style.BRIGHT + Fore.RED + "\nERROR:",
                        "Enter integer please",
                    )
                else:
                    try:
                        user_info = database.get_one_user(str(user_id))
                        try:
                            info_ask = (
                                Style.BRIGHT
                                + Fore.MAGENTA
                                + str(user_info[0][1])
                            )
                        except IndexError:
                            print(
                                Style.BRIGHT + Fore.RED + "\nERROR:",
                                "unknown user with id",
                                Style.BRIGHT + Fore.MAGENTA + str(user_id),
                            )
                        else:
                            if (
                                input(
                                    f"Delete user"
                                    f" {info_ask}?"
                                    f" {Style.NORMAL + Fore.WHITE}Y/N: ",
                                ).lower()
                                == "y"
                            ):
                                database.delete_user(user_id)
                            else:
                                print(
                                    "\n"
                                    + Style.BRIGHT
                                    + Fore.BLUE
                                    + "Nothing changed :/",
                                )
                            success(input_required=False)
                    except sqlite3.OperationalError:
                        print(
                            Style.BRIGHT + Fore.RED + "\nERROR:",
                            "Please check tables in your db",
                        )
                input("\nPress enter....")
            case "Clear database":
                db_name = input("Enter name of db: ")
                try:
                    database.clear_db(db_name)
                except sqlite3.OperationalError:
                    print(
                        Style.BRIGHT + Fore.RED + "\nERROR:",
                        "No such table",
                        Style.BRIGHT + Fore.MAGENTA + db_name,
                    )
                    input("\nPress enter....")
                    self.db_asker()
                success()
            case "Create table":
                clear_console()
                db_name = input("Enter name of db: ")
                try:
                    database.create_db(db_name)
                except sqlite3.OperationalError:
                    print(
                        "\n" + Style.BRIGHT + Fore.RED + "ERROR:",
                        f"Table '{db_name}' already exists\n",
                    )
                else:
                    success(input_required=False)
                input("\nPress enter....")
            case "Back":
                self.base_asker()
        self.db_asker()


if __name__ == "__main__":
    menu = TerminalMenu()
    menu.base_asker()
