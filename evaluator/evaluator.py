from dotenv import load_dotenv
import os
import openai
from mailbox import Message
import requests

load_dotenv('.environment')

EVALUATOR_MODEL = 'gpt-3.5-turbo'
openai.api_key = os.environ['OPENAI_API_KEY']


headers = {
    "Content-Type": "application/json"
}


def evaluate_message_importance(message: Message) -> str:
    # limit the message to the first and last 2000 characters
    content = message['body'][:2000] + '\n...\n' + message['body'][-2000:]

    if EVALUATOR_MODEL == 'local':
        return get_local_llm_response(content)

    elif EVALUATOR_MODEL[0:3] == 'gpt':
        return get_chatgpt_response(content)

    raise ValueError('Invalid Evaluator model')


def get_local_llm_response(content: str):
    history = [
        {
            "role": "system",
            "content": """
                You are an executive assistant working for a Software Engineering Manager named Nathan Clonts.
                You receive email messages, and evaluate how important they are for Nathan Clonts to address on a scale of 1 to 10.
                Evaluate the email, and at the very end of your response, put the number of the importance of the email on a scale of 1 to 10.
                Do not add any text after the importance level.

                Example response: This email is important because it is waiting for a response, and the sender seems urgent. Importance Level: 8
            """
        },
        {
            "role": "user",
            "content": content,
        }
    ]

    response = requests.post(
        'http://localhost:5000/v1/chat/completions',
        headers=headers,
        json={
            "mode": "instruct",
            "instruction_template": "Alpaca",
            "messages": history,
        },
    )
    assistant_message = response.json()['choices'][0]['message']['content']
    return assistant_message

def get_chatgpt_response(content: str):
    client = openai.OpenAI(
        api_key=os.environ.get("OPENAI_API_KEY"),
    )
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": """
                    You are an executive assistant working for a Software Engineering Manager named Nathan Clonts.
                    You receive email messages, and evaluate how important they are for Nathan Clonts to address on a scale of 1 to 10.
                    Evaluate the email, and at the very end of your response, put the number of the importance of the email on a scale of 1 to 10.

                    Example response: This email is important because it is waiting for a response, and the sender seems urgent. Importance Level: 8
                """
            },
            {
                "role": "user",
                "content": content,
            }
        ],
        model=EVALUATOR_MODEL,
    )
    return chat_completion
