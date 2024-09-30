from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
from actions.constants import *
from actions.constants_database import *
from actions.utils.utils import *
from actions.utils.utils_database import *
from .constants import *
import logging

from ..utils.utils_database import insert_row

logger = logging.getLogger(__name__)


class ActionStartLogin(Action):
    def name(self) -> Text:
        return "action_start_login"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(response="utter_start_login")
        return []


class ActionSubmitLoginForm(Action):

    def name(self) -> Text:
        return "action_submit_login_form"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        user_name = tracker.get_slot(USER_NAME)
        if tracker.get_slot(LOGGED_IN) is True:
            dispatcher.utter_message(response="utter_login_success")
            insert_values = {
                COL_NAME: user_name,
                COL_EMAIL: tracker.get_slot(USER_EMAIL),
                COL_ACTIVITY: LOGIN,
                COL_TIME: get_timestamp()
            }
            is_inserted, row_id = insert_row(
                TABLE_LOGIN_HISTORY,
                data=insert_values,
                schema=DB_SCHEMA,
                returning_id=COL_ID
            )
            logger.debug(f"is inserted: {is_inserted}" f"table-name: {TABLE_LOGIN_HISTORY}  row_id:{row_id}")
            logger.debug(f"Logged-in: {user_name}")
        else:
            dispatcher.utter_message(response="utter_login_fail")
            logger.error(f"Log-in failed: {user_name}")
        return []


class ValidateLoginForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_login_form"

    async def extract_user_email(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict
    ) -> Dict[Text, Any]:
        if tracker.get_slot(REQUESTED_SLOT) == USER_EMAIL:
            email = next(tracker.get_latest_entity_values(EMAIL), None)
            return {USER_EMAIL: email}
        return {USER_EMAIL: tracker.get_slot(USER_EMAIL)}

    async def validate_user_email(
            self,
            slot_value: Any,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict
    ) -> Dict[Text, Any]:
        if tracker.get_slot(REQUESTED_SLOT) == USER_EMAIL:
            input_email = slot_value
            entries = retrieve_rows(
                TABLE_USERS,
                {
                    COL_EMAIL: input_email
                },
                SCHEMA_HELPDESK
            )
            if len(entries) > 0:
                return {USER_EMAIL: input_email}
            else:
                dispatcher.utter_message(response="utter_unregistered_email", email=input_email)
                return {USER_EMAIL: None}
        return {USER_EMAIL: tracker.get_slot(USER_EMAIL)}

    async def validate_user_password(
            self,
            slot_value: Any,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict
    ) -> Dict[Text, Any]:
        if tracker.get_slot(REQUESTED_SLOT) == USER_PASSWORD:
            input_pass = slot_value
            entries = retrieve_rows(
                TABLE_USERS,
                {
                    COL_EMAIL: tracker.get_slot(USER_EMAIL)
                },
                SCHEMA_HELPDESK
            )
            saved_pass = entries[-1][COL_PASSWORD]
            user_name = entries[-1][COL_NAME]
            if input_pass == saved_pass:
                return {USER_PASSWORD: input_pass, LOGGED_IN: True, USER_NAME: user_name}
            else:
                dispatcher.utter_message(response="utter_wrong_password")
                return {USER_PASSWORD: None}
        return {USER_PASSWORD: tracker.get_slot(USER_PASSWORD)}

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
        requested_slot = tracker.get_slot(REQUESTED_SLOT)
        if (
            requested_slot != USER_PASSWORD and latest_intent == CANCEL
            and second_last_action != ACTION_SUBMIT_CANCEL_FORM
        ):
            return []
        return slots
