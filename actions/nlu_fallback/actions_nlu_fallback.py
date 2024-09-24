from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.events import Restarted, AllSlotsReset, UserUtteranceReverted, SlotSet
from rasa_sdk.executor import CollectingDispatcher
from actions.utils import *
from .constants import *
import logging


logger = logging.getLogger(__name__)


class ActionHandleFallback(Action):

    def name(self) -> Text:
        return "action_handle_fallback"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        second_last_action = get_previous_action_name(tracker.events, log=False)
        logger.warning(f"Inside {self.name()}")
        logger.warning(f"latest_message: {tracker.latest_message}")
        if second_last_action != self.name():
            # nlu_fallback first time
            dispatcher.utter_message(response="utter_ask_rephrase")
        else:
            # nlu_fallback consecutive second time
            dispatcher.utter_message(response="utter_handle_fallback")
        return [
            UserUtteranceReverted(),
        ]
