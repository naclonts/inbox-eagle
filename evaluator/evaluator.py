from dotenv import load_dotenv
import os
import openai
from mailbox import Message
import requests

load_dotenv('.environment')

openai.api_key = os.environ['OPENAI_API_KEY']

headers = {
    "Content-Type": "application/json"
}


def evaluate_message_importance(message: Message) -> str:
    return get_chatgpt_response(message)
    

def get_local_llm_response(message: Message):
    history = [
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
            "content": message['body']
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

def get_chatgpt_response(message: Message):
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
                "content": message['body']
            }
        ],
        model="gpt-4",
    )
    return chat_completion
