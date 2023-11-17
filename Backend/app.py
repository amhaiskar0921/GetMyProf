# app.py
from flask import Flask, request, render_template
from flask_cors import CORS
import sorting_ranking
import PeterPortal_queries as pp
from RMP_queries import UCI_Prof

app = Flask(__name__, template_folder='../Frontend', static_folder='../static')
CORS(app)

START_YEAR = 2021
END_YEAR = 2023

@app.route("/")
def index():
    # Render your index.html from the frontend folder
    return render_template("index.html")

# @app.route("/questionnaire")
# def questionnaire():
#     result = request.form
#     # Render the questionnaire template
#     return render_template("questionnaire.html", result = result)

@app.route("/answers", methods=['POST'])
def process_answers():
    # Handle the answers received from the frontend
    answers = request.form
    print("Received data:", answers)
    # Convert answers to the format expected by the sorting_ranking module
    user_answers = sorting_ranking.process_questionnaire_answers(answers)
    # Get professor information based on the answers
    prof_dict = pp.get_all_prof_info_for_given_course(
        START_YEAR, END_YEAR, answers['department'], answers['courseName'])
    
    # Process the answers and return the results
    top_profs = sorting_ranking.get_top_professors(prof_dict, user_answers)
    all_top_prof_info = {}

    for prof in top_profs:
        all_top_prof_info[prof[0]] = {}
        all_top_prof_info[prof[0]]['Average GPA'] = pp.calculate_mean_gpa(prof_dict, prof[0])
        rmp_prof_obj = UCI_Prof(prof[0][:-1])
        all_top_prof_info[prof[0]]['Average difficulty'] = rmp_prof_obj.get_avg_difficulty()
        all_top_prof_info[prof[0]]['Retake rate'] = rmp_prof_obj.get_retake_percentage()

    # Render the results template with the obtained data
    return render_template("results.html", results=all_top_prof_info)


if __name__ == "__main__":
    app.run(debug=True)