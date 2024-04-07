import tkinter as tk
from tkinter import ttk

from app.services.project_info import Project


class CreateProjectGUI:
    def __init__(self, root: tk.Tk) -> None:
        self.project = Project()

        self.add_name_project_window = tk.Toplevel(root)
        self.add_name_project_window.title("Введіть назву об'єкта")
        self.add_name_project_window.geometry("400x250")

        tk.Label(
            self.add_name_project_window,
            text="Коротка назва об'єкта"
        ).grid(row=0, column=0)

        short_name_project_var = tk.StringVar()

        def get_short_name() -> None:
            self.project.short_name = short_name_project_var.get()
            # self.project.create_project_folder_with_template()
            # self.add_name_project_window.destroy()

        short_name_entry_widget = tk.Entry(
            self.add_name_project_window, bg="white",
            width=30,
            borderwidth=2,
            textvariable=short_name_project_var,
            justify="center",
        )
        short_name_entry_widget.grid(row=0, column=1)

        tk.Label(
            self.add_name_project_window,
            text="Місце розташування"
        ).grid(row=1, column=0)

        path_to_folder_project_var = tk.StringVar()

        path_to_folder_project = tk.Entry(
            self.add_name_project_window, bg="white",
            width=30,
            borderwidth=2,
            textvariable=path_to_folder_project_var,
            justify="center",
        )
        path_to_folder_project.grid(row=1, column=1)

        def get_path_to_folder() -> None:
            path_to_folder = self.project.choose_path_for_project()
            path_to_folder_project.insert(0, path_to_folder)

        tk.Button(
            self.add_name_project_window,
            text="Вибрати",
            command=get_path_to_folder
        ).grid(row=1, column=2)

        self.create_fill_for_properties()

    def create_fill_for_properties(self) -> None:
        key_property = [key for key in self.project.property_template]
        name_and_value_project_properties_list = []

        for i in range(len(key_property)):
            name_property_var = tk.StringVar()
            value_property_var = tk.StringVar()

            name_property = tk.Entry(
                self.add_name_project_window, bg="white",
                width=25,
                borderwidth=2,
                textvariable=name_property_var,
                justify="center",
            )

            value_property = tk.Entry(
                self.add_name_project_window, bg="white",
                width=30,
                borderwidth=2,
                textvariable=value_property_var,
                justify="center",
            )

            name_and_value_project_properties_list.append(
                (name_property, value_property)
            )

            name_property.grid(row=i + 2, column=0)
            value_property.grid(row=i + 2, column=1)

        for i in range(len(key_property)):
            property = name_and_value_project_properties_list[i][0]
            property.insert(0, key_property[i])
            property.configure(state="disabled")




        tk.Button(
            self.add_name_project_window,
            text="Створити",
            command="get_short_name"
        ).grid(row=30, column=1)
