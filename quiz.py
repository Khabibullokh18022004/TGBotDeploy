import requests
from dotenv import load_dotenv
import os
import re

load_dotenv()
openai_api_key = os.getenv('openai_api_key')
telegram_key = os.getenv('telegram_key')


def quiz(text, lang, q_type):
    openai_url = "https://api.openai.com/v1"

    headers = {"Authorization": f"Bearer {openai_api_key}"}

    if text == '.':
        return None

    url = f"{openai_url}/chat/completions"

    data = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {
                "role": "user",
                "content": f'''
Create a programming quiz in the language '{lang}', specifically about the topic '{text}'. 
Generate a quiz with the following specifications:
if {q_type} is multiple:
    - Format the quiz as {q_type}
    - Include five questions related to the topic '{text}'.
    - Each question should have four answers: three incorrect and one correct answer. 
    - Ensure that all answers are unique and there are no duplicate options.
    - Format the output in YAML. Below is an example of the desired format:
    
questions:
  - id: 1
    q: "Insert the first question about {text} here?"
    a:
      - "Incorrect answer 1"
      - "Incorrect answer 2"
      - "Incorrect answer 3"
      - correct: "Correct answer"
  - id: 2
    q: "Insert the second question about {text} here?"
    a:
      - "Incorrect answer 1"
      - "Incorrect answer 2"
      - "Incorrect answer 3"
      - correct: "Correct answer"
  - id: 3
    q: "Insert the third question about {text} here?"
    a:
      - "Incorrect answer 1"
      - "Incorrect answer 2"
      - "Incorrect answer 3"
      - correct: "Correct answer"
    
if {q_type} is true_false:
    - Format the quiz as {q_type}
    - Include five questions related to the topic '{text}'.
    - Each question should have two answers True and False. 
    - Only of them is correct, either True or False and you must assign the one that's
            correct (you know pretty well the answer) with the YAML format (either - correct: "True", - correct: "False")
    - Format the output in YAML. Below is an example of the desired format:
    
questions:
  - id: 1
    q: "Insert the first question about {text} here?"
    a:
      - "True"
      - "False"
  - id: 2
    q: "Insert the second question about {text} here?"
    a:
      - "True"
      - "False"
  - id: 3
    q: "Insert the third question about {text} here?"
    a:
      - "True"
      - "False"
'''
            }
        ]
    }

    response = requests.post(url, json=data, headers=headers)

    print("Status Code", response.status_code)
    chatgpt_response = response.json()["choices"][0]["message"]["content"]
    print("Response from LLM\n", chatgpt_response)

    pattern = r'questions:\n(.*?)(?=```|$)'
    match = re.search(pattern, chatgpt_response, re.DOTALL)
    if match:
        chatgpt_response = match.group(0)
    else:
        print('No questions section found')

    if lang == 'russian':
        with open('questions.yaml', 'w', encoding='UTF-8') as file:
            file.write(chatgpt_response)
            print('YAML file saved successfully')
    else:
        with open('questions.yaml', 'w') as file:
            file.write(chatgpt_response)
            print('YAML file saved successfully')
