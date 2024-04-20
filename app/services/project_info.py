import os
from shutil import copytree
import json

import easygui

from app.services.autocad import Autocad


class Project:
    """
    This class represents a project and provides methods to interact with the
    project.
    """
    property_template = {
        "Назва об'єкту": "PROJECT NAME",
        "Розділ проекту": "Зовнішні мережі водопостачання та каналізації",
        "Стадія проектування": "Р",
        "ТУ В1": "00000",
        "ТУ К1": "11111",
        "ТУ К2": "22222",
        "Проектна організація": "ФОП Столярчук О.В.",
        "ГІП": "Столярчук",
        "Розробив": "Грицай",
        "Замовник": "CUSTOMER NAME",
        "Представник Водоканалу": "SIGNATORY PROJECT",
        "Посада представника": "JOB TITLE SIGNATORY",
        "ID Проекту": "PROJECT ID",
    }

    def __init__(self, short_name: str | None = None) -> None:
        """
        Initialize a Project instance.

        Args:
        short_name (str, optional): The short name of the project.
        Defaults to None.
        """

        self.acad = Autocad()
        self.path_to_project = None
        self.short_name = short_name

    def add_json_info_file_project(self) -> None:
        """
        Add a JSON info file to the project.
        """
        json_info_file = json.dumps(self.property_template)
        file_path = os.path.join(self.path_to_project, "project_info.json")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(json_info_file)

    def write_user_property(self, key: str, value: str) -> None:
        """
        Write a user property to the drawings.

        Args:
        key (str): The key of the user property.
        value (str): The value of the user property.
        """
        opened_drawings = [drawing for drawing in self.acad.docs]
        for drawing in opened_drawings:
            self.acad.add_user_property_to_drawing(drawing, key, value)

    def write_all_property(self, **kwargs) -> None:
        """
        Write all properties to the open drawings and save them.

        Args:
        kwargs (dict): The properties to be written.
        """

        opened_drawings = [drawing for drawing in self.acad.docs]

        # Remove the first item from the list (usually the main document)
        del opened_drawings[0]
        for drawing in opened_drawings:
            for key, value in kwargs.items():
                self.acad.add_user_property_to_drawing(
                    drawing=drawing,
                    key=key,
                    value=value
                )
            self.acad.quick_save_dwg(drawing)
        while opened_drawings:
            drawing = opened_drawings.pop()
            self.acad.close_dwg(drawing)

    def write_template_project_info(
            self,
            project_files_path: list[str]
    ) -> None:
        """
        Write the template project information to the project files.

        Args:
        project_files_path (list[str]): List of paths to the project files.
        """
        for file_path in project_files_path:
            opened_files = [doc.FullName for doc in self.acad.docs]
            if file_path not in opened_files:
                self.acad.open_dwg(file_path)
        self.write_template_user_property()

    def write_template_user_property(self) -> None:
        """
        Write the template user property to the project files.
        """
        self.write_all_property(**self.property_template)

    @staticmethod
    def choose_path_for_project() -> str:
        """
        Opens a dialog box for the user to choose a location for a new project.

        Returns:
        str: The path to the chosen location.
        """
        # Open a dialog box to choose a location for a new project
        return easygui.diropenbox(title="Виберіть місце для нового проекту")

    def create_project_folder_with_template_dwg(
            self,
            path_to_project: str | None = None
    ) -> None:
        """
        Creates a new project folder with a template DWG file.

        Args:
        path_to_project (str, optional): The path to the new project.
        Defaults to None.
        """

        # Get the directory of the current file
        app_directory = os.path.dirname(
            os.path.dirname(
                os.path.abspath(__file__)
            )
        )
        # Define the path to the template DWG file
        path_to_template = os.path.join(
            app_directory,
            "files", "dwg_template", "project_water_sewerage"
        )
        self.short_name = self.short_name.lower().title()

        # If no path to the project is provided, open a dialog box to choose
        # a location
        if path_to_project is None:
            path_to_project = easygui.diropenbox(
                title="Виберіть місце для нового проекту"
            )
        self.path_to_project = os.path.join(path_to_project, self.short_name)

        # Copy the template DWG file to the new project folder
        copytree(path_to_template, self.path_to_project, dirs_exist_ok=True)

        # Rename the DWG files in the new project folder
        self.rename_file_dwg_for_new_project(path_to_project)

    @staticmethod
    def path_to_all_dwg_project_files(path_to_project: str) -> list:
        """
        Get a list of all DWG files in the specified project directory.

        Args:
        path_to_project (str): The path to the project directory.

        Returns:
        list[str]: A list of paths to DWG files.
        """
        dwg_files: list[str] = []
        for root, dirs, files in os.walk(path_to_project):
            for file in files:
                if file.endswith(".dwg"):
                    dwg_files.append(os.path.join(root, file))
        return dwg_files

    @staticmethod
    def path_to_json_project_files(path_to_project: str) -> str | bool:
        """
        Get the path to the JSON project file.

        Args:
        path_to_project (str): The path to the project directory.

        Returns:
        Union[str, bool]: The path to the JSON project file if it exists, False otherwise.
        """
        path_to_json = os.path.join(path_to_project, "project_info.json")
        if os.path.exists(path_to_json):
            return path_to_json
        return False

    def rename_file_dwg_for_new_project(self, path_to_project: str) -> None:
        """
        This method renames all DWG files in a given project directory.

        Args:
        path_to_project (str): The path to the project directory.

        Returns:
        None
        """
        dwg_files = self.path_to_all_dwg_project_files(path_to_project)
        for dwg_file in dwg_files:
            directory, filename = os.path.split(dwg_file)
            new_file_name = filename.split("_")
            new_file_name[0] = self.short_name
            new_file_name = "_".join(new_file_name)

            old_file_path = os.path.join(directory, filename)
            new_file_path = os.path.join(directory, new_file_name)

            os.rename(old_file_path, new_file_path)

    @staticmethod
    def open_project_folder(path_to_project: str) -> None:
        """
        Open the project folder in the default file explorer.

        Args:
        path_to_project (str): The path to the project folder.

        Returns:
        None
        """

        # Use the os.startfile function to open the project folder in the
        # default file explorer
        os.startfile(path_to_project)

    def take_from_user_project_info(self) -> None:
        """
        This method prompts the user to input additional information for
        the project.
        The information is stored in the `property_template` dictionary and
        is later used to write properties to the drawing files.
        """

        print("\033[1mВам необхідно додати необхідну інформацію до проекту.\n"
              "Ці дані будуть збереженні у властивостях файлів .dwg\033[0m\n")
        for key in self.property_template:
            print(f"Введіть: \033[1;31m{key}\033[0m\n"
                  f"(за замовчуванням: "
                  f"\033[1;31m{self.property_template[key]}\033[0m)")
            value = input("Введіть значення або натисніть Enter: ")
            print()
            if value:
                self.property_template[key] = value
        for key, value in self.property_template.items():
            print(f"\033[1m{key}\033[0m: {value}")

    def open_exist_project(self) -> tuple[dict, str] | bool:
        """
        Open an existing project.
        This method opens an existing project by locating the JSON project file
        and loading its properties. If the project file exists, the method
        updates the `property_template` dictionary and sets the
        `path_to_project` attribute.
        Returns:
            tuple[dict, str] | bool: A tuple containing the project properties
            and the directory path of the project, or False if the project
            file does not exist.
        """
        path_to_json = self.path_to_json_project_files(
            self.choose_path_for_project()
        )
        if path_to_json:
            with open(path_to_json, "r") as json_file:
                project_properties = json.load(json_file)
            dir_project = os.path.dirname(path_to_json)
            self.property_template = project_properties
            self.path_to_project = dir_project

        return False
