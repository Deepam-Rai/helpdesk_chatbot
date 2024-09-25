from typing import Text
from rasa_sdk import Action, Tracker
from rasa_sdk.events import UserUtteranceReverted
from rasa_sdk.executor import CollectingDispatcher
from actions.utils.utils import *
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
        logger.warning(f"latest_message: {tracker.latest_message.get('text')}")
        if second_last_action != self.name():
            # nlu_fallback first time
            dispatcher.utter_message(response="utter_ask_rephrase")
        else:
            # nlu_fallback consecutive second time
            dispatcher.utter_message(response="utter_handle_fallback")
            log_fallback(tracker.latest_message)
        return [
            UserUtteranceReverted(),
        ]
