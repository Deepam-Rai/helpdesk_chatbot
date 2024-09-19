from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict

from actions.constants import *
from .constants import *
import logging


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
        if tracker.get_slot(LOGGED_IN) is True:
            dispatcher.utter_message(response="utter_already_logged_in")
        else:
            dispatcher.utter_message(response="utter_start_login")
        return []


class ActionAskOTP(Action):

    def name(self) -> Text:
        return "action_ask_login_otp"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(response="utter_otp_shared")
        dispatcher.utter_message(response="utter_ask_login_otp")
        sent_login_otp = "1234"
        return [
            SlotSet(SENT_LOGIN_OTP, sent_login_otp)
        ]


class ActionSubmitLoginForm(Action):

    def name(self) -> Text:
        return "action_submit_login_form"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        if tracker.get_slot(LOGGED_IN) is True:
            dispatcher.utter_message(response="utter_login_success")
        else:
            dispatcher.utter_message(response="utter_login_fail")
        return []


class ValidateLoginForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_login_form"

    async def extract_login_otp(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict
    ) -> Dict[Text, Any]:
        if tracker.get_slot(REQUESTED_SLOT) == LOGIN_OTP:
            otp = next(tracker.get_latest_entity_values(OTP), None)
            return {LOGIN_OTP: otp}
        return {LOGIN_OTP: tracker.get_slot(LOGIN_OTP)}

    async def validate_login_otp(
            self,
            slot_value: Any,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict
    ) -> Dict[Text, Any]:
        if tracker.get_slot(REQUESTED_SLOT) == LOGIN_OTP:
            input_otp = slot_value
            sent_otp = tracker.get_slot(SENT_LOGIN_OTP)
            logger.debug(f"input_otp: {input_otp} type:{type(input_otp)}")
            logger.debug(f"input_otp: {sent_otp} type:{type(sent_otp)}")
            if input_otp == sent_otp:
                return {LOGIN_OTP: input_otp, LOGGED_IN: True}
            else:
                dispatcher.utter_message(response="utter_entered_wrong_otp")
                return {LOGIN_OTP: None}
        return {LOGIN_OTP: tracker.get_slot(LOGIN_OTP)}
