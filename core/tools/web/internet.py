from langchain.tools import tool
import wikipedia

@tool
def get_wiki_summary(topic, sentences=2):
    """Returns a short summary of the given wikipedia topic"""
    try:
        # Returns a summary with the specified number of sentences
        return wikipedia.summary(topic, sentences=sentences)
    except wikipedia.exceptions.DisambiguationError as e:
        # Handles cases where the topic is ambiguous by using the first option
        return wikipedia.summary(e.options[0], sentences=sentences)
    except wikipedia.exceptions.PageError:
        return "Page not found."

TOOLS = [get_wiki_summary]