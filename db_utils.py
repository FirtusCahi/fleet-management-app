import sqlite3
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

def create_tables(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS vehicles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                registration TEXT UNIQUE NOT NULL,
                make TEXT NOT NULL,
                model TEXT NOT NULL,
                year INTEGER,
                revision_date TEXT,
                control_date TEXT
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS drivers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                surname TEXT NOT NULL,
                license_number TEXT UNIQUE NOT NULL,
                expiry_date TEXT
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                vehicle_id INTEGER NOT NULL,
                date TEXT NOT NULL,
                type TEXT NOT NULL,
                amount REAL NOT NULL,
                description TEXT,
                mileage INTEGER,
                liters REAL,
                FOREIGN KEY (vehicle_id) REFERENCES vehicles(id)
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS missions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                driver_id INTEGER NOT NULL,
                start_date TEXT NOT NULL,
                end_date TEXT NOT NULL,
                destination TEXT NOT NULL,
                duration INTEGER,
                meals INTEGER,
                nights INTEGER,
                weekends INTEGER,
                FOREIGN KEY (driver_id) REFERENCES drivers(id)
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS vehicle_assignments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                vehicle_id INTEGER NOT NULL,
                driver_id INTEGER NOT NULL,
                assignment_date TEXT NOT NULL,
                FOREIGN KEY (vehicle_id) REFERENCES vehicles(id),
                FOREIGN KEY (driver_id) REFERENCES drivers(id),
                UNIQUE (vehicle_id, driver_id)
            )
        """)

        conn.commit()
        logger.info("Tables créées ou existantes.")
    except sqlite3.Error as e:
        logger.error(f"Erreur lors de la création des tables : {e}")
        if conn:
            conn.rollback()
    finally:
        if conn:
            conn.close()

# --- Fonctions pour les véhicules ---
def add_vehicle(db_file, registration, make, model, year, revision_date, control_date):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO vehicles (registration, make, model, year, revision_date, control_date)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (registration, make, model, year, revision_date, control_date))
        conn.commit()
        return cursor.lastrowid
    except sqlite3.IntegrityError:
        raise ValueError("L'immatriculation existe déjà.")
    except sqlite3.Error as e:
        logger.error(f"Erreur lors de l'ajout du véhicule : {e}")
        conn.rollback()
        raise

def get_vehicle(db_file, vehicle_id):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM vehicles WHERE id=?", (vehicle_id,))
    return cursor.fetchone()

def update_vehicle(db_file, vehicle_id, registration, make, model, year, revision_date, control_date):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    try:
        cursor.execute("""
            UPDATE vehicles SET registration=?, make=?, model=?, year=?, revision_date=?, control_date=?
            WHERE id=?
        """, (registration, make, model, year, revision_date, control_date, vehicle_id))
        conn.commit()
    except sqlite3.IntegrityError:
        raise ValueError("L'immatriculation existe déjà.")
    except sqlite3.Error as e:
        logger.error(f"Erreur lors de la mise à jour du véhicule : {e}")
        conn.rollback()
        raise

def delete_vehicle(db_file, vehicle_id):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM vehicles WHERE id=?", (vehicle_id,))
        conn.commit()
    except sqlite3.Error as e:
        logger.error(f"Erreur lors de la suppression du véhicule : {e}")
        conn.rollback()
        raise

def list_vehicles(db_file):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM vehicles")
    return cursor.fetchall()

def search_vehicles(db_file, query):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    search_term = f"%{query}%"
    cursor.execute("""
        SELECT * FROM vehicles
        WHERE registration LIKE ? OR make LIKE ? OR model LIKE ?
    """, (search_term, search_term, search_term))
    return cursor.fetchall()

# --- Fonctions pour les conducteurs ---
def add_driver(db_file, name, surname, license_number, expiry_date):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO drivers (name, surname, license_number, expiry_date)
            VALUES (?, ?, ?, ?)
        """, (name, surname, license_number, expiry_date))
        conn.commit()
        return cursor.lastrowid
    except sqlite3.IntegrityError:
        raise ValueError("Le numéro de permis existe déjà.")
    except sqlite3.Error as e:
        logger.error(f"Erreur lors de l'ajout du conducteur : {e}")
        conn.rollback()
        raise

