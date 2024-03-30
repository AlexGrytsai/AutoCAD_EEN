from app.services.project_info import Project


class App:
    pass


class ProjectApp(App):

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

    def print_error_massage_wrong_command(self, commands: dict) -> None:
        print("-" * 48)
        print("\033[1;31mВи ввели не коректну команду. "
              "Допустимі команди:\033[0m")
        self.create_command_menu(commands)
        print("-" * 48)

    @staticmethod
    def create_command_list(commands: dict) -> list:
        return ([key for key, value in commands.items()]
                + [value for key, value in commands.items()])

    @staticmethod
    def create_command_menu(commands: dict) -> None:
        for key, value in commands.items():
            print(f"\033[1m[{key}]:\033[0m {value.title()}")

    def create_new_project(self):
        short_name = input("\033[1mВведіть коротку назву:\033[0m ").lower()

        project = Project(short_name)
        project.create_project_folder_with_template()

        commands = {
            "0": "так",
            "1": "ні",
        }

        print("-" * 48)
        print("Заповнити дані проекту?")
        self.create_command_menu(commands)
        command = input("\033[1mВведіть команду:\033[0m ").lower()
        while True:
            if command not in self.create_command_list(commands):
                while True:
                    self.print_error_massage_wrong_command(commands)
                    command = input("\033[1mВведіть команду:\033[0m ").lower()
                    if command in self.create_command_list(commands):
                        break
            if command in ("0", "так"):
                project.take_from_user_project_info()
            dwg_files = project.path_to_all_dwg_project_files(
                project.path_to_project
            )

            print("Зачекайте, створюється проект. Це може зайняти 1-2хв.")

            project.write_template_project_info(dwg_files)
            project.open_project_folder(project.path_to_project)
            break

    def user_action(self):
        self.print_start_massage()

        commands = {
            "1": "створити",
            "0": "exit",
        }

        while True:
            command = input("\033[1mВведіть команду:\033[0m ").lower()
            if command not in self.create_command_list(commands):
                self.print_error_massage_wrong_command(commands)

            if command in ("1", "створити"):
                self.create_new_project()
                break

            if command in ("0", "exit"):
                break
