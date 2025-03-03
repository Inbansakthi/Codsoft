import random
import re

class Chatbot:
    def __init__(self):
        self.responses = {
            "greetings": [
                "Hello! I am here to discuss cricket with you.", 
                "Hi there! Are you a cricket fan?", 
                "Hey! Ask me anything about cricket."
            ],

            "what_is_cricket": [
                "Cricket is a bat-and-ball sport played between two teams of 11 players, where the aim is to score more runs than the opponent."
            ],

            "cricket_formats": [
                "Cricket has three main formats: Test Cricket (5 days), One-Day Internationals (ODIs - 50 overs), and Twenty20 (T20 - 20 overs)."
            ],

            "over_in_cricket": [
                "An over consists of six legal deliveries bowled by a single bowler."
            ],

            "greatest_cricketer_of_all_time": [
                "Many consider Sir Don Bradman the greatest batsman, while Sachin Tendulkar is also widely regarded as one of the best."
            ],

            "scored_the_most_runs_in_international_cricket": [
                "Sachin Tendulkar holds the record for the most runs in international cricket."
            ],
            
            "best_teams": [
                "Historically, Australia, India, and England have been among the top-performing cricket teams."
            ],
            
            "fallback": [
                "I'm not sure I understand. Can you rephrase that?", 
                "That's a deep question! You might find a better answer on an official cricket website."
            ]
        }

    def get_response(self, user_input):
        user_input = user_input.lower()

        # Rule-based matching
        if re.search(r"\b(hi|hello|hey)\b", user_input):
            return random.choice(self.responses["greetings"])
        elif re.search(r"\b(what is cricket|define cricket|explain cricket|tell me about cricket)\b", user_input):
            return random.choice(self.responses["what_is_cricket"])
        elif re.search(r"\b(what are the cricket formats|types of cricket|explain about cricket formats|list out the cricket formats and define them)\b", user_input):
            return random.choice(self.responses["cricket_formats"])
        elif re.search(r"\b(what is an over in cricket|cricket over|define cricket over)\b", user_input):
            return random.choice(self.responses["over_in_cricket"])
        elif re.search(r"\b(who is the greatest cricketer of all time|who is the GOAT of cricket|greatest cricketer)\b", user_input):
            return random.choice(self.responses["greatest_cricketer_of_all_time"])
        elif re.search(r"\b(who has scored the most runs in international cricket|who has scored the most runs)\b", user_input):
            return random.choice(self.responses["scored_the_most_runs_in_international_cricket"])
        elif re.search(r"\b(which are the best teams in cricket|best cricket teams|top cricket teams)\b", user_input):
            return random.choice(self.responses["best_teams"])
        else:
            return random.choice(self.responses["fallback"])

def chat():
    bot = Chatbot()
    print("Cricket Chatbot: Hi! I'm a Cricket Chatbot. Ask me anything about cricket. Type 'exit' to end the conversation.")
    
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit", "bye"]:
            print("Cricket Chatbot: Goodbye! Have a great day.")
            break
        print("Cricket Chatbot:", bot.get_response(user_input))

# Start the chatbot
chat()