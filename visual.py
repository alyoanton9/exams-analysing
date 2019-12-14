import matplotlib
import matplotlib.pyplot as plt
import numpy as np

# we have scores in format : [(user_id, (min_score, max_score))]
def get_bar_tuples(users_scores):
    ids_list = []
    min_scores_list = []
    max_scores_list = []
    for i in range (0, len(users_scores)):
        user_id = users_scores[i][0]
        user_min_score = users_scores[i][1][0]
        user_max_score = users_scores[i][1][1]

        ids_list.append(user_id)
        min_scores_list.append(user_min_score)
        max_scores_list.append(user_max_score)
    
    ids_tuple = tuple(ids_list)
    min_scores_tuple = tuple(min_scores_list)
    max_scores_tuple = tuple(max_scores_list)
    return (ids_tuple, min_scores_tuple, max_scores_tuple) 

def get_splots_and_rects(bar_tuples, exam_min_score):
    ids = bar_tuples[0]
    min_scores = bar_tuples[1]
    max_scores = bar_tuples[2]

    ind = np.arange(len(min_scores))  # the x locations for the groups
    """suppose there are just numbers from 0 to number of users, also there are x-cord. of the middle of bar (check it)"""
    print(min_scores)
    print(ind)
    width = 0.3 # the width of the bars

    (fig, ax) = plt.subplots() # figure and axes (оси)
    rects1 = ax.bar(ind - width / 2, min_scores, width, 
                label = "Minimum user's score")
    """ 'ind - width/2' is an x-coordinate of bar's center (0.85 and 1.15 for 1 bar left and right(r2))
        min_scores are heights of bars, label is written on the top"""
    rects2 = ax.bar(ind + width / 2, max_scores, width,
                label = "Maximum user's scrore")

    ax.set_ylabel("Exam's scores")
    ax.set_xlabel("Users' ids")
    ax.set_title("Minimum and maximum exam scores of users")
    ax.set_xticks(ind) # x points of bars (there are just 0..number of users)
    ax.set_xticklabels(ids)
    plt.axhline(y = exam_min_score, linewidth = 1, color = "black",
                    label = "Exam's minimum score") # just a horizontal line
    ax.legend() # just to add labels
    return ((fig, ax), (rects1, rects2))

def autolabel(ax, rects, xpos = 'center'):
    ha = {'center': 'center', 'right': 'left', 'left': 'right'}
    offset = {'center': 0, 'right': 1, 'left': -1}

    for rect in rects:
        height = rect.get_height()
        """annotate point xy with the textА
        add the text on the top of the bar"""
        ax.annotate('{}'.format(height),
                    xy = (rect.get_x() + rect.get_width() / 2, height), 
                    xytext = (offset[xpos]*3, 1), # hard to understand
                    textcoords = "offset points", # coords are set as offsets
                    ha = ha[xpos], va = 'bottom') # horizontal and vertical alignment