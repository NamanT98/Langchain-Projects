import dotenv

dotenv.load_dotenv()
from youtube_search import YoutubeSearch
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import load_tools
from langchain.agents import initialize_agent
from langchain.agents import AgentType
from langchain.tools import BaseTool
from langchain_community.document_loaders import YoutubeLoader


class RecipeTool(BaseTool):
    name: str = "Food Recipe Collector"
    description: str = "Use this tool when you need to know the recipe of any food item"

    def _run(self, food_item_name: str) -> str:
        results = YoutubeSearch(
            search_terms=f"{food_item_name} recipe", max_results=5
        ).to_dict()

        for i in results:
            try:
                loader = YoutubeLoader(i["id"], language=["en", "en-US"])
                transcripts = loader.load()[0].page_content
                return transcripts
            except:
                pass
        return "Recipe Not Found!"

    def _arun(self, radius: int):
        raise NotImplementedError("This tool does not support async")


class FoodRecipeAgent:
    def __init__(self):

        self.llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-pro-latest",
            temperature=0.7,
            top_p=0.85,
        )

    def create_prompt(self):
        """Function to read customized agent prompt"""
        with open("Food Recipe Guide/prompt.txt", "r") as f:
            prompt = f.read()
        return prompt

    def get_tools(self):
        """Function to load tools for the agent"""
        tools = [load_tools(["serpapi"])[0], RecipeTool()]
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
