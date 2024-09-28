from openai import OpenAI
import tiktoken  # For token counting, requires the tiktoken library


class Responder:
    def __init__(self, model="gpt-4", max_tokens=4096, summary_threshold=3000):
        # Initialize the OpenAI client, history, and token limit
        self.client = OpenAI()
        self.history = []
        self.model = model
        self.max_tokens = max_tokens  # Maximum token limit for model
        self.summary_threshold = summary_threshold  # Threshold to trigger summarization

    def count_tokens(self, text):
        """Utility function to count tokens in a string using tiktoken."""
        encoding = tiktoken.encoding_for_model(self.model)
        return len(encoding.encode(text))

    def summarize_history(self):
        """Summarize the conversation history when it exceeds the token limit."""
        if not self.history:
            return

        # Concatenate the history for summarization
        history_text = " ".join([message["content"] for message in self.history])

        # Use GPT to summarize the history
        summary_prompt = f"Summarize the following conversation: {history_text}"
        summary_response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": summary_prompt}],
            max_tokens=150  # Limit summary size
        )

        # Extract the summary text and return it
        summary = summary_response['choices'][0]['message']['content']
        return summary

    def manage_memory(self):
        """Manage the conversation history to ensure it stays within token limits."""
        # Count the tokens used by the current history
        history_tokens = sum(self.count_tokens(msg["content"]) for msg in self.history)

        # If the token count exceeds the threshold, summarize the history
        if history_tokens > self.summary_threshold:
            summary = self.summarize_history()

            # Clear history and replace it with the summary
            self.history = [{"role": "assistant", "content": summary}]
            print("History summarized to maintain token limit.")

    def respond(self, query):
        """Generate a response while managing memory and token limits."""
        # Manage memory before adding new input
        self.manage_memory()

        # Add user query to the history
        self.history.append({"role": "user", "content": query})

        # Prepare the messages for the model, including the entire history
        messages = self.history.copy()

        # Stream the response
        stream = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            stream=True,
        )

        response_text = ""

        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                content = chunk.choices[0].delta.content
                print(content, end="")
                response_text += content

        # Add the model's response to the history
        self.history.append({"role": "assistant", "content": response_text})


# Example usage
if __name__ == "__main__":
    responder = Responder(model="gpt-4", max_tokens=4096, summary_threshold=3000)

    user_input = "Can you explain quantum computing?"
    print("User:", user_input)

    responder.respond(user_input)

    follow_up = "Can you summarize what we discussed so far?"
    print("\nUser:", follow_up)
    responder.respond(follow_up)
