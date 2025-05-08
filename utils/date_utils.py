from datetime import date, timedelta

def calculate_weekends(start_date, end_date):
    if not isinstance(start_date, date) or not isinstance(end_date, date):
        raise TypeError("Les arguments doivent être des objets datetime.date")
    if start_date > end_date:
        return 0
    weekends = 0
    current_date = start_date
    while current_date <= end_date:
        if current_date.weekday() >= 5:  # Saturday (5) or Sunday (6)
            weekends += 1
        current_date += timedelta(days=1)
    return weekends