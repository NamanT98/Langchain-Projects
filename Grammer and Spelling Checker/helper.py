from dotenv import load_dotenv

load_dotenv()

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import HumanMessage, SystemMessage


class TextSummarizer:
    def __init__(self) -> None:
        self.system = SystemMessage(
            content="""
        You are a grammar and spell checker. Your task is to review the provided text for any spelling, grammar,
        or punctuation errors. If you detect and correct any mistakes, return the corrected version of the text. 
        If the text is already correct with no errors, simply respond with 'Everything is correct.'
        """
        )

        self.llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-pro-latest",
            temperature=0.7,
            top_p=0.85,
        )

    def create_prompt(self, query):
        prompt = f"""Check the following text:
        
        {query}
        """

        return prompt

    def run_chain(self, query):
        response = self.llm.invoke(
            [self.system, HumanMessage(content=self.create_prompt(query))]
        )
        return response.content
