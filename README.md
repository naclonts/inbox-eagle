# Inbox Eagle

A script that queries your emails and ranks them in importance based on which ones need a reply from you.

Configurable to use either a local LLM or an OpenAI API model.

## Getting started

1. `cp .env.example .env`
2. `cp prompt-config.example.json prompt-config.json`
3. Set up GMail API credentials, and place the credentials JSON in this directory named `credentials-gmail.json`.
4. `pip install -r requirements.txt`

## Running the script

`$ python start.py`

The script currently evaluates unread emails received within the last X days.

Example output:

```
-------- Evaluating messages (2) --------

Message ID: 18d71921aacafc7a - Subject: ['Your utilities statement is overdue']
Snippet: Please submit payment for $100.00 for your electric bill. Kindly, City Utilities
Evaluation: This appears to be a payment that needs to be submitted. Therefore, this is given an importance level of 8.0.
Rating: 8.0

----------------

Message ID: 18d659d34ec34e35 - Subject: ['Boeing’s AI Wings It']
Snippet: Plus: Microsoft's AI Explains Itself; Apple's Sixth Sense
Rating: 2.0
Evaluation: Interesting patent. No urgent response necessary. Importance Level: 2
```



