from openai import OpenAI
import tiktoken

class Responder:
    def __init__(self, model="gpt-4", max_tokens=4096, summary_threshold=3000):
        self.client = OpenAI()
        self.history = []
        self.model = model
        self.max_tokens = max_tokens
        self.summary_threshold = summary_threshold

    def count_tokens(self, text):
        encoding = tiktoken.encoding_for_model(self.model)
        return len(encoding.encode(text))

    def summarize_history(self):
        if not self.history:
            return
        history_text = " ".join([msg["content"] for msg in self.history])
        summary_prompt = f"Summarize the following conversation: {history_text}"
        summary_response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": summary_prompt}],
            max_tokens=150
        )
        summary = summary_response['choices'][0]['message']['content']
        return summary

    def manage_memory(self):
        history_tokens = sum(self.count_tokens(msg["content"]) for msg in self.history)
        if history_tokens > self.summary_threshold:
            summary = self.summarize_history()
            self.history = [{"role": "assistant", "content": summary}]

    def respond(self, query):
        self.manage_memory()
        self.history.append({"role": "user", "content": query})
        stream = self.client.chat.completions.create(
            model=self.model,
            messages=self.history,
            stream=True,
        )
        response_text = ""
        for chunk in stream:
            if chunk.choices[0].delta.content:
                response_text += chunk.choices[0].delta.content
                print(chunk.choices[0].delta.content, end="")
        self.history.append({"role": "assistant", "content": response_text})

        return response_text
