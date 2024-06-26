import tkinter as tk
from tkinter import ttk

from app.gui.project_gui import CreateProjectGUI
from app.gui.project_gui import OpenProjectGUI
from app.services.project_info import Project


class App:
    """Base class representing an application."""
    pass


class AppGUI(App):
    """Class representing the GUI for the CAD EEN application."""
    def __init__(self) -> None:
        self.root = tk.Tk()

        self.root.title("AutoCAD External engineering networks")
        self.root.geometry("380x150")

        self.root.call("source", "app/files/Theme/azure.tcl")
        self.root.call("set_theme", "light")

        self.root.resizable(False, False)

        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        icon = tk.PhotoImage(file="app/files/Theme/auto-cad.png")
        self.root.iconphoto(False, icon)

        self.frame_with_actions()

        self.project = None

        self.root.mainloop()

    def frame_with_actions(self) -> None:
        """
        Creates a label frame with actions related to the project and adds it
        to the root window.
        This function creates a label frame with the text "Дії з проектом"
        and adds it to the root window. It also creates a menubutton with the
        text "Проект" and adds it to the label frame. The menubutton has
        a menu with two commands: "Новий проект" and "Відкрити проект".
        Each command is associated with a corresponding callback function:
        `self.command_create_project` and `self.command_open_project`
        respectively. The menubutton and label frame are then grid-packed
        in the root window.
        """

        label_frame_actions_with_project = ttk.LabelFrame(
            self.root,
            text="Дії з проектом",
            padding=(10, 10),

        )

        menu_btb_project = ttk.Menubutton(
            self.root,
            text="Проект"
        )
        menu_btb_project.menu = tk.Menu(menu_btb_project)
        menu_btb_project["menu"] = menu_btb_project.menu

        menu_btb_project.menu.add_command(
            label="Новий проект",
            command=self.command_create_project
        )
        menu_btb_project.menu.add_command(
            label="Відкрити проект",
            command=self.command_open_project
        )
        menu_btb_project.grid(row=0, column=0, padx=30, pady=30, sticky="nsew")

        # label_frame_actions_with_project.grid(
        #     row=0,
        #     column=0,
        #     padx=10,
        #     pady=10,
        #     sticky="nsew"
        # )

    def command_create_project(self) -> None:
        """
        A method that triggers the creation of a new project window.
        It initializes the CreateProjectGUI class with the root window
        and calls the create_project_window method.
        """

        CreateProjectGUI(self.root).create_project_window()

    def command_open_project(self) -> None:
        """
        A method that triggers the creation of a new project window.
        It initializes the OpenProjectGUI class with the root window and calls
        the create_project_window method.
        """

        OpenProjectGUI(self.root).create_project_window()


class AppTerminal(App):
    """
    Class representing a terminal application.
    This class inherits from the App class.
    """

    @staticmethod
    def print_start_massage() -> None:
        print("\033[1;31mAutoCAD External Engineering Networks\033[0m\n")

        print(
            "У цьому додатку Ви можете керувати своїми проектами по інженерним"
            " мережам (створювати, редагувати та видаляти проекти).\n"
            "Проект - це набір файлів в форматі .dwg (загальні дані, профілі "
            "та інше), які створюються під окремий проект.\n"
            "Проект буде створенний з шаблонів (наразі - тільки для ЗВК).\n")

        print("Дії, які можна виконувати:")

        print("[1]. \033[1mСТВОРИТИ\033[0m\n"
              "\tВам необхідно вказати коротку назву для проекту "
              "(наприклад: Жовтнева, Перемоги), потім вибрати директорію для "
              "створення проекту.\n"
              "\tПісля цього буде створена папка з назвою "
              "'Коротка назва проекту' з шаблонами файлів.\n"
              "\tДалі, Вам необхідно буде заповнити дані проекту "
              "(повна назва, № ТУ і таке інше)\n")
        print("[0]. \033[1mEXIT\033[0m\n")

    def print_error_massage_wrong_command(self, commands: dict) -> None:
        print("-" * 48)
        print("\033[1;31mВи ввели не коректну команду. "
              "Допустимі команди:\033[0m")
        self.create_command_menu(commands)
        print("-" * 48)

    @staticmethod
    def create_command_list(commands: dict) -> list:
        return ([key for key, value in commands.items()]
                + [value for key, value in commands.items()])

    @staticmethod
    def create_command_menu(commands: dict) -> None:
        for key, value in commands.items():
            print(f"\033[1m[{key}]:\033[0m {value.title()}")

    def create_new_project(self):
        """
        Creates a new project.
        This function prompts the user to enter a short name for the project.
        It then creates a new instance of the Project class with the entered
        short name and calls the create_project_folder_with_template_dwg
        method to create a project folder with a template DWG file.

        After that, it displays a menu asking the user if they want to fill in
        the project data. The user can enter either "0" or "1" to respond.
        If the user enters "0", the project.take_from_user_project_info method
        is called to fill in the project data.

        The function then retrieves the paths to all DWG files in the project
        folder using the path_to_all_dwg_project_files method of the project
        instance. It displays a message indicating that the project is being
        created and calls the write_template_project_info method of the project
        instance to write project information to the DWG files. Finally, it
        calls the open_project_folder method of the project instance to open
        the project folder.

        If the user enters an invalid command, the function displays an error
        message and prompts the user to enter a valid command.
        """

        short_name = input("\033[1mВведіть коротку назву:\033[0m ").lower()

        project = Project(short_name)
        project.create_project_folder_with_template_dwg()

        commands = {
            "0": "так",
            "1": "ні",
        }

        print("-" * 48)
        print("Заповнити дані проекту?")
        self.create_command_menu(commands)
        command = input("\033[1mВведіть команду:\033[0m ").lower()
        while True:
            if command not in self.create_command_list(commands):
                while True:
                    self.print_error_massage_wrong_command(commands)
                    command = input("\033[1mВведіть команду:\033[0m ").lower()
                    if command in self.create_command_list(commands):
                        break
            if command in ("0", "так"):
                project.take_from_user_project_info()
            dwg_files = project.path_to_all_dwg_project_files(
                project.path_to_project
            )

            print("Зачекайте, створюється проект. Це може зайняти 1-2хв.")

            project.write_template_project_info(dwg_files)
            project.open_project_folder(project.path_to_project)
            break

    def user_action(self):
        """
        This function prompts the user for a command and performs different
        actions based on the command.
        """

        self.print_start_massage()

        commands = {
            "1": "створити",
            "0": "exit",
        }

        while True:
            command = input("\033[1mВведіть команду:\033[0m ").lower()
            if command not in self.create_command_list(commands):
                self.print_error_massage_wrong_command(commands)

            if command in ("1", "створити"):
                self.create_new_project()
                break

            if command in ("0", "exit"):
                break
