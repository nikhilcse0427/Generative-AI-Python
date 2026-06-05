from dotenv import load_dotenv
load_dotenv()

from langchain_mistralai import ChatMistralAI
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

search_tool = TavilySearchResults(max_result=5)

llm = ChatMistralAI(model="mistral-small-2506")

prompt = ChatPromptTemplate.from_template(
  """
  You are helpfull assistant summarise the {news} into bullet points
  """
)

news_result = search_tool.run("Give top 5 sports news from all over world")

chain = prompt | llm | StrOutputParser()

result = chain.invoke({"news":news_result})

print(result)