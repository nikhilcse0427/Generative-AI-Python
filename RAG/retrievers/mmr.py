import warnings
warnings.filterwarnings("ignore")

from dotenv import load_dotenv
load_dotenv()

from langchain_mistralai import ChatMistralAI
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_mistralai import MistralAIEmbeddings
from langchain_community.vectorstores import Chroma



docs = [
    Document(page_content="Python is widely used in Artificial Intelligence.", metadata={"source": "AI_book"}),
    Document(page_content="Pandas is used for data analysis in Python.", metadata={"source": "DataScience_book"}),
    Document(page_content="Neural networks are used in deep learning.", metadata={"source": "DL_book"}),
]

text_splitter = RecursiveCharacterTextSplitter(chunk_size=100, chunk_overlap=0)
chunks = text_splitter.split_documents(docs)

embeddings = MistralAIEmbeddings(
    model="mistral-embed",
)

vector_store = Chroma.from_documents(
    chunks,
    embeddings
)
# ----------------------------similarity_retriever-----------------------------
similarity_retriever = vector_store.as_retriever(
  search_type="similarity",
  search_kwargs={"k":3}
)

similartiy_docs = similarity_retriever.invoke("Most popular language used for AI?")

for doc in similartiy_docs:
  print(doc.page_content)

# ---------------------------------mmr---------------------------------

mmr_retriever = vector_store.as_retriever(
  search_type="mmr",
  search_kwargs={"k":3}
)

mmr_docs = similarity_retriever.invoke("Most popular language used for AI?")

for item in mmr_docs:
  print(item.page_content)