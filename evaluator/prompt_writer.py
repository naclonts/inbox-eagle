
def get_message_evaluation_prompt(prompt_config, message_content: str):
    """
    Returns a prompt with a series of messages with role + content.
    """
    return [
        {
            "role": "system",
            "content": f"""
                ### Objective:
                You are an executive assistant working for me, a person named {prompt_config['full_name']} who is a {prompt_config['my_role']}.
                I work at {prompt_config['company_name']}, which is: {prompt_config['company_description']} .
                You receive email messages, and evaluate how important they are for {prompt_config['full_name']} to address on a scale of 1 to 10.
                Evaluate the email, and at the very end of your response, put the number of the importance of the email on a scale of 1 to 10.
                Emails are more important if they are urgent, or addressed to me and expecting a response.
                Do not repeat the contents of the email message you received.
                Do not add any text, words, or punctuation after the importance level.

                ### Example responses:
                We are waiting on a response from {prompt_config['full_name']}, and we can't continue work on our end until then. Importance Level: 8
                This is an update on world news, covering news related to your industry. Importance Level: 2
                Your payment for Digital Services has been received. Importance Level: 3
                Here's your weekly overview of product usage for last Week! Importance Level: 2
                Your payment is past due and we are about to suspend your account. Importance Level: 9
            """
        },
        {
            "role": "user",
            "content": message_content,
        }
    ]


def get_rating_extraction_prompt(prompt_config, evaluation_content: str):
    """Returns a prompt that asks the LLM to extract the numeric evaluation rating."""
    return [
        {
            "role": "system",
            "content": f"""
                Take the importance level from the evaluation and put it at the very end of your response.
                Return only the number, and do not add any text, words, or punctuation.

                Example input: This message is fairly important, so I assigned it an 8.0 importance level.
                Example responses: 8.0
            """
        },
        {
            "role": "user",
            "content": evaluation_content,
        }
    ]
