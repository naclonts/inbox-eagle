import commentjson

def log_evaluation(message, evaluation):
    print('\033[92m' + f"Message ID: {message['id']} - Subject: {message['subject']}" + '\033[0m')
    print(f"Snippet: {message['snippet']}")
    print(f'Rating: {evaluation["rating"]}')
    print(f'Evaluation: {evaluation["response"]}')
    print('\n----------------\n')

def load_prompt_config():
    """Load the prompt config to get the evaluator model and settings about the user."""
    with open('prompt-config-setup.json', 'r') as file:
        prompt_config = commentjson.load(file)
    return prompt_config
