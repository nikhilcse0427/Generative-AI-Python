import warnings
warnings.filterwarnings("ignore")

from langchain_community.document_loaders import PyPDFLoader

data = PyPDFLoader("./document_loaders/Sociology.pdf")
doc = data.load()

print(doc[1].page_content)