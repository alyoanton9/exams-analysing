import time
import utils as u

############ main part #######################

print("Hello!")
answers_and_scores = u.get_answers_and_scores()
print(answers_and_scores)
question_ids = u.get_question_ids(answers_and_scores)

print("What number of users are going to be tested today?")
users_num = int(input())

for i in range (0, users_num):
    (user_id, user_answers) = u.get_user_answers(question_ids)
    #print(user_answers)
    user_scores = u.get_user_scores(user_answers, answers_and_scores)
    #print(user_scores)
    u.write_results(answers_and_scores[0], answers_and_scores[1], user_id, user_scores)
    time.sleep(3)