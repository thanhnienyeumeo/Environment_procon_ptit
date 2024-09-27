# swagger doc: https://proconvn.duckdns.org/docs

import requests
import json
import numpy as np
from pattern import Pattern
from game import Game
url = "https://proconvn.duckdns.org"
headers = {"Authorization": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MjIsIm5hbWUiOiJQVElUIiwiaXNfYWRtaW4iOmZhbHNlLCJpYXQiOjE3MjcwODE4NzAsImV4cCI6MTcyNzI1NDY3MH0.q_v10XqiMVC4q44Tcw3xewdjDPzKIct7eeAFP_0Tvtg"}


# request question from server
question_id = 72
#get part

# question = requests.get(f"{url}/question/{question_id}", headers=headers).json()

# with open('question.json', 'w') as f:
#     json.dump(question, f, indent=4)

#load part
f = open('question.json', 'r')
question = json.load(f)

def get_info(question) :
    question_data = json.loads(question['question_data'])
    board = question_data['board']
    general = question_data['general']

    #preprocess board
    for i in board: print(i)
    height = board['height']
    width = board['width']
    start_board = board['start']
    
    end_board = board['goal']
    start_board = np.array(start_board)
    end_board = np.array(end_board)
    print(start_board.shape)
    #preprocess general
    n = general['n']

    general_patterns = []
    for i in general["patterns"]:
        p = i["p"]
        width = i["width"]
        height = i["height"]
        cells = i["cells"]
        cells = np.array(cells)
        general_patterns.append(Pattern(height, width, board = cells))
    return height, width, start_board, end_board, general_patterns

height, width, start_board, end_board, general_patterns = get_info(question)
print(start_board.shape)
print(end_board.shape)

for patterns in general_patterns:
    print(patterns)
m = start_board.shape[0]
n = start_board.shape[1]
print(m,n)

game = Game(m, n, 20, start_board, end_board, general_patterns)

def check(board, final_board, x,y,p,q):
    #check if the part of x
    if x >= 0 and y >= 0 and (x + p > board.shape[0] or y + q > board.shape[1]):
        return False
    if board[x][y] == final_board[x][y]:
        return False
    return True
#duyet tat ca cac step co the --> dua ra step cho ket qua tot nhat
cur_board = game.grid.board.copy()
final_board = game.final_grid.board.copy()
for i in range(0, len(game.dict)):
    # if i % 500 == 0: 
    x,y, direction, id = game.dict[i]
    p,q,type = game.grid.patterns[id].p, game.grid.patterns[id].q, game.grid.patterns[id].id
    if(not check(cur_board, final_board, x,y,p,q)): continue
    
    if i % 100 == 0: 
        print(f"step {i}: x = {x}, y = {y}, direction = {direction}, p = {p}, q = {q}, type = {type}")
    
    board, reward, done, _, _= game.fake_step(i)
    if done:
        print("found")
        #save this pattern to file
        x,y, direction, p = game.dict[i]
        #example: {"n": 1, "ops": [{"x": 1, "y": 1, "s": 1, "p": 1}]}
        with open('answer.json', 'w') as f:
            json.dump({"n": 1, "ops": [{"x": x, "y": y, "s": direction, "p": p}]}, f, indent=4)
        break
    if i % 3000 == 0:
        print(board)

else: print("not found")
# for i in question:
    
#     if i == 'question_data':
#         #convert question_data to json
#         question_data = json.loads(question[i])
#         for j in question_data:
#             print(j)
#             #create a file name j and save it to j.json
#             with open(j + '.json', 'w') as f:
#                 json.dump(question_data[j], f, indent=4)
#     else:
#         print(i, question[i])

# solve question
def solve(question):
    _, _, start_board, end_board, general_patterns = get_info(question)
    m = start_board.shape[0]
    n = start_board.shape[1]
    game = Game(m, n, 20, start_board, end_board, general_patterns)
    print(len(game.dict))
    for i in range(0,m):
        if(game.grid.board[i][0] != game.final_grid.board[i][0]):
            #way 1: move horizontal
            p = m - i
            for q in range(0, n):
                pass
    return {"n": 1, "ops": [{"x": 1, "y": 1, "s": 1, "p": 1}]}


# steps = solve(question)

# # send your answer to server
# payload = {"question_id": question_id, "answer_data": steps}
# res = requests.post(f"{url}/answer", json=payload, headers=headers).json()

# #  get your answer id
# answer_id = res["id"]

# # get your answer and score from server
# answer = requests.get(f"{url}/answer/{answer_id}", headers=headers).json()
# score_data = json.loads(answer["score_data"])
# print("final score:", score_data["final_score"])

f.close()