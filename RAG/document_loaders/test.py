import warnings
warnings.filterwarnings("ignore")

from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

# pip install langchain-text-splitters langchain-unstructured
data = TextLoader("./document_loaders/notes.txt")
text_splitter = RecursiveCharacterTextSplitter(
  seperator=[""],
  chunk_size=100, 
  chunk_overlap=5
  )


docs = data.load()
chunks = text_splitter.split_documents(docs)


print(len(chunks))

for item in chunks:
  print(item.page_content)
  print("\n")

# print(docs[0].page_content)



