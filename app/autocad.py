from win32com.client import Dispatch


class Autocad:
    acad = Dispatch("AutoCAD.Application")
    doc = acad.ActiveDocument
    db = doc.Database
    si = db.SummaryInfo
