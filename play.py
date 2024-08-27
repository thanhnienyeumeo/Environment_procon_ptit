# swagger doc: https://proconvn.duckdns.org/docs

import requests
import json


url = "https://proconvn.duckdns.org"
headers = {"Authorization": "<TOKEN_HERE>"}


# request question from server
question_id = 12
question = requests.get(f"{url}/question/{question_id}", headers=headers).json()


# solve question
def solve(question):
    return {"n": 1, "ops": [{"x": 1, "y": 1, "s": 1, "p": 1}]}


steps = solve(question)

# send your answer to server
payload = {"question_id": question_id, "answer_data": steps}
res = requests.post(f"{url}/answer", json=payload, headers=headers).json()

#  get your answer id
answer_id = res["id"]

# get your answer and score from server
answer = requests.get(f"{url}/answer/{answer_id}", headers=headers).json()
score_data = json.loads(answer["score_data"])
print("final score:", score_data["final_score"])