def get_driver(db_file, driver_id):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM drivers WHERE id=?", (driver_id,))
    return cursor.fetchone()

def update_driver(db_file, driver_id, name, surname, license_number, expiry_date):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    try:
        cursor.execute("""
            UPDATE drivers SET name=?, surname=?, license_number=?, expiry_date=?
            WHERE id=?
        """, (name, surname, license_number, expiry_date, driver_id))
        conn.commit()
    except sqlite3.IntegrityError:
        raise ValueError("Le numéro de permis existe déjà.")
    except sqlite3.Error as e:
        logger.error(f"Erreur lors de la mise à jour du conducteur : {e}")
        conn.rollback()
        raise

def delete_driver(db_file, driver_id):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM drivers WHERE id=?", (driver_id,))
        conn.commit()
    except sqlite3.Error as e:
        logger.error(f"Erreur lors de la suppression du conducteur : {e}")
        conn.rollback()
        raise

def list_drivers(db_file):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM drivers")
    return cursor.fetchall()

def search_drivers(db_file, query):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    search_term = f"%{query}%"
    cursor.execute("""
        SELECT * FROM drivers
        WHERE name LIKE ? OR surname LIKE ? OR license_number LIKE ?
    """, (search_term, search_term, search_term))
    return cursor.fetchall()

# --- Fonctions pour les dépenses ---
def add_expense(db_file, vehicle_id, date, type, amount, description, mileage, liters):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO expenses (vehicle_id, date, type, amount, description, mileage, liters)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (vehicle_id, date, type, amount, description, mileage, liters))
        conn.commit()
        return cursor.lastrowid
    except sqlite3.Error as e:
        logger.error(f"Erreur lors de l'ajout de la dépense : {e}")
        conn.rollback()
        raise

def get_expense(db_file, expense_id):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM expenses WHERE id=?", (expense_id,))
    return cursor.fetchone()

def update_expense(db_file, expense_id, vehicle_id, date, type, amount, description, mileage, liters):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    try:
        cursor.execute("""
            UPDATE expenses SET vehicle_id=?, date=?, type=?, amount=?, description=?, mileage=?, liters=?
            WHERE id=?
        """, (vehicle_id, date, type, amount, description, mileage, liters, expense_id))
        conn.commit()
    except sqlite3.Error as e:
        logger.error(f"Erreur lors de la mise à jour de la dépense : {e}")
        conn.rollback()
        raise

def delete_expense(db_file, expense_id):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM expenses WHERE id=?", (expense_id,))
        conn.commit()
    except sqlite3.Error as e:
        logger.error(f"Erreur lors de la suppression de la dépense : {e}")
        conn.rollback()
        raise

def list_expenses(db_file, vehicle_id=None):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    if vehicle_id:
        cursor.execute("SELECT * FROM expenses WHERE vehicle_id=?", (vehicle_id,))
    else:
        cursor.execute("SELECT * FROM expenses")
    return cursor.fetchall()

def get_total_expenses(db_file, vehicle_id=None):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    if vehicle_id:
        cursor.execute("SELECT SUM(amount) FROM expenses WHERE vehicle_id=?", (vehicle_id,))
    else:
        cursor.execute("SELECT SUM(amount) FROM expenses")
    result = cursor.fetchone()
    return result[0] if result[0] else 0.0

def get_expenses_by_type(db_file, vehicle_id=None):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    if vehicle_id:
        cursor.execute("""
            SELECT type,
            
            SUM(amount) FROM expenses WHERE vehicle_id=? GROUP BY type
        """, (vehicle_id,))
    else:
        cursor.execute("SELECT type, SUM(amount) FROM expenses GROUP BY type")
    return cursor.fetchall()

# --- Fonctions pour les missions ---
def add_mission(db_file, driver_id, start_date, end_date, destination, duration, meals, nights, weekends):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO missions (driver_id, start_date, end_date, destination, duration, meals, nights, weekends)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (driver_id, start_date, end_date, destination, duration, meals, nights, weekends))
        conn.commit()
        return cursor.lastrowid
    except sqlite3.Error as e:
        logger.error(f"Erreur lors de l'ajout de la mission : {e}")
        conn.rollback()
        raise

