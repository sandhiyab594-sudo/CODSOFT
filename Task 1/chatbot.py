

import re
import random
from datetime import datetime


class ChatBot:
    """A small rule-based chatbot built on regex pattern matching."""

    def __init__(self, bot_name="Codsy"):
        self.bot_name = bot_name
        self.user_name = None
        self.exit_flag = False

        
        self.rules = [
            (r"\bmy name is\s+([a-zA-Z]+)", self._handle_set_name),
            (r"\b(hi|hello|hey|hola|good morning|good afternoon|good evening)\b", self._handle_greeting),
            (r"\bhow are you\b", self._handle_how_are_you),
            (r"\bwhat('?s| is) your name\b", self._handle_bot_name),
            (r"\bwho (made|created|built) you\b", self._handle_creator),
            (r"\bhow old are you\b", self._handle_age),
            (r"\b(what (can you do|do you do)|help)\b", self._handle_help),
            (r"\btime\b", self._handle_time),
            (r"\b(date|day is it|today)\b", self._handle_date),
            (r"\bweather\b", self._handle_weather),
            (r"\bjoke\b", self._handle_joke),
            (r"\bthank(s| you)?\b", self._handle_thanks),
            (r"\b(bye|goodbye|exit|quit|see you)\b", self._handle_bye),
        ]

   
    def _handle_set_name(self, match):
        self.user_name = match.group(1).capitalize()
        return f"Nice to meet you, {self.user_name}! How can I help you today?"

    def _handle_greeting(self, match):
        greetings = [
            "Hello! How can I help you today?",
            "Hi there! What can I do for you?",
            "Hey! Good to see you.",
        ]
        if self.user_name:
            return f"Hi {self.user_name}! " + random.choice(greetings)
        return random.choice(greetings)

    def _handle_how_are_you(self, match):
        return "I'm just a program, but I'm running smoothly! How about you?"

    def _handle_bot_name(self, match):
        return f"My name is {self.bot_name}. sandhiya"

    def _handle_creator(self, match):
        return "I was built as part of a CodSoft AI internship project."

    def _handle_age(self, match):
        return "I don't really have an age — I'm just lines of Python code!"

    def _handle_help(self, match):
        return (
            "I can chat about: greetings, my name, your name, the time, "
            "today's date, a joke, the weather (generic reply), and saying "
            "'thanks'. Type 'bye' anytime to end our chat."
        )

    def _handle_time(self, match):
        now = datetime.now().strftime("%I:%M %p")
        return f"The current time is {now}."

    def _handle_date(self, match):
        today = datetime.now().strftime("%A, %d %B %Y")
        return f"Today's date is {today}."

    def _handle_weather(self, match):
        return ("I don't have live internet access, so I can't check real "
                "weather, but I hope it's pleasant wherever you are!")

    def _handle_joke(self, match):
        jokes = [
            "Why do programmers prefer dark mode? Because light attracts bugs!",
            "Why did the computer go to therapy? It had too many issues.",
            "I would tell you a UDP joke, but you might not get it.",
        ]
        return random.choice(jokes)

    def _handle_thanks(self, match):
        return random.choice(["You're welcome!", "No problem!", "Anytime!"])

    def _handle_bye(self, match):
        self.exit_flag = True
        name_part = f", {self.user_name}" if self.user_name else ""
        return f"Goodbye{name_part}! Have a great day."

    
    def get_response(self, user_input):
        """Return a chatbot reply for a given line of user input."""
        if not user_input or not user_input.strip():
            return "I didn't catch that. Could you say something?"

        text = user_input.lower().strip()

        for pattern, handler in self.rules:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                try:
                    return handler(match)
                except Exception:
                    
                    return "Sorry, something went wrong with that. Could you rephrase?"

        fallback_responses = [
            "I'm not sure I understand. Could you rephrase that?",
            "Hmm, I don't have a rule for that yet. Try asking something else!",
            "Sorry, I didn't get that. Type 'help' to see what I can do.",
        ]
        return random.choice(fallback_responses)

   
    def run(self):
        print(f"{self.bot_name}: Hello! I'm {self.bot_name}, a rule-based chatbot.")
        print(f"{self.bot_name}: Type 'bye' or 'quit' anytime to end our chat.\n")

        while True:
            try:
                user_input = input("You: ")
            except (EOFError, KeyboardInterrupt):
                
                print(f"\n{self.bot_name}: Goodbye!")
                break

            response = self.get_response(user_input)
            print(f"{self.bot_name}: {response}")

            if self.exit_flag:
                break


if __name__ == "__main__":
    bot = ChatBot(bot_name="Codsy")
    bot.run()