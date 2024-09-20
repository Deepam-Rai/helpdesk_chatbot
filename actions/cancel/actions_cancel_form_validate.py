from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
from .constants import *
import logging


logger = logging.getLogger(__name__)


class ValidateCancelForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_cancel_form"

    async def required_slots(
        self,
        domain_slots: List[Text],
        dispatcher: "CollectingDispatcher",
        tracker: "Tracker",
        domain: "DomainDict",
    ) -> List[Text]:
        slots = domain_slots.copy()
        to_cancel = tracker.get_slot(TO_CANCEL)
        if to_cancel is None:
            slots = []
        return slots
