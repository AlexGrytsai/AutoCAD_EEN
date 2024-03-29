from win32com.client import Dispatch
from win32com.client import CDispatch


class Autocad:
    acad = Dispatch("AutoCAD.Application")
    doc = acad.ActiveDocument
    docs = acad.Documents
    db = acad.ActiveDocument.Database
    si = db.SummaryInfo

    def open_dwg(self, address_file: str) -> None:
        if self.acad.Preferences.System.SingleDocumentMode:
            self.acad.ActiveDocument.Open(address_file)
        else:
            self.acad.Documents.Open(address_file)

    @staticmethod
    def esc_command(drawing: CDispatch) -> None:
        drawing.PostCommand("_commandline")

    @staticmethod
    def quick_save_dwg(drawing: CDispatch) -> None:
        drawing.SendCommand("_qsave ")

    @staticmethod
    def close_dwg(drawing: CDispatch) -> None:
        drawing.Close(False)

    def close_acad(self) -> None:
        self.acad.Quit()

    @staticmethod
    def update_user_property_drawing_value(
            drawing: CDispatch,
            key: str,
            value: str
    ) -> None:
        drawing.SummaryInfo.SetCustomByKey(key, value)

    @staticmethod
    def get_user_property_from_drawing_by_key(
            drawing: CDispatch,
            key: str
    ) -> str | bool:
        try:
            return drawing.Database.SummaryInfo.GetCustomByKey(key)
        except Exception:
            return False

    def add_user_property_to_drawing(
            self,
            drawing: CDispatch,
            key: str,
            value: str
    ) -> None:
        if not self.get_user_property_from_drawing_by_key(drawing, key):
            drawing.SummaryInfo.AddCustomInfo(key, value)
        else:
            self.update_user_property_drawing_value(drawing, key, value)

    @staticmethod
    def remove_user_property(
            drawing: CDispatch,
            property_name: str
    ) -> None:
        drawing.SummaryInfo.RemoveCustomByKey(property_name)
