import os
import sqlite3
from statistics import mean

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
        person_id = int(input("Enter person id: "))
        number_of_photos = int(input("Enter number of photos u required: "))
        frame_time = 10
        show_window = (
            True if input("Show window? Y/N: ").lower() == "y" else False
        )
        print("\n" + Style.BRIGHT + Fore.BLUE + "Start recording", end="\r")
        FaceGen().create_or_update_person_dataset(
            str(person_id),
            number_of_photos,
            show_window,
            frame_time,
        )
        success(input_required=False)
        print(f"{number_of_photos} photos have been created")
        input("\nPress enter....")

    @staticmethod
    def start_training():
        clear_console()
        show_window = (
            True if input("Show window? Y/N: ").lower() == "y" else False
        )
        print("\n" + Style.BRIGHT + Fore.BLUE + "Start recording", end="\r")
        yml_path = FaceTrainer().start_training(show_window, 1)
        success(input_required=False)
        print("Saved .yml file at:", Style.BRIGHT + Fore.MAGENTA + yml_path)
        input("\nPress enter....")

    @staticmethod
    def start_checker():
        clear_console()
        is_users = database.get_all_users()
        if not is_users:
            print(Style.BRIGHT + Fore.RED + "ERROR:", "no users in db")
            input("\nPress enter....")
            return
        print(Style.BRIGHT + Fore.BLUE + "Checker is activated")
        confidence_dictionary_clear = Checker().checker()
        confidence_dictionary_without_random_values = {
            i: confidence_dictionary_clear[i]
            for i in confidence_dictionary_clear
            if len(confidence_dictionary_clear[i]) >= 3
        }
        confidence_dictionary_without_edge_values = {
            i: confidence_dictionary_without_random_values[i][1:-1]
            for i in confidence_dictionary_without_random_values
        }
        confidence_dictionary_with_max_values = {
            i: round(mean(confidence_dictionary_without_edge_values[i]), 1)
            for i in confidence_dictionary_without_edge_values
        }
        maximum_match = max(
            confidence_dictionary_with_max_values.items(),
            key=lambda x: x[1],
        )
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
                ModelMethods.start_checker()
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
                ModelMethods.start_checker()
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
            "Exit",
        ]
        answer, index = pick(options=options)

        clear_console()
        match answer:
            case "Get all users":
                response = database.get_all_users()
                if response:
                    tab = PrettyTable(["ID", "NAME"], hrules=True)
                    tab.align = "l"
                    tab.add_rows(response)
                    print(tab)
                else:
                    print(Style.BRIGHT + Fore.BLUE + "No data in table now :(")
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
                    user_info = database.get_one_user(str(user_id))
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
                database.add_user(username)
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
                    user_info = database.get_one_user(str(user_id))
                    try:
                        info_ask = (
                            Style.BRIGHT + Fore.MAGENTA + str(user_info[0][1])
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
                input("\nPress enter....")
            case "Clear database":
                db_name = input("Enter name of db: ")
                database.clear_db(db_name)
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
            case "Exit":
                self.base_asker()
        self.db_asker()


if __name__ == "__main__":
    menu = TerminalMenu()
    menu.base_asker()
