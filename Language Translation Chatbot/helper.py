from dotenv import load_dotenv

load_dotenv()

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import HumanMessage, SystemMessage


class Translator:
    def __init__(self) -> None:
        self.system = SystemMessage(
            content="""
        You are a language translation assistant. When a user provides a text and specifies the Source language,
        your task is to verify that the text matches the specified source language.
        If it does, accurately translate the text into the target language provided by the user.
        If the text does not match the specified source language, inform the user of the discrepancy.

        If you cannot translate the text into the target language then reply that you don't support the target language.
        There should not be empty response.
        """
        )

        self.llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-pro-latest",
            temperature=0.7,
            top_p=0.85,
        )

    def create_prompt(self, query, lang):
        prompt = f"""Translate the below text from the given source and target language:
        
        Text:{query}

        Source Language:{lang[0]}
        Target Language:{lang[1]}"""

        return prompt

    def run_chain(self, query, lang):
        print(lang)
        response = self.llm.invoke(
            [self.system, HumanMessage(content=self.create_prompt(query, lang))]
        )
        # print("Response is:",response.content)
        return response.content
