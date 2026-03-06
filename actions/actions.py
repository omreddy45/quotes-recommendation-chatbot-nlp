# actions/actions.py
# Custom actions for the Quotes Recommendation Chatbot
# These actions can be used for dynamic quote generation
# To enable: uncomment action_endpoint in endpoints.yml
# and run: rasa run actions

from typing import Any, Text, Dict, List
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher

# Example custom action (uncomment when needed):
#
# class ActionGiveDynamicQuote(Action):
#     def name(self) -> Text:
#         return "action_give_dynamic_quote"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         intent = tracker.latest_message.get("intent", {}).get("name")
#         # Add custom logic here
#         dispatcher.utter_message(text="Here's a dynamic quote for you!")
#         return []
