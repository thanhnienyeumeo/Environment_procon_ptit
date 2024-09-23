# swagger doc: https://proconvn.duckdns.org/docs

import requests
import json


url = "https://proconvn.duckdns.org"
headers = {"Authorization": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MjIsIm5hbWUiOiJQVElUIiwiaXNfYWRtaW4iOmZhbHNlLCJpYXQiOjE3MjcwODE4NzAsImV4cCI6MTcyNzI1NDY3MH0.q_v10XqiMVC4q44Tcw3xewdjDPzKIct7eeAFP_0Tvtg"}


# request question from server
question_id = 72
question = requests.get(f"{url}/question/{question_id}", headers=headers).json()
#save question data to example.json
with open('example.json', 'w') as f:
    json.dump(question, f, indent=4)

for i in question:
    
    if i == 'question_data':
        #convert question_data to json
        question_data = json.loads(question[i])
        for j in question_data:
            print(j)
            #create a file name j and save it to j.json
            with open(j + '.json', 'w') as f:
                json.dump(question_data[j], f, indent=4)
    else:
        print(i, question[i])

# solve question
def solve(question):
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
