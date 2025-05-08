from datetime import datetime

class Vehicle:
    def __init__(self, id=None, registration=None, make=None, model=None, year=None, revision_date=None, control_date=None):
        self.id = id
        self.registration = registration
        self.make = make
        self.model = model
        self.year = year
        self.revision_date = self._parse_date(revision_date)
        self.control_date = self._parse_date(control_date)

    def _parse_date(self, date_str):
        return datetime.strptime(date_str, '%Y-%m-%d').date() if date_str else None

class Driver:
    def __init__(self, id=None, name=None, surname=None, license_number=None, expiry_date=None):
        self.id = id
        self.name = name
        self.surname = surname
        self.license_number = license_number
        self.expiry_date = self._parse_date(expiry_date)

    def _parse_date(self, date_str):
        return datetime.strptime(date_str, '%Y-%m-%d').date() if date_str else None

class Expense:
    def __init__(self, id=None, vehicle_id=None, date=None, type=None, amount=None, description=None, mileage=None, liters=None):
        self.id = id
        self.vehicle_id = vehicle_id
        self.date = self._parse_date(date)
        self.type = type
        self.amount = amount
        self.description = description
        self.mileage = mileage
        self.liters = liters

    def _parse_date(self, date_str):
        return datetime.strptime(date_str, '%Y-%m-%d').date() if date_str else None

class Mission:
    def __init__(self, id=None, driver_id=None, start_date=None, end_date=None, destination=None, duration=None, meals=None, nights=None, weekends=None):
        self.id = id
        self.driver_id = driver_id
        self.start_date = self._parse_date(start_date)
        self.end_date = self._parse_date(end_date)
        self.destination = destination
        self.duration = duration
        self.meals = meals
        self.nights = nights
        self.weekends = weekends

    def _parse_date(self, date_str):
        return datetime.strptime(date_str, '%Y-%m-%d').date() if date_str else None

class VehicleAssignment:
    def __init__(self, id=None, vehicle_id=None, driver_id=None, assignment_date=None):
        self.id = id
        self.vehicle_id = vehicle_id
        self.driver_id = driver_id
        self.assignment_date = self._parse_date(assignment_date)

    def _parse_date(self, date_str):
        return datetime.strptime(date_str, '%Y-%m-%d').date() if date_str else None