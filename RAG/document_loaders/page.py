import warnings
warnings.filterwarnings("ignore")

from langchain_community.document_loaders import WebBaseLoader

url = "https://timesofindia.indiatimes.com/"

data = WebBaseLoader(url)

docs = data.load()

print(docs[0].page_content)