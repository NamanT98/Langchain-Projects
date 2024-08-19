from dotenv import load_dotenv
load_dotenv()

from langchain_community.document_loaders import YoutubeLoader
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings,ChatGoogleGenerativeAI
from langchain.schema import HumanMessage,SystemMessage,AIMessage

class ChatBot:
    def __init__(self) -> None:
        self.history =[SystemMessage(content="""
        You are a helpful assistant that that can answer questions about youtube videos
        based on the video's transcript. 
        Only use the factual information from the transcript to answer the question.

        Sometimes the query may not be related to the video's transcript and in such cases you are allowed to 
        answer the questions on your own knowledge. 
                                     
        Your answers should be verbose and detailed.
        """)]

    def create_prompt(self,query):
        prompt=f"""Using the transcript given below, answer the query.:
        
        Transcript:{self.get_context(query)}

        Query:{query}"""

        return prompt

    
    def create_db(self,url):
        url=url.split('?v=')[1]
        loader=YoutubeLoader(url,language=['en','en-US'])
        transcript=loader.load()
        text_splitter=RecursiveCharacterTextSplitter(chunk_size=1000,chunk_overlap=200)
        docs=text_splitter.split_documents(transcript)
        embeddings=GoogleGenerativeAIEmbeddings(model='models/embedding-001')
        self.db=FAISS.from_documents(docs,embeddings)
        return self.db
        
    def get_context(self,query):
        docs=self.db.similarity_search_with_score(query,8)
        docs_page_content=" ".join([d[0].page_content for d in docs])
        return docs_page_content
    
    def get_llm(self):
        llm=ChatGoogleGenerativeAI(model='gemini-1.5-pro-latest',
                            temperature=0.7,
                            top_p=0.85,
                            )
        
        return llm

    def run_chain(self,query):
        self.history.append(HumanMessage(content=self.create_prompt(query)))
        llm=self.get_llm()
        response=llm.invoke(self.history)
        self.history.append(AIMessage(content=response.content))
        return response.content