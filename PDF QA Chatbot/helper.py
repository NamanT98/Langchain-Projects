from dotenv import load_dotenv

load_dotenv()

from PyPDF2 import PdfReader
from langchain.prompts import PromptTemplate
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import HumanMessage, SystemMessage, AIMessage


class PdfChatbot:
    def __init__(self) -> None:
        self.history = [
            SystemMessage(
                content="""
        You are a helpful assistant that that can answer questions about pdf
        based on the context given. 
        Only use the factual information from the context to answer the question.

        Sometimes the query may not be related to the context and in such cases you are allowed to 
        answer the questions on your own knowledge. 
                                     
        Your answers should be verbose and detailed.
        """
            )
        ]

        self.llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-pro-latest",
            temperature=0.7,
            top_p=0.85,
        )

    def create_db(self, docs):
        splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=2000)
        text = ""
        for pdf in docs:
            pdf_reader = PdfReader(pdf)
            for page in pdf_reader.pages:
                text += page.extract_text()
        docs = splitter.split_text(text)
        embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
        self.db = FAISS.from_texts(docs, embeddings)
        return self.db

    def get_context(self, query):
        docs = self.db.similarity_search_with_score(query, 8)
        docs_page_content = " ".join([d[0].page_content for d in docs])
        return docs_page_content

    def create_prompt(self, query):
        prompt = f"""Using the Context given below, answer the query.:
        
        Context:{self.get_context(query)}

        Query:{query}"""

        return prompt

    def run_chain(self, query):
        self.history.append(HumanMessage(content=self.create_prompt(query)))
        response = self.llm.invoke(self.history)
        self.history.append(AIMessage(content=response.content))
        return response.content
