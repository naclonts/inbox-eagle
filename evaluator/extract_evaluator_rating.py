
from evaluator import prompt_writer
from evaluator.types import MessageEvaluation
from llm_api.api import get_llm_response


def extract_rating_from_evaluation(prompt_config, evaluation_content: str) -> float:
    """
    Extracts the numeric rating from an evaluation message using an LLM.

    If a numeric rating isn't found, returns -1.
    """
    prompt = prompt_writer.get_rating_extraction_prompt(prompt_config, evaluation_content)
    response = get_llm_response(prompt_config, prompt)
    try:
        return float(response)
    except ValueError:
        # It's possible the input text didn't contain a rating, or the LLM hallucinated in its response.
        # In either case, return -1, while logging the input and output.
        print(f'\n*** Error parsing response for rating: {response}, in response to eval:\n\n"{evaluation_content}"\n ***\n')
        return -1
