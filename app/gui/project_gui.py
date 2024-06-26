import os.path
import tkinter as tk
from tkinter import Toplevel
from tkinter import messagebox
from tkinter import ttk
from tkinter.ttk import Button

from app.services.project_info import Project


class ProjectGUI:
    def __init__(self, root: tk.Tk) -> None:
        self.project = Project()

        self.project_property_window = tk.Toplevel(root)
        self.project_property_window.title("Дані проекта")

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
        """
        Creates the project window and initializes the necessary components.
        This function is responsible for creating the project window and
        initializing the required components for the project.
        Parameters:
            self (CreateProjectGUI): The instance of the `CreateProjectGUI` class.
        Returns:
            None
        """
        self.short_name_project = self.create_fill_short_name()

        self.path_to_folder = self.create_fill_path_for_project()
        self.btn_path_to_folder(self.path_to_folder)

        self.key_value_properties = self.create_fill_for_properties()
        self.btn_create_project()
        self.btn_cancel_create()

        self.project_property_window.update_idletasks()

    def create_fill_short_name(self) -> tk.Entry:
        """
        Creates a tkinter Entry widget for the short name of an object
        and returns it.

        :return: A tkinter Entry widget for the short name of an object.
        :rtype: tk.Entry
        """

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
        """
        Creates a tkinter Entry widget for the path to the project folder
        and returns it.

        :return: A tkinter Entry widget for the path to the project folder.
        :rtype: tk.Entry
        """

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
        """
        Creates a button that, when clicked, retrieves the path to a folder
        and inserts it into the provided tk.Entry widget.

        :param path_to_folder_project: A tk.Entry widget to insert the path
        to the folder.
        :type path_to_folder_project: tk.Entry
        :return: None
        :rtype: None
        """
        def get_path_to_folder() -> None:
            path_to_folder = self.project.choose_path_for_project()

            path_to_folder_project.insert(0, path_to_folder)

        ttk.Button(
            self.project_property_window,
            text="Вибрати",
            command=get_path_to_folder,
            style="Accent.TButton"
        ).grid(row=1, column=0, padx=5, pady=5)

    def create_fill_for_properties(self) -> list[tuple[tk.Entry, tk.Entry]]:
        """
        Creates and configures tkinter Entry widgets for the key-value
        properties of the project.

        :return: A list of tuples containing the Entry widgets for the key
        and value properties.
        :rtype: list[tuple[tk.Entry, tk.Entry]]
        """
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

    def btn_create_project(self) -> Button:
        """
        Creates a button that, when clicked, triggers the creation of a new project.

        :return: The created button widget.
        :rtype: Button
        """
        btn_create_project = ttk.Button(
            self.project_property_window,
            text="Створити",
            command=self.create_new_project,
            style="Accent.TButton"
        )
        btn_create_project.grid(row=30, column=1, padx=10, pady=10)

        return btn_create_project

    def btn_cancel_create(self) -> None:
        def cancel_create() -> None:
            self.project_property_window.destroy()

        ttk.Button(
            self.project_property_window,
            text="Скасувати",
            command=cancel_create,
        ).grid(row=30, column=0, padx=10, pady=10)

    @staticmethod
    def clear_text_in_entry(
            entry: tk.Entry,
            template_list_property: list[str]
    ) -> None:
        """
        Clears the text in the given tkinter Entry widget if it matches any
        of the strings in the provided list.

        :param entry: The tkinter Entry widget to clear the text from.
        :type entry: tk.Entry
        :param template_list_property: A list of strings to check against the
        text in the Entry widget.
        :type template_list_property: list[str]
        :return: None
        :rtype: None
        """
        if entry.get() in template_list_property:
            entry.delete(0, tk.END)

    def get_all_user_properties(self) -> dict[str, str]:
        """
        A function that retrieves all user properties from the key-value
        properties.

        Returns:
            dict[str, str]: A dictionary containing the user properties.
        """
        user_properties = {}
        for property in self.key_value_properties:
            key, value = property
            user_properties[key.get()] = value.get()
        return user_properties

    def check_required_fields(self) -> bool:
        """
        Check if both the short name project and the path to the folder
        have values.

        Returns:
            bool: True if both short name project and path to the folder
            have values, False otherwise.
        """
        if self.short_name_project.get() and self.path_to_folder.get():
            return True
        return False

    def message_window(
            self,
            title: str,
            message: str
    ) -> Toplevel:
        """
        Creates a new message window with the given title and message.

        :param title: The title of the message window.
        :type title: str
        :param message: The message to be displayed in the message window.
        :type message: str
        :return: The newly created message window.
        :rtype: Toplevel
        """

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
        """
        A function that creates a new project, populates the necessary project
        details, creates the project folder with a template DWG file, writes
        project information, adds a JSON info file, and opens the project
        folder. If required fields are not filled, it shows a warning message.
        """

        if self.check_required_fields():
            message = self.message_window(
                title="Створюється проект",
                message="Створюється проект.\n"
                        "Це може зайняти декілька хвилин.\n"
                        "Не вимикайте комп'ютер та не закривайте программу!"
            )
            message.grab_set()
            message.update()

            self.project.short_name = self.short_name_project.get()
            self.project.property_template = self.get_all_user_properties()

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
    """
    This class represents the GUI for opening an existing project.
    It inherits from the CreateProjectGUI class.
    """
    def __init__(self, root: tk.Tk) -> None:
        super().__init__(root)

        self.project.open_exist_project()

    def create_project_window(self) -> None:
        """
        Creates the project window and initializes the necessary components.
        This function is responsible for creating the project window and
        initializing the required components for the project.
        """

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

        btn_rewrite_property = self.btn_create_project()
        btn_rewrite_property.configure(
            text="Змінити",
            command=self.rewrite_properties
        )

    def unbind_entry_value_properties(self) -> None:
        """
        Unbinds the "<FocusIn>" event from the value Entry widgets in the
        key-value properties.
        This function iterates over each key-value property in
        `self.key_value_properties` and unbinds the "<FocusIn>" event from
        the value Entry widget. This is done by calling the `unbind` method on
        the value Entry widget and passing "<FocusIn>" as the event to unbind.
        """

        for property in self.key_value_properties:
            key, value = property
            value.unbind("<FocusIn>")

    def label_path_to_project(self) -> None:
        """
        Creates a tkinter Label widget with the text "Розташування проекту" and
        grids it in the project property window at row 1, column 0 with
        10 pixels of padding on the x-axis and y-axis.
        """

        tk.Label(
            self.project_property_window, text="Розташування проекту"
        ).grid(row=1, column=0, padx=10, pady=10)

    def rewrite_properties(self) -> None:
        """
        This function checks if the new user properties are different from
        the existing project properties. If they are different, it displays
        a message to the user and updates the project properties.
        It then updates the project information in all the DWG files,
        adds a JSON info file to the project, and closes the project property
        window. If the new properties are the same as the existing properties,
        it displays an info message to the user.
        """

        new_properties = self.get_all_user_properties()
        if new_properties != self.project.property_template:
            message = self.message_window(
                title="Зміна данних проекту",
                message="Змінюються дані проекту.\n"
                        "Це може зайняти декілька хвилин.\n"
                        "Не вимикайте комп'ютер та не закривайте программу!"
            )
            message.grab_set()
            message.update()

            self.project.property_template = new_properties

            dwg_files = self.project.path_to_all_dwg_project_files(
                self.project.path_to_project
            )
            self.project.write_template_project_info(dwg_files)

            self.project.add_json_info_file_project()

            message.destroy()
            self.project_property_window.destroy()
        else:
            messagebox.showinfo(title="Info",
                                message="Ви не внесли жодних змін.")
