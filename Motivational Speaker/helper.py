from dotenv import load_dotenv
load_dotenv()

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import HumanMessage,SystemMessage,AIMessage

class MotivationalSpeaker:
    def __init__(self) -> None:
        self.history =[SystemMessage(content="""
        You are an inspiring and encouraging motivational speaker. Your role is to uplift and motivate people by
        sharing powerful quotes, positive thoughts, and personalized advice. Draw on wisdom, empathy, and optimism to
        inspire confidence, perseverance, and a positive mindset in those who interact with you.
        """)]

        self.llm=ChatGoogleGenerativeAI(model='gemini-1.5-pro-latest',
                            temperature=0.7,
                            top_p=0.85,
                            )

    def run_chain(self,query):
        self.history.append(HumanMessage(content=query))
        response=self.llm.invoke(self.history)
        self.history.append(AIMessage(content=response.content))
        return response.content