import json
import copy
import utils as u
import visual as vi
import matplotlib.pyplot as plt

############## main part ###############################

with open("exams_information.json", "r") as read_file1:
    exams_info = json.load(read_file1)
with open("users_answers.json", "r") as read_file2:
    users_info = json.load(read_file2)

trainers = exams_info['trainers']
exams = exams_info['exams']
e_questions = exams_info['questions']
e_answers = exams_info['answers']

users = users_info['users']
u_questions = users_info['questions']
u_answers = users_info['answers']

print("Hello! Enter your id, please.")
trainer_id = int(input())
trainers_exam_id = u.find_exam_by_trainer(trainer_id, trainers)
if (trainers_exam_id != None):
    (exam_min_score, exam_max_score), exam_answers = u.get_exam_answers(trainers_exam_id,
                                                                        exams, e_questions,
                                                                        e_answers)
    u.pretty_show_exam(exam_min_score, exam_answers)

    users_answers = u.get_users_answers(trainers_exam_id, users, exams,
                                        u_questions, u_answers)

    u.pretty_show_results(exam_min_score, exam_max_score, exam_answers, users_answers)
    users_scores = u.answers_to_scores(exam_max_score, exam_answers, users_answers)
    users_scores.sort(key = u.sort_by_max_score, reverse = True)

    print("Do you want to visualise results? (y / n)")
    answer = input()
    if (answer == 'y'):
        bar_tuples = vi.get_bar_tuples(users_scores)
        ((fig, ax), (rects1, rects2)) = vi.get_splots_and_rects(bar_tuples, exam_min_score)

        vi.autolabel(ax, rects1, "left")
        vi.autolabel(ax, rects2, "right")
        fig.tight_layout() # checks the extents of ticklabels, axis labels, and titles
        plt.show()
