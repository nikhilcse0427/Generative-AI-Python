import warnings
warnings.filterwarnings("ignore")

from langchain_community.retrievers import ArxivRetriever


retrievers = ArxivRetriever(
  load_max_docs=2,
  load_all_available_meta = True
)

docs = retrievers.invoke("project management platform like JIRA")

for item in docs:
  print("Title: ", item.metadata.get("title"))
  print("Authors: ", item.metadata.get("authors"))
  print("Abstract: ", item.page_content)
  print("Published: ", item.metadata.get("published"))
  print("Summary: ", item.metadata.get("summary"))
  print("\n")

