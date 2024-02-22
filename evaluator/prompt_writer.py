
def get_message_evaluation_prompt(prompt_config, message_content: str):
    """
    Returns a prompt with a series of messages with role + content.
    """

    return [
        {
            "role": "system",
            "content": f"""
                ### Objective:
                You are an executive assistant working a person named {prompt_config['full_name']} who is a {prompt_config['my_role']}.
                {get_company_clause(prompt_config)}

                You receive email messages, and evaluate how important they are for {prompt_config['full_name']} on a scale of 1 to 10.
                Summarize and evaluate the email, listing any specific facts that are important.
                At the end of your response, put the number of the importance of the email on a scale of 1 to 10.
                {get_rating_criteria_clause(prompt_config)}

                ### Example emails with importance level:

                {get_example_evaluations(prompt_config)}

            """
        },
        {
            "role": "user",
            "content": message_content,
        }
    ]

def get_company_clause(prompt_config):
    """Returns a string with the company clause if the company name is defined."""
    company_name = prompt_config.get("company_name", "")
    if company_name:
        return f"I work at {prompt_config['company_name']}, which is: {prompt_config['company_description']}"
    return ""

def get_rating_criteria_clause(prompt_config):
    """Returns a string with the rating criteria clause if the rating criteria is defined."""
    rating_criteria = prompt_config.get("rating_criteria", "")
    if rating_criteria:
        return f"Use the following criteria to determine the importance level: {prompt_config['rating_criteria']}"
    return ""

def get_example_evaluations(prompt_config):
    """Returns a string with example evaluations if they are defined."""
    example_evaluations = prompt_config.get("example_evaluations", [])
    if example_evaluations:
        return "\n".join([f"- {example}" for example in example_evaluations])
    return ""

def get_rating_extraction_prompt(prompt_config, evaluation_content: str):
    """Returns a prompt that asks the LLM to extract the numeric evaluation rating."""
    return [
        {
            "role": "system",
            "content": f"""
                Take the importance level from the evaluation and return it.
                Return only the number, and do not add any text, words, or punctuation.

                Example input: This message is fairly important, so I assigned it an 7.0 importance level.
                Example responses: 7.0
            """
        },
        {
            "role": "user",
            "content": evaluation_content,
        }
    ]
