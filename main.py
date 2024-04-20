# AutoCAD External engineering networks
from tkinter.messagebox import showerror

from app.gui.applications import AppGUI
from app.services.autocad import Autocad


def main():
    """
    This function checks if AutoCAD is installed on the system and runs the GUI application if it is.
    """

    if Autocad.check_install_autocad():
        AppGUI()
    else:
        showerror(
            "Error",
            "AutoCAD is not installed on your system."
        )


if __name__ == '__main__':
    main()
