import os.path
import tkinter as tk
from tkinter import Toplevel
from tkinter import messagebox
from tkinter import ttk

from app.services.project_info import Project


class ProjectGUI:
    def __init__(self, root: tk.Tk) -> None:
        self.project = Project()

        self.project_property_window = tk.Toplevel(root)
        self.project_property_window.title("Дані об'єкта")

        icon = tk.PhotoImage(file="app/files/Theme/auto-cad.png")
        self.project_property_window.iconphoto(False, icon)

        self.project_property_window.grab_set()


class CreateProjectGUI(ProjectGUI):
    def __init__(self, root: tk.Tk) -> None:
        super().__init__(root=root)

        self.short_name_project = None
        self.path_to_folder = None
        self.key_value_properties = None

    def create_project_window(self) -> None:
        self.short_name_project = self.create_fill_short_name()

        self.path_to_folder = self.create_fill_path_for_project()
        self.btn_path_to_folder(self.path_to_folder)

        self.key_value_properties = self.create_fill_for_properties()
        self.btn_create_project()
        self.btn_cancel_create()

        self.project_property_window.update_idletasks()

    def create_fill_short_name(self) -> tk.Entry:
        tk.Label(
            self.project_property_window,
            text="Коротка назва об'єкта"
        ).grid(row=0, column=0)

        short_name_project_var = tk.StringVar()

        short_name_entry_widget = tk.Entry(
            self.project_property_window, bg="white",
            width=30,
            borderwidth=2,
            textvariable=short_name_project_var,
            justify="center",
        )
        short_name_entry_widget.grid(row=0, column=1)

        return short_name_entry_widget

    def create_fill_path_for_project(self) -> tk.Entry:

        path_to_folder_project_var = tk.StringVar()

        path_to_folder_project = tk.Entry(
            self.project_property_window, bg="white",
            width=30,
            borderwidth=2,
            textvariable=path_to_folder_project_var,
            justify="center",
        )
        path_to_folder_project.grid(row=1, column=1)

        return path_to_folder_project

    def btn_path_to_folder(self, path_to_folder_project: tk.Entry) -> None:
        def get_path_to_folder() -> None:
            path_to_folder = self.project.choose_path_for_project()

            path_to_folder_project.insert(0, path_to_folder)

        ttk.Button(
            self.project_property_window,
            text="Вибрати",
            command=get_path_to_folder
        ).grid(row=1, column=0, padx=5, pady=5)

    def create_fill_for_properties(self) -> list[tuple[tk.Entry, tk.Entry]]:
        key_property = [key for key in self.project.property_template]
        value_property = [
            value for value in self.project.property_template.values()
        ]

        entry_key_value_properties = []

        for i in range(len(key_property)):
            name_property_var = tk.StringVar()
            value_property_var = tk.StringVar()

            entry_key_property = tk.Entry(
                self.project_property_window, bg="white",
                width=25,
                borderwidth=2,
                textvariable=name_property_var,
                justify="center",
            )

            entry_value_property = tk.Entry(
                self.project_property_window, bg="white",
                width=30,
                borderwidth=2,
                textvariable=value_property_var,
                justify="center",
            )

            entry_key_value_properties.append(
                (entry_key_property, entry_value_property)
            )

            entry_key_property.grid(row=i + 2, column=0, padx=5, pady=5)
            entry_value_property.grid(row=i + 2, column=1, padx=5, pady=5)

            entry_key_property.bind(
                "<FocusIn>",
                lambda event, entry=entry_key_property:
                self.clear_text_in_entry(entry, key_property)
            )

            entry_value_property.bind(
                "<FocusIn>",
                lambda event, entry=entry_value_property:
                self.clear_text_in_entry(entry, value_property)
            )

        for i in range(len(key_property)):
            entry_key_property = entry_key_value_properties[i][0]
            entry_value_property = entry_key_value_properties[i][1]

            entry_key_property.insert(0, string=key_property[i])
            entry_value_property.insert(0, string=value_property[i])

            entry_key_property.configure(state="disabled")

        return entry_key_value_properties

    def btn_create_project(self) -> None:
        ttk.Button(
            self.project_property_window,
            text="Ok",
            command=self.create_new_project
        ).grid(row=30, column=0, padx=10, pady=10)

    def btn_cancel_create(self) -> None:
        def cancel_create() -> None:
            self.project_property_window.destroy()

        ttk.Button(
            self.project_property_window,
            text="Cancel",
            command=cancel_create
        ).grid(row=30, column=1, padx=10, pady=10)

    @staticmethod
    def clear_text_in_entry(
            entry: tk.Entry,
            template_list_property: list[str]
    ) -> None:
        if entry.get() in template_list_property:
            entry.delete(0, tk.END)

    def get_all_user_properties(self) -> None:
        user_properties = {}
        for property in self.key_value_properties:
            key, value = property
            user_properties[key.get()] = value.get()
        self.project.property_template = user_properties

    def check_required_fields(self) -> bool:
        if self.short_name_project.get() and self.path_to_folder.get():
            return True
        return False

    def message_window_creating_project(
            self,
            title: str,
            message: str
    ) -> Toplevel:
        message_window = tk.Toplevel(self.project_property_window)
        message_window.title(title)

        icon = tk.PhotoImage(file="app/files/Theme/auto-cad.png")
        message_window.iconphoto(False, icon)

        message_window.resizable(width=False, height=False)
        message_window.update_idletasks()

        message_text = tk.Label(
            message_window,
            text=message,
            justify="center"
        )
        message_text.grid(row=0, column=0, padx=10, pady=10)

        return message_window

    def create_new_project(self) -> None:
        if self.check_required_fields():
            message = self.message_window_creating_project(
                title="Створюється проект",
                message="Створюється проект.\n"
                        "Це може зайняти декілька хвилин.\n"
                        "Не вимикайте комп'ютер та не закривайте программу!"
            )
            message.grab_set()
            message.update()

            self.project.short_name = self.short_name_project.get()
            self.get_all_user_properties()
            self.project.create_project_folder_with_template_dwg(
                self.path_to_folder.get()
            )

            dwg_files = self.project.path_to_all_dwg_project_files(
                self.project.path_to_project
            )
            self.project.write_template_project_info(dwg_files)

            self.project.add_json_info_file_project()

            self.project.open_project_folder(self.project.path_to_project)

            message.destroy()
            self.project_property_window.destroy()

        else:
            messagebox.showwarning(
                title="Помилка",
                message="Необхідно заповнити всі обов'язкові поля"
            )


class OpenProjectGUI(CreateProjectGUI):
    def __init__(self, root: tk.Tk) -> None:
        super().__init__(root)

        self.project.open_exist_project()

    def create_project_window(self) -> None:
        short_name_project = self.create_fill_short_name()
        short_name_project.insert(
            0, os.path.basename(
                os.path.normpath(self.project.path_to_project)
            )
        )
        short_name_project.configure(state="disabled")

        self.label_path_to_project()
        path_to_folder = self.create_fill_path_for_project()
        path_to_folder.insert(0, self.project.path_to_project)

        self.key_value_properties = self.create_fill_for_properties()
        self.unbind_entry_value_properties()

        self.project_property_window.update_idletasks()

        self.btn_cancel_create()

    def unbind_entry_value_properties(self) -> None:
        for property in self.key_value_properties:
            key, value = property
            value.unbind("<FocusIn>")

    def label_path_to_project(self) -> None:
        tk.Label(
            self.project_property_window, text="Розташування проекту"
        ).grid(row=1, column=0, padx=10, pady=10)