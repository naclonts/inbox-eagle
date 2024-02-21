# Inbox Eagle

An app that queries your emails and ranks them in importance based on which ones need a reply from you.

Configurable to use either a local LLM or an OpenAI API model.

## Getting started

1. `cp .env.example .env`
2. `cp prompt-config.example.json prompt-config-setup.json`
3. Set up GMail API credentials, and place the credentials JSON in this directory named `credentials-gmail.json`.
4. `pip install -r requirements.txt`
5. `cd client && npm ci`

## Running the script

Start by running the command line script to authorize Gmail and test the evaluation process:

```
$ python run_script.py
```

This'll save your credentials to a token.pickle file locally.

Next run the server and the front-end:

```sh
$ python start.py
```

Front-end client:

```sh
$ cd client
$ npm start
```

## Screenshots

Here's the web UI running locally:

![image](https://github.com/naclonts/inbox-eagle/assets/10605105/a8ac0c3a-55f9-4866-b155-ce5e6d891ea6)



Here's some output from running `run_script.py` via the command line: 

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



