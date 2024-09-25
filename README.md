# helpdesk_chatbot
RASA helpdesk chatbot.

## Setup
1. For sending OTPs, email account and email-app-password is required to be set in `actions/credentials.json` file. Currently, code is working with gmail accounts, and gmail **app-password** is used instead of account password itself. Check [this guide](https://support.google.com/accounts/answer/185833?hl=en) to obtain app-password for your account.
2. Uses additional [rasa/duckling](https://hub.docker.com/r/rasa/duckling) container for entity extraction.  

Capabilities:
1. login, logout user on demand
   1. Email OTP verificatoin implemented.
2. Database Integration:
   1. Login/logout activities are stored in hosted [PostgreSQL](https://www.postgresql.org/) database.
3. Cancelling ongoing process - login, logout, etc.
4. Two-stage handling for out-of-scope user inputs. 
   1. On consecutive second nlu_fallback, logs the latest_message to `actions/logs/nlu_fallback.json` for future reference.

## Run
Project is dockerized.  
Commands to run:
```shell
make build; # for the first time

make train-redeploy-logs;

# to serve a simple UI locally
make ui;

# to view action logs
make action-logs;
```
