from app.autocad import Autocad


class ProjectInfo:
    acad = Autocad()

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
        property_template = {
            "Назва об'єкту": "PROJECT NAME",
            "Розділ проекту": "PROJECT TITLE NETWORK",
            "Стадія проектування": "STAGE PROJECT",
            "ТУ В1": "NUMBER TR WATER",
            "ТУ К1": "NUMBER OF TR SIGNATORY",
            "ТУ К2": "NUMBER OF TR RAIN SEWERAGE",
            "Проектна організація": "AUTHOR PROJECT",
            "ГІП": "CHIEF PROJECT ENGINEER",
            "Розробив": "NAME DESIGNER",
            "Замовник": "CUSTOMER NAME",
            "Представник Водоканалу": "SIGNATORY PROJECT",
            "Посада представника": "JOB TITLE SIGNATORY",
            "ID Проекту": "PROJECT ID",
        }
        self.write_all_property(**property_template)
