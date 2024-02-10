
from evaluator import prompt_writer
from evaluator.types import MessageEvaluation
from llm_api.api import get_llm_response


def extract_rating_from_evaluation(prompt_config, evaluation_content: str) -> float:
    """Uses an LLM to extract the numeric rating from the evaluation message."""
    prompt = prompt_writer.get_rating_extraction_prompt(prompt_config, evaluation_content)
    response = get_llm_response(prompt_config, prompt)
    try:
        return float(response)
    except ValueError:
        print(f'\n*** Error parsing response for rating: {response} ***\n')
        return -1
