import dotenv
import os
import requests

dotenv.load_dotenv()

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import load_tools
from langchain.agents import initialize_agent
from langchain.agents import AgentType
from langchain.tools import BaseTool


class HotelData(BaseTool):
    name: str = "Hotel data collector"
    description: str = (
        "use this tool when you need the information about the hotel at destination place"
    )

    def _run(self, source: str, destination: str, from_date: str, to_date: str) -> str:
        url = "https://tripadvisor16.p.rapidapi.com/api/v1/hotels/searchLocation"
        querystring = {"query": destination}

        headers = {
            "x-rapidapi-key": os.environ.get("RAPID_API_KEY"),
            "x-rapidapi-host": "tripadvisor16.p.rapidapi.com",
        }

        response = requests.get(url, headers=headers, params=querystring).json()
        geoid = response["data"][0]["geoId"]

        url = "https://tripadvisor16.p.rapidapi.com/api/v1/hotels/searchHotels"
        querystring = {
            "geoId": geoid,
            "checkIn": from_date,
            "checkOut": to_date,
            "pageNumber": "1",
            "currencyCode": "INR",
        }

        response = requests.get(url, headers=headers, params=querystring).json()
        hotels = []
        for i in response["data"]["data"]:
            hotels.append(i["title"])
        return {"Hotels": hotels}

    def _arun(self, radius: int):
        raise NotImplementedError("This tool does not support async")


class TravelAgent:
    def __init__(self):

        self.llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-pro-latest",
            temperature=0.7,
            top_p=0.85,
        )

    def create_prompt(self):
        """Function to read customized agent prompt"""
        with open("Travel Planning Agent/prompt.txt", "r") as f:
            prompt = f.read()
        return prompt

    def get_tools(self):
        """Function to load tools for the agent"""
        tools = [load_tools(["serpapi"])[0], HotelData()]
        tools[0].description = (
            "A search engine. Useful when you need to find information about anything. Use this to find popular attractions, landmarks, and activities at the destination. Input should be a search query."
        )
        return tools

    def get_agent(self):
        """Initializes agent"""
        self.agent = initialize_agent(
            agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
            tools=self.get_tools(),
            llm=self.llm,
            verbose=True,
            max_iterations=3,
            early_stopping_method="generate",
        )

        self.agent.agent.llm_chain.prompt.messages[0].prompt.template = (
            self.create_prompt()
        )
        return self.agent

    def run_agent(self, query):
        """Function to run the agent"""
        results = self.agent.run(query)
        return results
