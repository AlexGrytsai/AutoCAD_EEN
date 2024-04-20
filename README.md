# AutoCAD External engineering networks

## Overview
This project contains Python code for managing AutoCAD projects. It provides functionalities to create new projects, open existing projects, and manipulate project files within the AutoCAD environment. The code utilizes the `win32com` library for interacting with AutoCAD.

## Features
- **Create New Project**: Allows users to create a new AutoCAD project by specifying project name, location, and custom properties.
- **Open Existing Project**: Enables users to open an existing AutoCAD project, view its properties, and modify them if needed.
- **Manage Project Files**: Provides functionalities to manipulate project files, such as adding custom properties to DWG files and saving project information in JSON format.

## Dependencies
- Python 3.x
- `win32com` library for Windows automation
- `easygui` for GUI file dialogs

## Installation
1. Clone the repository to your local machine.
2. Install the required dependencies using `pip`:


## Usage
1. Run the `main.py` script to launch the application.
2. Choose the desired action from the project menu:
- **New Project**: Create a new AutoCAD project.
- **Open Project**: Open an existing AutoCAD project.

## File Structure
- `main.py`: Main script to run the application.
- `app/`:
- `services/`:
 - `autocad.py`: Contains classes for interacting with AutoCAD.
 - `project_info.py`: Contains the `Project` class for managing project information.
- `gui/`:
 - `project_gui.py`: Contains GUI classes for creating and opening projects.

## Contributing
Contributions are welcome! If you find any issues or have suggestions for improvements, feel free to open an issue or submit a pull request.

## License
This project is licensed under the MIT License - see the [LICENSE](./LICENSE) file for details.
