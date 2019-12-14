import copy
import os.path

# FOR BASE SOLUTION
def find_dicts(id, key, search_list, type_to_message):
    target_dicts = []
    for i in range (0, len(search_list)):
        current_dict = search_list[i]
        if (current_dict[key] == id):
            target_dicts.append(current_dict)
    if (target_dicts == []):
        print("There is no", type_to_message,
                "with <", id, "> id")
        return []
    return target_dicts


def find_dict(id, key, search_list, type_to_message):
    target_dicts = find_dicts(id, key, search_list, type_to_message)
    if (target_dicts != []):
        return target_dicts[0]
    else:
        return {}


def find_exam_by_trainer(trainer_id, trainers):
    target_trainer = find_dict(trainer_id, 'userId', trainers, 'trainer')
    if (target_trainer == {}):
        return 
    return target_trainer['examId']


def find_users_by_exam(exam_id, users):
    user_list = []
    for i in range (0, len(users)):
        current_user = users[i]
        if (current_user['examId'] == exam_id):
            user_list.append(current_user['userId'])
    if (user_list == []):
        print('There are no users who took the <', exam_id, '> exam')
        return 
    else:
        return user_list


def get_users_examId(user_id, users, exams):
    target_user = find_dict(user_id, 'userId', users, 'user')
    if (target_user == {}):
        return
    e_id = target_user['examId']
    print("User was passing", e_id, "exam...")
    target_exam = find_dict(e_id, 'examId', exams, 'exam')
    if (target_exam == {}):
        return
    else:
        return e_id


def get_exam_answers(exam_id, exams, questions, answers):
    target_exam = find_dict(exam_id, 'examId', exams, 'exam')
    if (target_exam == {}):
        return
    exam_min_score = target_exam['scoreMin']
    exam_questions = target_exam['questionIds']
    exam_max_score = 0

    answers_tuples = []
    for i in range (0, len(exam_questions)):
        q_id = exam_questions[i]
        target_q = find_dict(q_id, 'questionId', questions, 'question')
        if (target_q == {}):
            return
        a_id = target_q['answerId']
        target_a = find_dict(a_id, 'answerId', answers, 'answer')
        if (target_a == {}):
            return
        exam_max_score += target_q['score']
        ans_tuple = (q_id, a_id,
                        target_q['score'], target_a['isCorrect'])
        answers_tuples.append(ans_tuple)
    answers_tuples.sort()
    return ((exam_min_score, exam_max_score), answers_tuples)

# [(user_id, [(qId, aId)])]
# get users' answers by exam_id
def get_users_answers(exam_id, users, exams, questions, answers):
    target_exam = find_dict(exam_id, 'examId', exams, 'exam')
    if (target_exam == {}):
        return
    exam_questions = target_exam['questionIds']
    # dict of all answers: key is userId and value is [(qId, aId)]
    a_dict = {}
    for i in range (0, len(exam_questions)):
        q_id = exam_questions[i]
        target_q = find_dict(q_id, 'questionId', questions, 'question')
        if (target_q == {}):
            return
        a_ids = target_q['answerIds']
        for j in range (0, len(a_ids)):
            a_id = a_ids[j]
            target_a = find_dict(a_id, 'id', answers, 'answer')
            if (target_a == {}):
                return
            u_id = target_a['userId']
            exist_u_answers = a_dict.get(u_id)
            new_answer = (q_id, a_id)
            if (exist_u_answers == None):
                exist_u_answers = [new_answer]
            else:
                exist_u_answers.append(new_answer)
            
            #slow every time, but we are not in hurry, right? :)
            exist_u_answers.sort()
            a_dict.update({u_id : exist_u_answers})
    return a_dict


def get_min_and_max_scores(exam_max_score, exam_answers, user_answers):
    min_score, max_score = 0, 0
    
    for i in range (0, len(exam_answers)):
        exam_tuple = exam_answers[i]
        user_tuple = user_answers[i]
        if (exam_tuple[0] == user_tuple[0]):
            # the same answers
            if (exam_tuple[1] == user_tuple[1]):
                if (exam_tuple[3] == 1):
                    min_score += exam_tuple[2]
                    max_score += exam_tuple[2]
                # else the answer is incorrect anyway
            else:
                # if the exam answer is incorrect user's answer may be correct
                if (exam_tuple[3] == 0):
                    max_score += exam_tuple[2]
        else:
            # bcs questions are sorted by ids
            print("Exam questions doesn't equal user's questions")
            return
    min_percentage = round(min_score / exam_max_score, 3) * 100
    max_percentage = round(max_score / exam_max_score, 3) * 100

    return (min_score, max_score, min_percentage, max_percentage)

