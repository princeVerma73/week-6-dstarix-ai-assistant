class ConversationMemory:

    def __init__(
        self,
        max_messages=10
    ):

        self.messages = []

        self.max_messages = max_messages


    def add_message(
        self,
        role,
        content
    ):

        self.messages.append({
            "role": role,
            "content": content
        })

        if len(self.messages) > self.max_messages:

            self.messages.pop(0)


    def get_history(self):

        return self.messages


    def clear(self):

        self.messages = []


if __name__ == "__main__":

    memory = ConversationMemory()

    memory.add_message(
        "user",
        "What happens in the second phase?"
    )

    memory.add_message(
        "assistant",
        "The second phase focuses on practical projects."
    )

    print(
        memory.get_history()
    )