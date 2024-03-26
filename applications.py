from app.services.project_info import Project


class App:
    pass


class ProjectApp(App):
    commands = {
        "1": "створити",
        "0": "exit",
    }

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

    def print_error_massage_wrong_command(self):
        print("-" * 48)
        print("\033[1;31mВи ввели не коректну команду. "
              "Допустимі команди:\033[0m")
        for key, value in self.commands.items():
            print(f"[{key}] {value.title()}")
        print("-" * 48)

    def create_new_project(self):
        short_name = input("\033[1mВведіть коротку назву:\033[0m ").lower()

        project = Project(short_name)
        project.create_project_folder_with_template()

    def user_action(self):
        self.print_start_massage()

        while True:
            commands_list = ([key for key, value in self.commands.items()]
                             + [value for key, value in self.commands.items()])
            command = input("\033[1mВведіть команду:\033[0m ").lower()
            if command not in commands_list:
                self.print_error_massage_wrong_command()

            if command == "1" or command == "створити":
                self.create_new_project()

            if command == "0" or command == "exit":
                break


ProjectApp()