def get_mission(db_file, mission_id):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM missions WHERE id=?", (mission_id,))
    return cursor.fetchone()

def update_mission(db_file, mission_id, driver_id, start_date, end_date, destination, duration, meals, nights, weekends):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    try:
        cursor.execute("""
            UPDATE missions SET driver_id=?, start_date=?, end_date=?, destination=?, duration=?, meals=?, nights=?, weekends=?
            WHERE id=?
        """, (driver_id, start_date, end_date, destination, duration, meals, nights, weekends, mission_id))
        conn.commit()
    except sqlite3.Error as e:
        logger.error(f"Erreur lors de la mise à jour de la mission : {e}")
        conn.rollback()
        raise

def delete_mission(db_file, mission_id):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM missions WHERE id=?", (mission_id,))
        conn.commit()
    except sqlite3.Error as e:
        logger.error(f"Erreur lors de la suppression de la mission : {e}")
        conn.rollback()
        raise

def list_missions(db_file, driver_id=None):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    if driver_id:
        cursor.execute("SELECT * FROM missions WHERE driver_id=?", (driver_id,))
    else:
        cursor.execute("SELECT * FROM missions")
    return cursor.fetchall()

# --- Fonctions pour l'affectation véhicule-conducteur ---
def assign_vehicle_to_driver(db_file, vehicle_id, driver_id, assignment_date):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO vehicle_assignments (vehicle_id, driver_id, assignment_date)
            VALUES (?, ?, ?)
        """, (vehicle_id, driver_id, assignment_date))
        conn.commit()
        return cursor.lastrowid
    except sqlite3.IntegrityError:
        raise ValueError("Ce véhicule est déjà affecté à ce conducteur.")
    except sqlite3.Error as e:
        logger.error(f"Erreur lors de l'affectation du véhicule : {e}")
        conn.rollback()
        raise

def get_assignment(db_file, assignment_id):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM vehicle_assignments WHERE id=?", (assignment_id,))
    return cursor.fetchone()

def list_assignments(db_file):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT va.id, v.registration, d.name, d.surname, va.assignment_date
        FROM vehicle_assignments va
        JOIN vehicles v ON va.vehicle_id = v.id
        JOIN drivers d ON va.driver_id = d.id
    """)
    return cursor.fetchall()

def get_vehicle_assignments(db_file, vehicle_id):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT va.id, d.name, d.surname, va.assignment_date
        FROM vehicle_assignments va
        JOIN drivers d ON va.driver_id = d.id
        WHERE va.vehicle_id=?
    """, (vehicle_id,))
    return cursor.fetchall()

def get_driver_assignments(db_file, driver_id):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT va.id, v.registration, va.assignment_date
        FROM vehicle_assignments va
        JOIN vehicles v ON va.vehicle_id = v.id
        WHERE va.driver_id=?
    """, (driver_id,))
    return cursor.fetchall()

def delete_assignment(db_file, assignment_id):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM vehicle_assignments WHERE id=?", (assignment_id,))
        conn.commit()
    except sqlite3.Error as e:
        logger.error(f"Erreur lors de la suppression de l'affectation : {e}")
        conn.rollback()
        raise

# --- Fonctions pour les alertes ---
def check_vehicle_alerts(db_file):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    today = datetime.now().strftime('%Y-%m-%d')
    alerts = []

    cursor.execute("SELECT id, registration, revision_date FROM vehicles WHERE revision_date IS NOT NULL AND revision_date <= date(?, '+30 days')", (today,))
    for row in cursor.fetchall():
        alerts.append({"type": "Révision à prévoir", "vehicle_id": row[0], "registration": row[1], "date": row[2]})

    cursor.execute("SELECT id, registration, control_date FROM vehicles WHERE control_date IS NOT NULL AND control_date <= date(?, '+30 days')", (today,))
    for row in cursor.fetchall():
        alerts.append({"type": "Contrôle technique à prévoir", "vehicle_id": row[0], "registration": row[1], "date": row[2]})

    cursor.execute("SELECT id, registration, revision_date FROM vehicles WHERE revision_date IS NOT NULL AND revision_date < ?", (today,))
    for row in cursor.fetchall():
        alerts.append({"type": "Révision dépassée", "vehicle_id": row[0], "registration": row[1], "date": row[2]})

    cursor.execute("SELECT id, registration, control_date FROM vehicles WHERE control_date IS NOT NULL AND control_date < ?", (today,))
    for row in cursor.fetchall():
        alerts.append({"type": "Contrôle technique dépassé", "vehicle_id": row[0], "registration": row[1], "date": row[2]})

    return alerts

