import tkinter as tk
from tkinter import ttk

from app.gui.create_project_gui import CreateProjectGUI


class AppGUI:
    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title("AutoCAD External engineering networks")
        self.root.geometry("600x200")

        self.frame_with_actions()
        # self.frame_with_project_property()

        self.project = None

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
        CreateProjectGUI(self.root)



if __name__ == "__main__":
    AppGUI()
