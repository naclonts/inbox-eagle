
def get_message_evaluation_prompt(prompt_config, message_content: str) -> str:
    """
    Returns a prompt with a series of messages with role + content.
    """
    return [
        {
            "role": "system",
            "content": f"""
                You are an executive assistant working for me, a person named {prompt_config['full_name']} who is a {prompt_config['my_role']}.
                I work at {prompt_config['company_name']}, which is: {prompt_config['company_description']} .
                You receive email messages, and evaluate how important they are for {prompt_config['full_name']} to address on a scale of 1 to 10.
                Evaluate the email, and at the very end of your response, put the number of the importance of the email on a scale of 1 to 10.
                Do not add any text after the importance level.

                Example response: This email is important because it is waiting for a response, and the sender seems urgent. Importance Level: 8
            """
        },
        {
            "role": "user",
            "content": message_content,
        }
    ]
