from dotenv import load_dotenv
from langchain_mistralai import ChatMistralAI

load_dotenv()

model = ChatMistralAI(
    model="mistral-small-2506"
)

response = model.invoke("India GDP in 2030 and 2040", temperature=0.9, max_token=20)

print("Response:", response.content)