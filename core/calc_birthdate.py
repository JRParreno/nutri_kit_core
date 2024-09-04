from datetime import datetime, date

def calculate_age(born):
    today = date.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))

def calculate_total_months(birthdate, current_date=None):
    # If no current date is provided, use today's date
    if current_date is None:
        current_date = datetime.today()
    
    # Calculate the difference in years and months
    years_diff = current_date.year - birthdate.year
    months_diff = current_date.month - birthdate.month
    
    # Calculate the total months
    total_months = years_diff * 12 + months_diff
    
    # Adjust if the day of the current month is before the birthdate day
    if current_date.day < birthdate.day:
        total_months -= 1
    
    return total_months