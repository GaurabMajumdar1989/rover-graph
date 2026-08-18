import os
from json import load
from dotenv import load_dotenv
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langchain_tavily import TavilySearch


load_dotenv()

MODEL="nvidia/nemotron-nano-9b-v2:free"

@tool
def triple(num:float) -> float:
    """
    parameter num: a number to triple
    returns: the triple of that input number
    """
    return float(num)*3

tools = [TavilySearch(max_results=1), triple]

llm = ChatOpenAI(
    model=MODEL,
    base_url= os.environ['OPENROUTER_BASE_URL'],
    api_key=os.environ['OPENROUTER_API_KEY'],
    temperature=0
).bind_tools(tools)