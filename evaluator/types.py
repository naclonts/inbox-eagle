from mail_client.get_mail import Message
from typing import TypedDict

MessageEvaluation = TypedDict('MessageEvaluation', {
    'message': Message,
    'rating': float,
    'evaluation': str,
    'model': str,
})
