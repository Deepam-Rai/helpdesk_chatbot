from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet, FollowupAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
from actions.constants import *
from .constants import *
import logging


logger = logging.getLogger(__name__)


class ActionPreCancel(Action):
    """
    Checks if there is really anything to cancel.
    Handles cancel_form accordingly.
    """
    def name(self) -> Text:
        return "action_pre_cancel"

    def run(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict,
    ) -> List[Dict[Text, Any]]:
        return_vals = []
        active_loop = tracker.active_loop.get('name')
        if active_loop is not None:
            return_vals += [
                SlotSet(TO_CANCEL, active_loop)
            ]
        else:
            dispatcher.utter_message(response="utter_nothing_to_cancel")
            return_vals += [
                SlotSet(TO_CANCEL, None)
            ]
        return return_vals


class ActionAskCancelConfirm(Action):
    def name(self) -> Text:
        return "action_ask_confirm_cancel"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> List[Dict[Text, Any]]:
        btns = [
            {
                "title": "Cancel",
                "payload": "/affirm"
            },
            {
                "title": "Do not cancel",
                "payload": "/deny"
            }
        ]
        dispatcher.utter_message(response="utter_ask_confirm_cancel", buttons=btns)
        return []


class ActionSubmitCancelForm(Action):
    def name(self) -> Text:
        return "action_submit_cancel_form"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> List[Dict[Text, Any]]:
        return_vals = [
            SlotSet(TO_CANCEL, None),
            SlotSet(CONFIRM_CANCEL, None)
        ]
        to_cancel = tracker.get_slot(TO_CANCEL)
        if to_cancel is not None:
            confirm_cancel = tracker.get_slot(CONFIRM_CANCEL)
            if confirm_cancel is True:
                dispatcher.utter_message(response="utter_cancel_success")
                return_vals += [SlotSet(REQUESTED_SLOT, None)]
            else:
                dispatcher.utter_message(response="utter_cancel_fail")
                return_vals += [
                    FollowupAction(to_cancel)
                ]
        return return_vals