# 0 - didn't pass, 1 - may be passed, 2 - passed
def is_passed(user_min_score, user_max_score, exam_min_score):
    if (user_max_score < exam_min_score):
        return 0
    else:
        if (user_min_score < exam_min_score):
            return 1
        else:
            return 2


def report_on_passing(pass_index, userId):
    if (pass_index == 0):
        print("User <", userId, "> definitely didn't pass the exam")
    else:
        if (pass_index == 1):
            print("User <", userId, "> could pass the exam")
        else:
            print("User <", userId, "> definitely passed the exam\n")


def pretty_show_exam(exam_min_score, exam_answers):
    print("Exam's minimum score:", exam_min_score)
    print("Exam's information in format : <questionId>, <answerId>, <questionScore>, <isCorrect>")
    for i in range (0, len(exam_answers)):
        print(exam_answers[i])


def pretty_show_results(exam_min_score, exam_max_score, exam_answers, users_answers):
    print("\nUsers' results:")
    users_tuples_list = [(k, v) for k, v in users_answers.items()]
    for i in range (0, len(users_tuples_list)):
        current_u_tuple = users_tuples_list[i]
        print("User <", current_u_tuple[0], "> :")
        (min_score, max_score, min_percentage, max_percentage) = get_min_and_max_scores(exam_max_score,
                                                                                        exam_answers,
                                                                                        current_u_tuple[1])
        print("Minimum score:", min_score, "Maximum score:", max_score,
                "\nMinimum percentage:", min_percentage, "Maximum percentage:", max_percentage)
        print("Answers' information in format : <questionId> <answerId>")
        for q_a in current_u_tuple[1]:
            print(q_a)
        pass_index = is_passed(min_score, max_score, exam_min_score)
        print("Verdict:")
        report_on_passing(pass_index, current_u_tuple[0])

def answers_to_scores(exam_max_score, exam_answers, users_answers):
    users_tuples_list = [(k, v) for k, v in users_answers.items()]
    scores_list = []
    for i in range (0, len(users_tuples_list)):
        current_u_tuple = users_tuples_list[i]
        user_id = current_u_tuple[0]
        (min_score, max_score, min_percentage, max_percentage) = get_min_and_max_scores(exam_max_score,
                                                                                        exam_answers,
                                                                                        current_u_tuple[1])
        scores_tuple = (user_id, (min_score, max_score), (min_percentage, max_percentage))
        scores_list.append(scores_tuple)
    return scores_list

def sort_by_max_score(user_scores):
    return user_scores[1][1]




# FOR EXTRA SOLUTION
def get_answers_and_scores():
    print("Enter exam's id")
    exam_id = int(input())
    print("What's minimum score?")
    min_scores = int(input())
    print("And what's the number of questions?")
    num_q = int(input())
    # (qId, aId, score)
    ans_sc_tuples = []

    print("Now enter the information about exam in a format 'questionId answerId questionScores'")
    for i in range (0, num_q):
        inp = input()
        q_a_s = []
        q_a_s = inp.split()
        for j in range (0, len(q_a_s)):
            q_a_s[j] = int(q_a_s[j])

        ans_sc_tuples.append(tuple(q_a_s))
    return (exam_id, min_scores, ans_sc_tuples) 


def get_question_ids(answers_and_scores):
    a_s_list = answers_and_scores[2]
    question_ids = []
    for i in range (0, len(a_s_list)):
        question_ids.append(a_s_list[i][0])
    return question_ids


def get_user_answers(question_ids):
    print("Hello, you are going to be tested, enter your id, please")
    user_id = int(input())
    answer_ids = []
    for i in range (0, len(question_ids)):
        print("The question:", question_ids[i])
        print("Enter your answer:")
        ans = int(input())
        answer_ids.append((question_ids[i], ans))
    print("The test is finished. See you later!")
    return (user_id, answer_ids)


def get_user_scores(user_answers, answers_and_scores):
    a_s_tuples = answers_and_scores[2]
    user_scores = 0
    a_s_tuples.sort()
    user_answers.sort()

    for i in range (0, len(a_s_tuples)):
        if (a_s_tuples[i][1] == user_answers[i][1]):
            user_scores += a_s_tuples[i][2]
    return user_scores    


def write_results(exam_id, min_score, user_id, user_scores):
    filename = "exam" + str(exam_id) + ".txt"
    check_file = os.path.exists(filename) 
    if (check_file):
        f = open(filename, "a")
    else:
        f = open(filename, "w")
        f.write("Minimum score: " + str(min_score) + "\n")
        f.write("User's id:      " + "User's scores:\n")
    
    f.write('%-16s' % str(user_id))
    f.write('%-16s' % str(user_scores))
    f.write('\n')

    f.close()
