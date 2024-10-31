import random

class SimpleChatBot:
    def __init__(self):
        self.user_name = None
        self.responses = {
            "greeting": ["Hello! What's your name?", "Hi there! May I know your name?", "Hey! Who am I chatting with?"],
            "farewell": ["Goodbye! Have a great day!", "See you later!", "Take care!"],
            "weather": ["I can't check the weather, but I hope it's nice where you are!"],
            "joke": ["Why did the scarecrow win an award? Because he was outstanding in his field!",
                     "Why don’t skeletons fight each other? They don’t have the guts!",
                     "Why did the math book look sad? Because it had too many problems!"],
            "default": ["I'm not sure how to respond to that.", "Could you ask something else?", "I'm here to help with simple questions!"]
        }

    def chatbot_response(self, user_input):
        user_input = user_input.lower()
        
        # Greetings
        if "hello" in user_input or "hi" in user_input:
            if not self.user_name:
                return random.choice(self.responses["greeting"])
            else:
                return f"Hello again, {self.user_name}!"

        # get user name
        if "my name is" in user_input:
            self.user_name = user_input.split("my name is ")[-1].capitalize()
            return f"Nice to meet you, {self.user_name}!"

        # Respond to weather
        if "weather" in user_input:
            return random.choice(self.responses["weather"])

        # Tell a joke
        if "joke" in user_input:
            return random.choice(self.responses["joke"])

        # Say goodbye
        if "bye" in user_input:
            return random.choice(self.responses["farewell"])

        # Default response
        return random.choice(self.responses["default"])

    def start_chat(self):
        print("ChatBot: Hello! Type 'bye' to end the chat.")
        while True:
            user_input = input("You: ")
            if "bye" in user_input.lower():
                print("ChatBot:", self.chatbot_response("bye"))
                break
            response = self.chatbot_response(user_input)
            print("ChatBot:", response)

chatbot = SimpleChatBot()
chatbot.start_chat()
