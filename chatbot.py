import openai
import pickle
from key import key


class Bot:
    def __init__(self, engine="davinci", temp=0.6, tokens=200, header="This is chat between Human and Bot. Bot is an AI assistant and knows almost everything. It is designed to assist and help humans and provide them detailed answers to any questions that they ask.\n"):
        self.engine = engine
        self.temp = temp
        self.tokens = tokens
        self.header = header
        self.conversation = ""
        self.footer = """User: {}
Bot:"""

    def reply(self, user_input):
        # enable persistance
        prompt = self.header + self.conversation + self.footer
        # disable persistance
        # prompt = self.header + self.footer
        prompt = prompt.format(user_input)

        response = openai.Completion.create(
            engine=self.engine,
            prompt=prompt,
            stop="User:",
            temperature=self.temp,
            max_tokens=self.tokens
        )

        bot_reply = response['choices'][0]['text']
        bot_reply = bot_reply.split("\n\n")[0].rstrip()
        self.conversation += f"User: {user_input}\nBot: {bot_reply}\n"
        return str(bot_reply)


def main():
    openai.api_key = key
    completion = openai.Completion()

    if input("Load previous (y/n): ") == "y":
        try:
            with open(input("Filename: "), 'rb') as f:
                chatbot = pickle.load(f)
            print("Loaded successfully")
        except Exception as e:
            print(e)
            print("Error loading file")
    else:
        chatbot = Bot()

    user_input = ""
    while user_input != "exit":
        user_input = input("User: ")
        if user_input == "exit":
            break
        print("Bot:" + chatbot.reply(user_input))

    if input("Save? (y/n): ") == "y":
        with open(input("Name: ") + ".pkl", 'wb') as f:
            pickle.dump(chatbot, f)
            print("Saved")


if __name__ == '__main__':
    main()
