# #######################################################
#                     common
# slots
from actions.user_ops.constants import (
    USER_EMAIL,
    USER_NAME,
    USER_ROLE,
    LOGGED_IN,
)

# ########################################################
#                     list_users
# intents
LIST_USERS = "list_users"
# actions
ACTION_LIST_USERS = "action_list_users"

# ########################################################
#                   show_user_details
SHOW_USER_DETAILS_FORM = "show_user_details_form"
# intents
SHOW_USER_DETAILS = "show_user_details"
# slots
DETAILS_EMAIL = "details_email"
# actions
ACTION_PRE_SHOW_DETAILS = "action_pre_show_details"
