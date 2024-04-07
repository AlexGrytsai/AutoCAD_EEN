import os
from shutil import copytree

import easygui

from app.autocad import Autocad


class Project:
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
        self.acad = Autocad()
        self.path_to_project = None
        self.short_name = short_name

    def get_all_project_info(self) -> dict:
        all_projects = {}
        for i in range(self.acad.si.NumCustomInfo()):
            key = self.acad.si.GetCustomByIndex(i)[0]
            value = self.acad.si.GetCustomByIndex(i)[1]
            all_projects[key] = value
        return all_projects

    # TODO: Нужно переписать - перенести в Автокад
    #  и сделать для выбраного файла

    def write_user_property(self, key: str, value: str) -> None:
        opened_drawings = [drawing for drawing in self.acad.docs]
        for drawing in opened_drawings:
            self.acad.add_user_property_to_drawing(drawing, key, value)

    def write_all_property(self, **kwargs) -> None:
        opened_drawings = [drawing for drawing in self.acad.docs]
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
        for file_path in project_files_path:
            opened_files = [doc.FullName for doc in self.acad.docs]
            if file_path not in opened_files:
                self.acad.open_dwg(file_path)
        self.write_template_user_property()

    def remove_property(self, property_name: str) -> None:
        self.acad.doc.SummaryInfo.RemoveCustomByKey(property_name)

    # TODO: Нужно чтобы открывались все чертежи проекта
    #  и из них удалялось свойство

    def remove_all_property(self) -> None:
        for _ in range(self.acad.doc.SummaryInfo.NumCustomInfo()):
            self.acad.doc.SummaryInfo.RemoveCustomByIndex(0)

    # TODO: Нужно чтобы открывались все чертежи проекта и из них
    #  удалялось свойство

    def write_template_user_property(self) -> None:
        self.write_all_property(**self.property_template)

    @staticmethod
    def choose_path_for_project() -> str:
        return easygui.diropenbox(title="Виберіть місце для нового проекту")

    def create_project_folder_with_template(
            self,
            path_to_project: str | None = None
    ) -> None:

        app_directory = os.path.dirname(
            os.path.dirname(
                os.path.abspath(__file__)
            )
        )
        path_to_template = os.path.join(
            app_directory,
            "files", "dwg_template", "project_water_sewerage"
        )
        self.short_name = self.short_name.title()

        if self.path_to_project is None:
            path_to_project = easygui.diropenbox(
                title="Виберіть місце для нового проекту"
            )
        self.path_to_project = os.path.join(path_to_project, self.short_name)

        copytree(path_to_template, self.path_to_project, dirs_exist_ok=True)

        self.rename_file_dwg_for_new_project(path_to_project)

    @staticmethod
    def path_to_all_dwg_project_files(path_to_project: str) -> list:
        dwg_files: list[str] = []
        for root, dirs, files in os.walk(path_to_project):
            for file in files:
                if file.endswith(".dwg"):
                    dwg_files.append(os.path.join(root, file))
        return dwg_files

    def rename_file_dwg_for_new_project(self, path_to_project: str) -> None:
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
        os.startfile(path_to_project)

    def take_from_user_project_info(self) -> None:
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
