from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.events import SlotSet, FollowupAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
from actions.constants import *
from actions.utils.utils import *
from .constants import *
import logging


logger = logging.getLogger(__name__)


class ActionPreShowDetails(Action):
    """
    Checks if user is privileged enough.
    """
    def name(self) -> Text:
        return "action_pre_show_details"

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
        permission = PERMISSION_SHOW_USER_DETAILS
        granted = False
        for role in roles:
            if permission in IAM["permissions"][role]:
                granted = True
        if not granted:
            dispatcher.utter_message(response="utter_not_authorized")
            return []
        # if required details was provided with the intent, pre-fill the form slots
        details_email = next(tracker.get_latest_entity_values(EMAIL), None)
        return [
            SlotSet(ONGOING_PROCESS, SHOW_USER_DETAILS_FORM),
            SlotSet(DETAILS_EMAIL, details_email)
        ]


class ActionSubmitShowUserDetailsForm(Action):
    """
    Shows details of said user, if the logged-in user has required privilege.
    """
    def name(self) -> Text:
        return "action_submit_show_user_details_form"

    def run(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict,
    ) -> List[Dict[Text, Any]]:
        details_email = tracker.get_slot(DETAILS_EMAIL)
        if details_email is not None:
            user_details = get_user_details({COL_EMAIL: details_email})
            if len(user_details) < 1:
                dispatcher.utter_message(response="utter_no_user_found")
            else:
                if len(user_details) > 1:
                    dispatcher.utter_message(text="Multiple entries found.")
                details = ""
                for user in user_details:
                    user = mask_user_details(user)
                    details += "--------"
                    for key, value in user.items():
                        details += f"\n \n{key}:\t{value}"
                    details += "\n \n--------"
                dispatcher.utter_message(text=details)
        else:
            dispatcher.utter_message(response="utter_incomplete_details_provided")
        return [
            SlotSet(ONGOING_PROCESS, None)
        ]


class ValidateShowUserDetailsForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_show_user_details_form"

    async def required_slots(
        self,
        domain_slots: List[Text],
        dispatcher: "CollectingDispatcher",
        tracker: "Tracker",
        domain: "DomainDict",
    ) -> List[Text]:
        slots = domain_slots.copy()
        latest_intent = tracker.get_intent_of_latest_message(skip_fallback_intent=False)
        second_last_action = get_second_previous_action_name(tracker.events)
        if latest_intent == CANCEL and second_last_action != ACTION_SUBMIT_CANCEL_FORM:
            return []
        return slots
