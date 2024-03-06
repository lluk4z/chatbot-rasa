# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []
import pandas as pd

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import pandas as pd
import random
import datetime


from rasa.actions.action import Action
from rasa.events.slot_mappings import SlotMapping
from rasa.events.slot_set import SlotSet
from rasa.slots import Slot

class ActionRecommendMusic(Action):
    def name(self):
        return "action_recommend_music"

    @staticmethod
    def required_slots():
        return ["genre"]

    def slot_mappings(self) -> Dict[Text, List[SlotMapping]]:
        return {
            "genre": [SlotMapping(var_name="genre", intent="inform_genre")]
        }

    def run(self, dispatcher, tracker, domain):
        # Get the user's preferred genre from the user's session data
        user_preferred_genre = tracker.latest_message.get('metadata', {}).get('genre', None)

        # Check if the user has specified a genre
        if user_preferred_genre is None:
            # If not, ask the user to specify a genre
            dispatcher.utter_message(text="I'd be happy to recommend a song for you. Could you please tell me your favorite music genre?")
            return [SlotSet("genre", None)]

        # Get the list of genres and songs from the domain
        genres = domain['genres']
        musicas = domain['musicas']

        # Find the list of songs for the user's preferred genre
        user_preferred_genre_songs = musicas[user_preferred_genre]

        # Choose a random song from the list of matching songs
        chosen_song = random.choice(user_preferred_genre_songs)

        # Construct and send a message recommending the chosen song
        dispatcher.utter_message(text=f"I recommend listening to {chosen_song} in the genre '{user_preferred_genre}'!")

        return [SlotSet("genre", user_preferred_genre)]

class ActionAskGenrePreference(Action):
    def name(self) -> Text:
        return "utter_ask_genre_preference"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(text="Você tem algum gênero musical específico em mente?")
        return []
    
class ActionGreet(Action):
    def name(self) -> Text:
        return "utter_greet"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Obter o horário atual
        now = datetime.datetime.now()
        current_hour = now.hour

        # Mensagem de saudação com base no horário do dia
        if current_hour < 12:
            greeting_message = "Bom dia! Como posso ajudá-lo hoje?"
        elif current_hour < 18:
            greeting_message = "Boa tarde! Como posso ajudá-lo hoje?"
        else:
            greeting_message = "Boa noite! Como posso ajudá-lo hoje?"

        # Enviar mensagem de saudação
        dispatcher.utter_message(text=greeting_message)

        return []