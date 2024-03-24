from win32com.client import Dispatch


class Autocad:
    acad = Dispatch("AutoCAD.Application")
    doc = acad.ActiveDocument
    db = doc.Database
    si = db.SummaryInfo

    def open_dwg(self, address_file: str) -> None:
        if address_file != self.acad.ActiveDocument.FullName:
            if self.acad.Preferences.System.SingleDocumentMode:
                self.acad.ActiveDocument.Open(address_file)
            else:
                self.acad.Documents.Open(address_file)

    def close_and_save_dwg(self, address_file: str) -> None:
        for doc in self.acad.Documents:
            if doc.FullName == address_file:
                doc.Close()
                return

    def close_acad(self) -> None:
        self.acad.Quit()


Autocad().open_dwg("D:\\Python\\MY PROJECTS\\AutoCAD_EEN\\Чертеж4.dwg")
Autocad().close_and_save_dwg("D:\\Python\\MY PROJECTS\\AutoCAD_EEN\\Чертеж4.dwg")
Autocad().close_acad()
