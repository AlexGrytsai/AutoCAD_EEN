import win32com
from win32com.client import Dispatch
from win32com.client import CDispatch


class Autocad:
    """
    This class represents an AutoCAD application and provides methods to
    interact with it.
    """
    acad = Dispatch("AutoCAD.Application")  # Initialize AutoCAD application
    doc = acad.ActiveDocument  # Get the active document
    model = doc.ModelSpace  # Get the model space
    docs = acad.Documents  # Get all the documents
    db = acad.ActiveDocument.Database  # Get the active document's database
    si = db.SummaryInfo  # Get the summary info of the active document's database

    @staticmethod
    def check_install_autocad() -> bool:
        """
        Check if AutoCAD is installed on the system.
        Returns:
        bool: True if AutoCAD is installed, False otherwise.
        """
        try:
            win32com.client.Dispatch("AutoCAD.Application")
            return True
        except Exception:
            return False

    def open_dwg(self, address_file: str) -> None:
        """
        Open a DWG file.
        Args:
        address_file (str): The path to the DWG file.
        """
        if self.acad.Preferences.System.SingleDocumentMode:
            self.acad.ActiveDocument.Open(address_file)
        else:
            self.acad.Documents.Open(address_file)

    @staticmethod
    def quick_save_dwg(drawing: CDispatch) -> None:
        """
        Quick save the drawing.
        Args:
        drawing (CDispatch): The drawing to be saved.
        """
        drawing.SendCommand("_qsave ")

    @staticmethod
    def close_dwg(drawing: CDispatch) -> None:
        """
        Close the drawing.
        Args:
        drawing (CDispatch): The drawing to be closed.
        """
        drawing.Close(False)
        drawing.Close(False)

    def close_acad(self) -> None:
        """
        Close the AutoCAD application.
        """
        self.acad.Quit()

    @staticmethod
    def update_user_property_drawing_value(
            drawing: CDispatch,
            key: str,
            value: str
    ) -> None:
        """
       Update the value of a custom property in the drawing's summary info.

       Args:
       drawing (CDispatch): The drawing to update.
       key (str): The key of the custom property.
       value (str): The new value of the custom property.
       """
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
        """
        Get the value of a custom property from the drawing's summary info.

        Args:
        drawing (CDispatch): The drawing to get the property from.
        key (str): The key of the custom property.

        Returns:
        str | bool: The value of the custom property if it exists, False otherwise.
        """
        if not self.get_user_property_from_drawing_by_key(drawing, key):
            drawing.SummaryInfo.AddCustomInfo(key, value)
        else:
            self.update_user_property_drawing_value(drawing, key, value)

    @staticmethod
    def remove_user_property_from_drawing(
            drawing: CDispatch,
            property_name: str
    ) -> None:
        """
        Add a custom property to the drawing's summary info.

        Args:
        drawing (CDispatch): The drawing to add the property to.
        key (str): The key of the custom property.
        value (str): The value of the custom property.
        """
        drawing.SummaryInfo.RemoveCustomByKey(property_name)


class AutocadGeneralPlane(Autocad):

    def select_object(self):
        obj = self.model.Object.SelectOnScreen
        print(obj)
