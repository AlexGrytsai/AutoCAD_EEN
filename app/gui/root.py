import tkinter as tk
from tkinter import ttk

from app.services.project_info import Project


class AppGUI:
    def __init__(self) -> None:
        self.project = Project()

        self.root = tk.Tk()
        self.root.title("AutoCAD External engineering networks")
        self.root.geometry("400x200")

        self.frame_with_actions()
        self.frame_with_project_property()

        self.root.mainloop()

    def frame_with_actions(self) -> None:
        label_frame_actions_with_project = tk.LabelFrame(
            self.root,
            text="Дії з проектом"
        )
        btb_create_project = ttk.Button(
            label_frame_actions_with_project,
            text="Новий проект",
            command=self.command_create_project
        )
        btb_create_project.pack()

        label_frame_actions_with_project.grid(row=0, column=0)

    def frame_with_project_property(self) -> None:
        label_frame_project_properties = tk.LabelFrame(
            self.root,
            text="Дані проекту"
        )
        label_2 = ttk.Label(label_frame_project_properties, text="Label 2",
                            width=50)

        label_2.pack()

        label_frame_project_properties.grid(row=0, column=1)

    def command_create_project(self) -> None:
        add_name_project_window = tk.Toplevel(self.root)
        add_name_project_window.title("Введіть назву об'єкта")
        add_name_project_window.geometry("250x200")

        tk.Label(
            add_name_project_window,
            text="Введіть коротку назву об'єкта\n\n"
                 "(наприклад: Жовтнева, Перемоги)\n"
                 "За цим ім'ям буде створена папка проекту."
        ).pack()

        short_name_project_var = tk.StringVar()

        def short_name() -> None:
            self.project.short_name = short_name_project_var.get()
            self.project.create_project_folder_with_template()
            add_name_project_window.destroy()

        tk.Entry(
            add_name_project_window,
            textvariable=short_name_project_var
        ).pack()

        tk.Button(
            add_name_project_window,
            text="Ok",
            command=short_name
        ).pack()


if __name__ == "__main__":
    AppGUI()
