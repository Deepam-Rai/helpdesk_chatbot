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


class ActionStartSignup(Action):
    def name(self) -> Text:
        return "action_start_signup"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(response="utter_start_signup")
        return [
            SlotSet(USER_NAME, None),
            SlotSet(USER_EMAIL, None),
            SlotSet(LOGGED_IN, False)
        ]


class ActionAskSignupOTP(Action):

    def name(self) -> Text:
        return "action_ask_signup_otp"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        return_vals = []
        if tracker.get_slot(SENT_SIGNUP_OTP) is None:
            dispatcher.utter_message(response="utter_otp_shared")
            dispatcher.utter_message(response="utter_ask_signup_otp")
            sent_login_otp = send_otp(
                receiver_email=tracker.get_slot(USER_EMAIL),
                receiver_name=tracker.get_slot(USER_NAME)
            )
            return_vals.append(SlotSet(SENT_SIGNUP_OTP, sent_login_otp))
        return return_vals


class ActionSubmitSignupForm(Action):

    def name(self) -> Text:
        return "action_submit_signup_form"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        user_name = tracker.get_slot(USER_NAME)
        if tracker.get_slot(LOGGED_IN) is True:
            dispatcher.utter_message(response="utter_signup_success")
            insert_values = {
                COL_NAME: user_name,
                COL_EMAIL: tracker.get_slot(USER_EMAIL),
                COL_ROLE: tracker.get_slot(USER_ROLE),
                COL_PASSWORD: tracker.get_slot(SIGNUP_PASSWORD),
                COL_SIGNUP_TIME: get_timestamp()
            }
            is_inserted, row_id = insert_row(
                TABLE_USERS,
                data=insert_values,
                schema=DB_SCHEMA,
                returning_id=COL_ID
            )
            logger.debug(f"is inserted: {is_inserted}" f"table-name: {TABLE_USERS}  row_id:{row_id}")
            logger.debug(f"Signed-up: {user_name}")
        else:
            dispatcher.utter_message(response="utter_signup_fail")
            logger.error(f"Signup failed: {user_name}")
        return []


class ValidateSignupForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_signup_form"

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
                dispatcher.utter_message(response="utter_already_registered_email", email=input_email)
                return {USER_EMAIL: None}
            else:
                return {USER_EMAIL: input_email}
        return {USER_EMAIL: tracker.get_slot(USER_EMAIL)}

    async def extract_signup_otp(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict
    ) -> Dict[Text, Any]:
        if tracker.get_slot(REQUESTED_SLOT) == SIGNUP_OTP:
            otp = next(tracker.get_latest_entity_values(OTP), None)
            return {SIGNUP_OTP: otp}
        return {SIGNUP_OTP: tracker.get_slot(SIGNUP_OTP)}

    async def validate_signup_otp(
            self,
            slot_value: Any,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict
    ) -> Dict[Text, Any]:
        if tracker.get_slot(REQUESTED_SLOT) == SIGNUP_OTP:
            input_otp = slot_value
            sent_otp = tracker.get_slot(SENT_SIGNUP_OTP)
            if input_otp == sent_otp:
                return {SIGNUP_OTP: input_otp, LOGGED_IN: True}
            else:
                dispatcher.utter_message(response="utter_entered_wrong_otp")
                return {SIGNUP_OTP: None}
        return {SIGNUP_OTP: tracker.get_slot(SIGNUP_OTP)}

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
