from mail_client.get_mail import Message
from typing import TypedDict

# MessageEvaluation contains the evaluation of an email message.
MessageEvaluation = TypedDict('MessageEvaluation', {
    # the original email
    'message': Message,
    # the rating of the email
    'rating': float,
    # an explanation of the rating
    'evaluation': str,
    # the LLM used to evaluate the email, based on the provided prompt config
    'model': str,
})
