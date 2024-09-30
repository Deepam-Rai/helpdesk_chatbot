
----

<div align="center">
  <img src="https://img.shields.io/badge/Rasa-5A17EE?logo=rasa&logoColor=fff&style=plastic" alt="Rasa Badge" height="22">
  <img src="https://img.shields.io/badge/PostgreSQL-4169E1?logo=postgresql&logoColor=fff&style=plastic" alt="PostgreSQL Badge" height="22">
  <img src="https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=fff&style=plastic" alt="Docker Badge" height="22">
  <img src="https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=fff&style=plastic" alt="Python Badge" height="22">
</div>

----
# helpdesk_chatbot
[RASA(OpenSource)](https://rasa.com/docs/rasa/#rasa-open-source) helpdesk chatbot.


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
   4. list users
      1. Only users with required access can execute.
   5. show user details
      1. Only users with required access can execute.
    
2. Messaging platforms integration:
   1. Telegram integration
3. Database Integration([PostgreSQL](https://www.postgresql.org/) database):
   1. Login/logout activities stored.
   2. User details stored.
4. Access Management:
   1. Users have assigned roles and each role has different set of access permissions suited to their needs.
   2. Config file: `actions/IAM.json`
5. Cancelling ongoing process - login, logout, etc.
6. Two-stage handling for out-of-scope user inputs. 
   1. On 1st fallback: Asks user to rephrase their sentence.
   2. If bot fails to recognize even after 1st fallback: Sends appropriate utter to user and logs the latest_message to `actions/logs/nlu_fallback.json` for future reference.
  

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

Telegram integration([tutorial](https://youtu.be/QuyWEbKMzcA?si=g8Lwcys52gwt48o5)):
```shell
# 1. Start ngrok and expose the rasa-core-server to public internet
make ngrok;
# 2. Copy the ngrok url and put in "telegram" section of `credentials.yml`, after uncommenting that section
# 3. Fill in the required token, verify id fields too
# 4. Start the bot as usual
make train-redeploy-logs
# 5. Send usual messages from your telegram bot
```

----
# RASA features used

| Feature                 | Used in                                                                                     |
|-------------------------|---------------------------------------------------------------------------------------------|
| API Integrations        | 1. Telegram integration.<br/>2. Database - PostgreSQL integration.                          |
| Customized pipeline | Used pipelines pipeline components suited for the usecase: spacy components, duckling, etc. |
| Handling `nlu_fallback` | Implemented custom two-stage-fallback.                                                      |
| Forms                   | Typical procedures are implemented as forms.                                                |
| Custom Actions          | Used in forms and other misc actions. Includes `validation` actions as well.                |
| Rules, stories, slots.  | Part and parcel of using and integrating forms.                                             |


----
# References
- Telegram integration:
  - [Droid City](https://www.youtube.com/@DroidCity) : [Integrate Rasa With Telegram Chatbot](https://youtu.be/QuyWEbKMzcA?si=w6HU4dkwmBY--hZz)
  - [Official rasa docs](https://rasa.com/docs/rasa-pro/connectors/telegram/).
- 
