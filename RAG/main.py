import warnings
warnings.filterwarnings("ignore")

from dotenv import load_dotenv
load_dotenv()

from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter



model = ChatMistralAI(
    model="mistral-small-2506"
)
text_splitter = RecursiveCharacterTextSplitter(chunk_size=100, chunk_overlap=0)

loader = PyPDFLoader("./document_loaders/Sociology.pdf")
docs = loader.load()

texts = text_splitter.split_documents(docs)


prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an AI that summarizes text."),
    ("human", "{data}")
])

messages = prompt.format_messages(
    data=docs[0].page_content
)

result = model.invoke(messages)

print("Summary:")
print(result.content)