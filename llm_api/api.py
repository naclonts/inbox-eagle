from dotenv import load_dotenv
import os
import openai
import requests
load_dotenv('.env')

openai.api_key = os.environ['OPENAI_API_KEY']

def get_llm_response(prompt_config, prompt) -> str:
    """Returns a response from the language model based on the given prompt."""
    if prompt_config['evaluator_model'] == 'local':
        completion = get_local_llm_response(prompt_config, prompt)
    elif prompt_config['evaluator_model'][0:3] == 'gpt':
        completion = get_chatgpt_response(prompt_config, prompt)
    else:
        raise ValueError('Invalid Evaluator model ' + prompt_config['evaluator_model'])

    response = completion['choices'][0]['message']['content'].strip()
    return response

def get_local_llm_response(prompt_config, prompt):
    """
    Returns a response from a local language model using the OpenAI API format
    at port 5000 (e.g., Oobabooga).
    """
    response = requests.post(
        'http://localhost:5000/v1/chat/completions',
        headers={
            "Content-Type": "application/json"
        },
        json={
            "mode": "instruct",
            "instruction_template": "Alpaca",
            "messages": prompt,
        },
    )
    assistant_message = response.json()
    return assistant_message

def get_chatgpt_response(prompt_config, prompt):
    client = openai.OpenAI(
        api_key=os.environ.get("OPENAI_API_KEY"),
    )
    chat_completion = client.chat.completions.create(
        messages=prompt,
        model=prompt_config['evaluator_model'],
    )
    return chat_completion.model_dump()
