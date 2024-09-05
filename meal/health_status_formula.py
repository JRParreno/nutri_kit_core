import os
from django.conf import settings

from core.calc_birthdate import calculate_age, calculate_total_months
from meal.excel_reader import read_excel_file
from meal.models import UserMealPlan


def adjust_to_nearest_half(value):
    # Multiply by 2, round to nearest integer, then divide by 2
    # This rounds the value to the nearest 0.5 interval
    return round(value * 2) / 2


def getHealthForZWH(height, weight, age, gender):
    rounded_height = adjust_to_nearest_half(height)
    first_str_path = f"wfl_{'boys' if gender.lower() == 'male' else 'girls'}_0-to-2-years_zscores.xlsx"
    second_str_path = f"wfh_{'boys' if gender.lower() == 'male' else 'girls'}_2-to-5-years_zscores.xlsx"
    
    first_file_path = os.path.join(settings.BASE_DIR, 'assets', 'formula_one', first_str_path)
    second_file_path = os.path.join(settings.BASE_DIR, 'assets', 'formula_one', second_str_path)
    
        
    """
    For Wasted (Weight-for-Height Z-Score)
    ZWH= (weight - median weight for height) /
            SD0 - SD1neg
    """
    # Read the data from the Excel file
    first_data = read_excel_file(first_file_path)
    second_data = read_excel_file(second_file_path)

    
    if age >= 1 and age < 2:
        for index, row  in enumerate(first_data):
            row_length = row['Length']
            if (row_length == rounded_height):
                # print("------")
                # print("ZWH")
                # print(f"Length: {row_length} \nSD0: {row['SD0']} \nSD1neg: {row['SD1neg']}")
                # print("------")
                return (weight - row['SD0']) / (row['SD0'] - row['SD1neg'])

    if age >= 2 and age <= 5:
        for index, row  in enumerate(second_data):
            row_height = row['Height']
            if (row_height == rounded_height):
                # print("------")
                # print("ZWH")
                # print(f"Height: {row_height} \nSD0: {row['SD0']} \nSD1neg: {row['SD1neg']}")
                # print("------")

                return (weight - row['SD0']) / (row['SD0'] - row['SD1neg'])
    
    
    return -4


def getHealthForZHA(height, birthdate, gender):
    first_str_path = f"lhfa_{'boys' if gender.lower() == 'male' else 'girls'}_0-to-2-years_zscores.xlsx"
    second_str_path = f"lhfa_{'boys' if gender.lower() == 'male' else 'girls'}_2-to-5-years_zscores.xlsx"
    
    first_file_path = os.path.join(settings.BASE_DIR, 'assets', 'formula_two', first_str_path)
    second_file_path = os.path.join(settings.BASE_DIR, 'assets', 'formula_two', second_str_path)
    age = calculate_age(birthdate)
    months = calculate_total_months(birthdate)
    """
    For Stunted (Height-for-Age Z-Score)
    ZHA= (height - median height for age) /
            SD0 - SD1neg
    """
    # Read the data from the Excel file
    first_data = read_excel_file(first_file_path)
    second_data = read_excel_file(second_file_path)

    
    if age >= 1 and age < 2:
        for index, row  in enumerate(first_data):
            row_month = row['Month']
            if (row_month == months):
                # print("------")
                # print("ZHA")
                # print(f"Month: {row_month} \nSD0: {row['SD0']} \nSD1neg: {row['SD1neg']}")
                # print("------")

                return (height - row['SD0']) / row['SD']
            
    if age >= 2 and age <= 5:
        for index, row  in enumerate(second_data):
            row_month = row['Month']
            if (row_month == months):
                # print("------")
                # print("ZHA")
                # print(f"Month: {row_month} \nSD0: {row['SD0']} \nSD1neg: {row['SD1neg']}")
                # print("------")
                return (height - row['SD0']) / row['SD']
    
    
    return -4


def getHealthForZWA(weight, birthdate, gender):
    str_path = f"wfa_{'boys' if gender.lower() == 'male' else 'girls'}_0-to-5-years_zscores.xlsx"
    
    file_path = os.path.join(settings.BASE_DIR, 'assets', 'formula_three', str_path)
    months = calculate_total_months(birthdate)
    """
    For Underweight (Weight-for-Age Z-Score)
    ZWA = (weight - median weight for age) /
            SD0 - SD1neg
    """
    # Read the data from the Excel file
    data = read_excel_file(file_path)

    
    for index, row  in enumerate(data):
        row_month = row['Month']
        if (row_month == months):
            # print("------")
            # print("ZWA")
            # print(f"Month: {row_month} \nSD0: {row['SD0']} \nSD1neg: {row['SD1neg']}")
            # print("------")

            return (weight - row['SD0']) / (row['SD0'] - row['SD1neg'])
    
    return -4



def select_formula(formulas):
    if all(-2 <= value <= -1 or 1 <= value <= 2 for value in formulas.values()):
        return None

    if all(value > 0 for value in formulas.values()):
        temp_formula_three_value = formulas['formula_three']
        if (temp_formula_three_value >= 2 and temp_formula_three_value <= 3):
            return "overweight"
        return "obese"
    # Return the lowest value with priority: formula_three > formula_two > formula_one
    if formulas['formula_one'] < -2 or formulas['formula_one'] < -3:
       return "wasted"
    if formulas['formula_two'] < -2 or formulas['formula_two'] < -3:
        return "stunted"
    if formulas['formula_three'] < -2 or formulas['formula_three'] < -3:
        return "underweight"
    
    return None
        
