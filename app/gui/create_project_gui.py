import tkinter as tk

from app.services.project_info import Project


class CreateProjectGUI:
    def __init__(self, root: tk.Tk) -> None:
        self.project = Project()

        self.add_name_project_window = tk.Toplevel(root)
        self.add_name_project_window.title("Введіть дані об'єкта")
        self.add_name_project_window.geometry("400x250")

        self.short_name_project = self.create_fill_short_name()
        self.path_to_folder = self.create_fill_path_for_project()

        self.key_value_properties = self.create_fill_for_properties()

    def create_fill_short_name(self) -> tk.Entry:
        tk.Label(
            self.add_name_project_window,
            text="Коротка назва об'єкта"
        ).grid(row=0, column=0)

        short_name_project_var = tk.StringVar()

        short_name_entry_widget = tk.Entry(
            self.add_name_project_window, bg="white",
            width=30,
            borderwidth=2,
            textvariable=short_name_project_var,
            justify="center",
        )
        short_name_entry_widget.grid(row=0, column=1)

        return short_name_entry_widget

    def create_fill_path_for_project(self) -> tk.Entry:
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

        return path_to_folder_project

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
                self.add_name_project_window, bg="white",
                width=25,
                borderwidth=2,
                textvariable=name_property_var,
                justify="center",
            )

            entry_value_property = tk.Entry(
                self.add_name_project_window, bg="white",
                width=30,
                borderwidth=2,
                textvariable=value_property_var,
                justify="center",
            )

            entry_key_value_properties.append(
                (entry_key_property, entry_value_property)
            )

            entry_key_property.grid(row=i + 2, column=0)
            entry_value_property.grid(row=i + 2, column=1)

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

        tk.Button(
            self.add_name_project_window,
            text="Створити",
            command=self.create_new_project
        ).grid(row=30, column=1)

        return entry_key_value_properties

    @staticmethod
    def clear_text_in_entry(
            entry: tk.Entry,
            template_list_property: list[str]
    ) -> None:
        if entry.get() in template_list_property:
            entry.delete(0, tk.END)

    def create_new_project(self) -> None:
        if self.short_name_project:
            self.project.short_name = self.short_name_project.get()
            print(self.project.short_name)
        #TODO: Нужно сделать проверки, что бы было заполнены шорт имя и выбран путь
