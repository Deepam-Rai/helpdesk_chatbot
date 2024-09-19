# helpdesk_chatbot
RASA helpdesk chatbot.

## Setup
1. For sending OTPs, email account and email-app-password is required to be set in `actions/credentials.json` file. Currently, code is working with gmail accounts, and gmail **app-password** is used instead of account password itself. Check [this guide](https://support.google.com/accounts/answer/185833?hl=en) to obtain app-password for your account.
2. Uses additional [rasa/duckling](https://hub.docker.com/r/rasa/duckling) container for entity extraction.  

Capabilities:
1. login user on demand
   2. Email OTP verificatoin implemented.


## Run
Project is dockerized.
```shell
make build;

make train-redeploy-logs;
make action-logs;
```
