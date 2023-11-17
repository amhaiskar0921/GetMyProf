import requests
from urllib.parse import urlencode
import json

GRADE_BASE_URL = "https://api.peterportal.org/rest/v0/grades"


def calculate_mean_gpa(all_offerings_of_this_course_in_the_last_2_years: list[dict], prof_name: str):
    gpas = []
    for offering in all_offerings_of_this_course_in_the_last_2_years:
        if offering['instructor'] == prof_name:
            gpas.append(offering['averageGPA'])
    gpas = [i for i in gpas if i is not None]
    return sum(gpas) / len(gpas)

def calculate_grade_rate(all_offerings_of_this_course_in_the_last_2_years: list[dict], prof_name: str, grade: str):
    grades = 0
    size = 0
    for i in all_offerings_of_this_course_in_the_last_2_years:
        if i['instructor'] == prof_name:
            a_grade = i['gradeACount']
            b_grade = i['gradeBCount']
            c_grade = i['gradeCCount']
            d_grade = i['gradeDCount']
            f_grade = i['gradeFCount']
            total_student = a_grade+b_grade+c_grade+d_grade+f_grade
            if grade == "A":
                grades += a_grade/total_student
            elif grade == "B":
                grades += (a_grade+b_grade) / total_student
            elif grade == "C":
                grades += (a_grade+b_grade+c_grade) / total_student
            elif grade == "D":
                grades += (a_grade+b_grade+c_grade+d_grade) / total_student
            else:
                grades += (a_grade+b_grade+c_grade+d_grade+f_grade) / total_student
            size += 1
    return grades/size


def get_all_prof_info_for_given_course(year_start, year_end, department, number) -> dict:
    base_url = "https://api.peterportal.org/rest/v0/grades"
    common_params = {
        'department': department,
        'number': number
    }
    year = ""
    for i in range(year_start, year_end):
        year += str(i) + "-" + str((i + 1) % 1000) + ";"
    raw_params = {
        'year': year[:-1]
    }
    # Combine common and raw parameters
    raw_url = f"{GRADE_BASE_URL}/raw?{urlencode({**common_params, **raw_params})}"
    
    # Getting the list of professors
    page = requests.get(raw_url)
    if (page):
        prof_dict = json.loads(page.content)
        return prof_dict
       

def get_teacher_names(full_prof_dict) -> set:
    x = {i['instructor'] for i in full_prof_dict if i['instructor'] != 'UNKNOWN, INSTRUCTOR'}
    return x


if __name__ == "__main__":
    teachers = get_all_prof_info_for_given_course(2010, 2023, "I&C SCI", "51")
    if (len(teachers) != 0):
        names_set = get_teacher_names(teachers)
        for i in names_set:
            print(i)
        print(calculate_mean_gpa(teachers, "WONG-MA, J."))
    else:
        print("NO PROFESSORS FOUND FOR THIS COURSE")
    # print(requests.get(u).json())

# See PyCharm help at https://www.jetbrains.com/help/pycharm/