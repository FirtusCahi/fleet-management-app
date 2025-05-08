import pandas as pd

def export_to_excel(filepath, vehicles, drivers, expenses, missions, assignments, lang):
    writer = pd.ExcelWriter(filepath, engine='xlsxwriter')

    # Vehicles
    if vehicles:
        df_vehicles = pd.DataFrame(vehicles, columns=['ID', lang.get("registration", "Immatriculation"), lang.get("make", "Marque"), lang.get("model", "Modèle"), lang.get("year", "Année"), lang.get("revision_date_short", "Révision"), lang.get("control_date_short", "Contrôle")])
        df_vehicles.to_excel(writer, sheet_name=lang.get("vehicles_title", "Véhicules"), index=False)

    # Drivers
    if drivers:
        df_drivers = pd.DataFrame(drivers, columns=['ID', lang.get("name", "Nom"), lang.get("surname", "Prénom"), lang.get("license_number", "Numéro de permis"), lang.get("expiry_date_short", "Expiration")])
        df_drivers.to_excel(writer, sheet_name=lang.get("drivers_title", "Conducteurs"), index=False)

    # Expenses
    if expenses:
        expenses_data = []
        for exp in expenses:
            vehicle = database.get_vehicle(None, exp[1]) # Need connection if not in same scope
            vehicle_reg = vehicle[1] if vehicle else lang.get("unknown", "Inconnu")
            expenses_data.append([exp[0], vehicle_reg, exp[2], exp[3], exp[4], exp[5], exp[6], exp[7]])
        df_expenses = pd.DataFrame(expenses_data, columns=['ID', lang.get("vehicle", "Véhicule"), lang.get("date", "Date"), lang.get("type", "Type"), lang.get("amount", "Montant"), lang.get("description", "Description"), lang.get("mileage", "Kilométrage"), lang.get("liters", "Litres")])
        df_expenses.to_excel(writer, sheet_name=lang.get("expenses_title", "Dépenses"), index=False)

    # Missions
    if missions:
        missions_data = []
        for mis in missions:
            driver = database.get_driver(None, mis[1]) # Need connection if not in same scope
            driver_name = f"{driver[1]} {driver[2]}" if driver else lang.get("unknown", "Inconnu")
            missions_data.append([mis[0], driver_name, mis[2], mis[3], mis[4], mis[5], mis[6], mis[7], mis[8]])
        df_missions = pd.DataFrame(missions_data, columns=['ID', lang.get("driver", "Conducteur"), lang.get("start_date_short", "Début"), lang.get("end_date_short", "Fin"), lang.get("destination", "Destination"), lang.get("duration_short", "Durée"), lang.get("meals_short", "Repas"), lang.get("nights_short", "Nuits"), lang.get("weekends_short", "WE")])
        df_missions.to_excel(writer, sheet_name=lang.get("missions_title", "Missions"), index=False)

    # Assignments
    if assignments:
        df_assignments = pd.DataFrame(assignments, columns=['ID', lang.get("registration", "Immatriculation"), lang.get("name", "Nom"), lang.get("surname", "Prénom"), lang.get("assignment_date_short", "Date d\'affectation")])
        df_assignments.to_excel(writer, sheet_name=lang.get("assignments_title", "Affectations"), index=False)

    writer.close()