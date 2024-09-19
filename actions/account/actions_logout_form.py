from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.events import SlotSet, AllSlotsReset, Restarted
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
from actions.constants import *
from .constants import *
import logging


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
