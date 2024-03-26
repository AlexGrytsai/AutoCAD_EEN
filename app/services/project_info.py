import os
from shutil import copytree

import easygui

from app.autocad import Autocad


class Project:
    acad = Autocad()

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

    def __init__(self, short_name: str) -> None:
        self.short_name = short_name

    def get_all_project_info(self) -> dict:
        all_projects = {}
        for i in range(self.acad.si.NumCustomInfo()):
            key = self.acad.si.GetCustomByIndex(i)[0]
            value = self.acad.si.GetCustomByIndex(i)[1]
            all_projects[key] = value
        return all_projects

    def get_project_info_by_key(self, key: str) -> str | bool:
        try:
            return self.acad.si.GetCustomByKey(key)
        except Exception:
            return False

    def write_user_property(self, key: str, value: str) -> None:
        self.acad.doc.SummaryInfo.AddCustomInfo(key, value)

    def write_all_property(self, **kwargs) -> None:
        for key, value in kwargs.items():
            if not self.get_project_info_by_key(key):
                self.write_user_property(key, value)
            else:
                self.update_property_value(key, value)

    def remove_property(self, property_name: str) -> None:
        self.acad.doc.SummaryInfo.RemoveCustomByKey(property_name)

    def remove_all_property(self) -> None:
        for _ in range(self.acad.doc.SummaryInfo.NumCustomInfo()):
            self.acad.doc.SummaryInfo.RemoveCustomByIndex(0)

    def update_property_value(
            self,
            key: str,
            value: str
    ) -> None:
        self.acad.doc.SummaryInfo.SetCustomByKey(key, value)

    def make_template_user_property(self) -> None:
        self.write_all_property(**self.property_template)

    def create_project_folder_with_template(self) -> None:
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

        path_to_project = easygui.diropenbox(
            title="Виберіть місце для нового проекту"
        )

        path_to_project = os.path.join(path_to_project, self.short_name)

        copytree(path_to_template, path_to_project, dirs_exist_ok=True)

    def rename_file_dwg(self) -> None:
        pass

    def take_project_info(self) -> None:
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

    def take_manual_user_property(self) -> None:
        pass

    def make_template_project_info(
            self,
            project_files_path: list[str]
    ) -> None:
        for file_path in project_files_path:
            self.acad.open_dwg(file_path)
            self.make_template_user_property()
            self.acad.close_and_save_dwg(file_path)
        self.acad.close_acad()
