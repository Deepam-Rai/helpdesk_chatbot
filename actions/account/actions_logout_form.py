from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.events import SlotSet, AllSlotsReset, Restarted
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
from actions.constants import *
from .constants import *
import logging

from ..utils import get_second_previous_action_name

logger = logging.getLogger(__name__)


class ActionAskLogoutConfirm(Action):

    def name(self) -> Text:
        return "action_ask_logout_confirm"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        buttons = [
            {
                "title": "Log me out",
                "payload": "/affirm"
            },
            {
                "title": "Keep me logged in",
                "payload": "/deny"
            }
        ]
        dispatcher.utter_message(response="utter_ask_logout_confirm", buttons=buttons)


class ActionSubmitLogoutForm(Action):

    def name(self) -> Text:
        return "action_submit_logout_form"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        return_vals = [
            SlotSet(LOGOUT_CONFIRM, None)
        ]
        logout_confirm = tracker.get_slot(LOGOUT_CONFIRM)
        if logout_confirm:
            dispatcher.utter_message(response="utter_logged_out")
            return_vals += [
                AllSlotsReset(),
                Restarted()
            ]
        else:
            dispatcher.utter_message(response="utter_logout_cancelled")
        return return_vals


class ValidateLogoutForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_logout_form"

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
