# Inbox Eagle

An app that queries your unread emails and ranks them in importance based on which ones need a reply from you.

Configurable to use either a local LLM or an OpenAI API model.

## Getting started

1. `cp .env.example .env`
2. `cp prompt-config.example.json prompt-config-setup.json`
3. Set up GMail API credentials, and place the credentials JSON in this directory named `credentials-gmail.json`.
4. `pip install -r requirements.txt`
5. `cd client && npm ci`

## Running the script

Run the command line script, which authorizes Gmail and runs the evaluation process:

```sh
$ python run_script.py
```

This will save your Gmail credentials to a token.pickle file locally.

Run the server:

```sh
$ python start.py
```

Run the front-end client:

```sh
$ cd client
$ npm start
```

## Screenshots

Web UI:

![image](https://github.com/naclonts/inbox-eagle/assets/10605105/a8ac0c3a-55f9-4866-b155-ce5e6d891ea6)



Output from `run_script.py` command line script: 

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