def check_driver_alerts(db_file):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    today = datetime.now().strftime('%Y-%m-%d')
    alerts = []

    cursor.execute("SELECT id, name, surname, expiry_date FROM drivers WHERE expiry_date IS NOT NULL AND expiry_date <= date(?, '+30 days')", (today,))
    for row in cursor.fetchall():
        alerts.append({"type": "Permis expire bientôt", "driver_id": row[0], "name": f"{row[1]} {row[2]}", "date": row[3]})

    cursor.execute("SELECT id, name, surname, expiry_date FROM drivers WHERE expiry_date IS NOT NULL AND expiry_date < ?", (today,))
    for row in cursor.fetchall():
        alerts.append({"type": "Permis expiré", "driver_id": row[0], "name": f"{row[1]} {row[2]}", "date": row[3]})

    return alerts

def backup_database(db_file, backup_path):
    import shutil
    try:
        shutil.copy2(db_file, backup_path)
        logger.info(f"Base de données sauvegardée vers : {backup_path}")
        return True
    except Exception as e:
        logger.error(f"Erreur lors de la sauvegarde de la base de données : {e}")
        return False

def restore_database(backup_path, db_file):
    import shutil
    try:
        shutil.copy2(backup_path, db_file)
        logger.info(f"Base de données restaurée depuis : {backup_path}")
        return True
    except Exception as e:
        logger.error(f"Erreur lors de la restauration de la base de données : {e}")
        return False

if __name__ == '__main__':
    db_file = 'test_fleet_data.db'
    create_tables(db_file)

    # Exemple d'ajout et de listage
    vehicle_id = add_vehicle(db_file, "AA-123-BB", "Renault", "Clio", 2020, "2025-03-15", "2026-05-20")
    print(f"Véhicule ajouté avec l'ID : {vehicle_id}")
    vehicles = list_vehicles(db_file)
    print("Liste des véhicules :", vehicles)

    driver_id = add_driver(db_file, "Jean", "Dupont", "123456789", "2027-11-30")
    print(f"Conducteur ajouté avec l'ID : {driver_id}")
    drivers = list_drivers(db_file)
    print("Liste des conducteurs :", drivers)

    expense_id = add_expense(db_file, vehicle_id, "2025-05-05", "Carburant", 55.20, "Essence SP98", 15000, 40.5)
    print(f"Dépense ajoutée avec l'ID : {expense_id}")
    expenses = list_expenses(db_file, vehicle_id)
    print(f"Liste des dépenses pour le véhicule {vehicle_id} :", expenses)

    mission_id = add_mission(db_file, driver_id, "2025-05-10", "2025-05-12", "Paris", 3, 6, 2, 0)
    print(f"Mission ajoutée avec l'ID : {mission_id}")
    missions = list_missions(db_file, driver_id)
    print(f"Liste des missions pour le conducteur {driver_id} :", missions)

    assignment_id = assign_vehicle_to_driver(db_file, vehicle_id, driver_id, datetime.now().strftime('%Y-%m-%d'))
    print(f"Affectation ajoutée avec l'ID : {assignment_id}")
    assignments = list_assignments(db_file)
    print("Liste des affectations :", assignments)

    alerts = check_vehicle_alerts(db_file)
    print("Alertes véhicules :", alerts)
    driver_alerts = check_driver_alerts(db_file)
    print("Alertes conducteurs :", driver_alerts)

    backup_success = backup_database(db_file, "backup_fleet_data.db")
    print(f"Sauvegarde réussie : {backup_success}")
    restore_success = restore_database("backup_fleet_data.db", "restored_fleet_data.db")
    print(f"Restauration réussie : {restore_success}")