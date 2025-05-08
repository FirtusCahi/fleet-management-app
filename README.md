
Built by https://www.blackbox.ai

---

# Fleet Management Application

## Project Overview
The Fleet Management Application is designed to efficiently oversee and manage vehicles, drivers, and the expenses associated with fleet operations. This application is built using Python and incorporates a graphical user interface (GUI) through the Tkinter library, enabling users to perform database operations such as adding, updating, and retrieving information about vehicles, drivers, missions, and expenses.

## Installation
To get started with the Fleet Management Application, follow these steps to set up your environment:

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd fleet-management
   ```

2. **Install required dependencies:**
   Ensure that you have Python installed (Python 3.6 or above is recommended). You may also need to install the necessary packages. 

   Although no specific dependencies were listed in the project's `package.json`, do ensure you have `tkinter` and `sqlite3`, which are included with most Python installations. If you're using an environment manager like `virtualenv` or `conda`, make sure to activate it.

3. **Set up the database:**
   Upon launching the application, the database will be automatically created if it does not exist. You do not need to perform any manual database setup.

## Usage
To launch the application, run the `main.py` file. Here is how to do that:

```bash
python main.py
```

Once the application starts, you can interact with it through the GUI. Use the menus to manage vehicle assignments, drivers, expenses, and missions.

## Features
- **Vehicle Management:** Add, update, delete, and list vehicles.
- **Driver Management:** Manage driver records with their personal details and license status.
- **Expense Tracking:** Record different types of expenses related to vehicles, including fuel costs.
- **Mission Management:** Plan and track missions undertaken by drivers.
- **Vehicle Assignments:** Assign drivers to specific vehicles with tracking by date.
- **Alerts:** Receive notifications for vehicle revisions and driver license expiry dates.
- **Backup and Restore:** Save a backup of the database and restore it when necessary.
- **Language Support:** Supports multiple languages through external JSON files.

## Dependencies
While there are no specific dependencies mentioned for a `package.json`, the application utilizes the following libraries:
- `tkinter` (for GUI)
- `sqlite3` (for database operations)
- `json` (for language file management)
- `logging` (for error handling and logging)

Python's standard library includes these packages, so no additional installation is necessary.

## Project Structure
```plaintext
fleet-management/
├── __init__.py
├── main.py               # The main application entry point
├── db_utils.py           # Database utility functions
├── models.py             # Data models for vehicles, drivers, expenses, etc.
└── lang/
    └── translations/
        ├── ar.json       # Arabic language file
        └── fr.json       # French language file
```

Each key component of the application is structured in separate modules to maintain readability and modularity. The `models.py` file contains the data models needed for the application's core functionality, while `db_utils.py` handles all database interactions.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

This readme file provides a comprehensive guide to understanding, setting up, and using the Fleet Management Application effectively. Feel free to modify the content based on additional features or updates to the project.