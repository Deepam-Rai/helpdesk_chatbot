import os

# parameters
OTP_LENGTH = 4
EMAIL_USERNAME = "EMAIL_USERNAME"
EMAIL_PASSWORD = "EMAIL_PASSWORD"
CREDENTIALS_PARAMS = {  # logs error if these are not present in CREDENTIALS_FILE
    EMAIL_USERNAME,
    EMAIL_PASSWORD
}

# files
CREDENTIALS_FILE = "credentials.json"

# paths
APP_PATH = os.path.dirname(os.path.abspath(__file__))

# common values
TRUE = "True"
FALSE = "False"
YES = "yes"
NO = "no"

# slots
REQUESTED_SLOT = "requested_slot"

# actions
ACTION_SUBMIT_CANCEL_FORM = "action_submit_cancel_form"
