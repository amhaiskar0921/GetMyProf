from collections import defaultdict
import PeterPortal_queries as pp
from RMP_queries import UCI_Prof

q2tags = ["lots of homework", "so many papers"]
q3tags = ["caring", "gives good feedback", "clear grading criteria"]
q4tags = ["gives good feedback", "clear grading criteria", "tough grader", "amazing lectures", "test heavy"]

def process_questionnaire_answers(answers):
    # Customize this based on your questionnaire structure
    # This is just a placeholder, you should adapt it to your actual questionnaire structure
    user_answers = [
        answers['classDiff'],  # Map classDiff to the appropriate value
        answers['workload'],   # Map workload to the appropriate value
        answers['likeable'],   # Map likeable to the appropriate value
        answers['learning'],   # Map learning to the appropriate value
    ]
    return user_answers


def questionOne(prof_scores: dict, all_profs_for_this_course: dict, non_neutral_ans: int):
    if non_neutral_ans:
        for prof in all_profs_for_this_course:
            prof_avg = pp.calculate_mean_gpa(all_profs_for_this_course, prof['instructor'])
            if prof['instructor'] != 'UNKNOWN, INSTRUCTOR' and prof['instructor'] not in prof_scores:
                if non_neutral_ans == -1:
                    prof_scores[prof['instructor']] += prof_avg
                else:
                    prof_scores[prof['instructor']] += (4 - prof_avg)

    return prof_scores

def tag_cases(prof_scores: dict, unique_prof_names: set, user_answers: list[int]):
    tags = {2: q2tags, 3: q3tags, 4: q4tags}
    q_num = 2

    prof_objects = {}  # Dictionary to store professor objects

    for name in unique_prof_names:
        rmp_prof_obj = UCI_Prof(name[:-1])
        prof_objects[name] = rmp_prof_obj

    tag_freqs_for_all_profs = {name: prof_obj.get_tag_freq() for name, prof_obj in prof_objects.items()}  # Fetch tag frequencies for all professors
    # print(tag_freqs_for_all_profs)

    for tag in tags[q_num]:
        if user_answers[q_num - 1] == 0:
            continue
        for name, prof_obj in prof_objects.items():
            tag_freqs_for_this_prof = tag_freqs_for_all_profs[name]  # Use the pre-fetched tag frequencies
            if tag in tag_freqs_for_this_prof:
                if user_answers[q_num - 1] == 1:  # we already finished index 0, the first question
                    prof_scores[name] += tag_freqs_for_this_prof[tag]
                else:
                    prof_scores[name] -= tag_freqs_for_this_prof[tag]
        q_num += 1

    return prof_scores



def get_top_professors(all_profs_for_this_course: dict, user_answers: list[bool]):
    unique_prof_names = pp.get_teacher_names(all_profs_for_this_course)
    prof_scores = defaultdict(float)  # Initialize with float
    prof_scores = questionOne(prof_scores, all_profs_for_this_course, user_answers[0])
    prof_scores = tag_cases(prof_scores, unique_prof_names, user_answers)

    if (len(prof_scores) > 3):
        top_n_values = sorted(prof_scores.items(), key=lambda item: item[1], reverse=True)[:3]
    else:
        top_n_values = sorted(prof_scores.items(), key=lambda item: item[1], reverse=True)
    return top_n_values

if __name__ == '__main__':
    prof_dict = pp.get_all_prof_info_for_given_course(2021, 2023, "I&C SCI", "51")
    # print(prof_dict)
    prof_names = pp.get_teacher_names(prof_dict)
    # print(prof_names)
    
    # prof_list = [ranking.Professor(all_info, name) for all_info, name in zip(prof_dict, prof_names)]
    # prof_scores = {}  # Initialize with float
    # for name in prof_names:
    #     prof_scores[name] = 0.0
    # prof_scores = questionOne(prof_scores, prof_list, True)
    # print(prof_scores)

    # 0: neutral so that we can just skip over it
    # -1: don't want this quality
    # 1: we want this quality
    user_answers = [-1, -1, 0, 1]
    # prof_scores = questionOne(prof_scores, prof_dict, user_answers[0])

    # unique_prof_names = pp.get_teacher_names(prof_dict)
    # prof_scores = tag_cases(prof_scores, unique_prof_names, user_answers)

    top_profs = get_top_professors(prof_dict, user_answers)
    print(top_profs)
