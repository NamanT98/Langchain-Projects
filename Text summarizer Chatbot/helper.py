from dotenv import load_dotenv
load_dotenv()

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import HumanMessage,SystemMessage

class TextSummarizer:
    def __init__(self) -> None:
        self.system =SystemMessage(content="""
        You are a highly skilled text summarization model.
        Your task is to condense provided texts into clear, concise summaries while correcting any spelling and
        grammatical errors. Ensure that the summarized text is accurate, coherent, and free of mistakes, preserving the key information
        and intent of the original content.
        """)

        self.llm=ChatGoogleGenerativeAI(model='gemini-1.5-pro-latest',
                            temperature=0.7,
                            top_p=0.85,
                            )

    def create_prompt(self,query):
        prompt=f"""Summarize the following text:
        
        {query}
        """

        return prompt

    def run_chain(self,query):
        response=self.llm.invoke([self.system,HumanMessage(content=self.create_prompt(query))])
        return response.content