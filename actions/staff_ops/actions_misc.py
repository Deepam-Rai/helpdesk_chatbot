from typing import Any, Text, Dict, List

from prettytable import PrettyTable
from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet, FollowupAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
from actions.constants import *
from actions.utils.utils import *
from .constants import *
import logging


logger = logging.getLogger(__name__)


class ActionListUsers(Action):
    """
    Lists the users, if the logged-in user has required privilege.
    """
    def name(self) -> Text:
        return "action_list_users"

    def run(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict,
    ) -> List[Dict[Text, Any]]:
        logged_in = tracker.get_slot(LOGGED_IN)
        if not logged_in:
            dispatcher.utter_message(response="utter_login_first")
            return []
        user_mail = tracker.get_slot(USER_EMAIL)
        roles = get_user_role(user_mail)
        permission = PERMISSION_LIST_USERS
        granted = False
        for role in roles:
            if permission in IAM["permissions"][role]:
                granted = True
        if not granted:
            dispatcher.utter_message(response="utter_not_authorized")
            return []
        users_list = get_users_list()
        text = "Users list:\n"
        buttons = []
        for user in users_list:
            btn = {
                "title": f"{user[COL_NAME]} | {user[COL_EMAIL]}",
                "payload": f"/show_details{{\"email\":\"{user[COL_EMAIL]}\"}}"
            }
            buttons.append(btn)
        dispatcher.utter_message(text=text, buttons=buttons)
        return []
