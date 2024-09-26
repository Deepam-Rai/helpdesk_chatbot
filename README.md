----

<div align="center">
  <img src="https://img.shields.io/badge/Rasa-5A17EE?logo=rasa&logoColor=fff&style=plastic" alt="Rasa Badge" height="22">
  <img src="https://img.shields.io/badge/PostgreSQL-4169E1?logo=postgresql&logoColor=fff&style=plastic" alt="PostgreSQL Badge" height="22">
  <img src="https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=fff&style=plastic" alt="Docker Badge" height="22">
  <img src="https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=fff&style=plastic" alt="Python Badge" height="22">
</div>


# helpdesk_chatbot
RASA helpdesk chatbot.


Capabilities:
1. Typical procedures:
   1. signup
      1. Needs name, email, user role, new password.
      2. Email OTP verification.
      3. Doesn't allow already registered users.
      4. User details saved in database.
   2. login
      1. Needs email, password.
      2. Password crosschecked with set password in database.
      2. Only allows registered users.
   3. logout
2. Database Integration([PostgreSQL](https://www.postgresql.org/) database):
   1. Login/logout activities stored.
   2. User details stored.
3. Cancelling ongoing process - login, logout, etc.
4. Two-stage handling for out-of-scope user inputs. 
   1. On consecutive second nlu_fallback, logs the latest_message to `actions/logs/nlu_fallback.json` for future reference.
  

## Setup & Run
1. For sending OTPs, email account and email-app-password is required to be set in `actions/credentials.json` file. Currently, code is working with gmail accounts, and gmail **app-password** is used instead of account password itself. Check [this guide](https://support.google.com/accounts/answer/185833?hl=en) to obtain app-password for your account.
2. Uses additional [rasa/duckling](https://hub.docker.com/r/rasa/duckling) container for entity extraction.  


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
