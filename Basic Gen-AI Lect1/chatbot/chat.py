from dotenv import load_dotenv

load_dotenv()

from langchain_mistralai import ChatMistralAI

from langchain_core.messages import SystemMessage, AIMessage, HumanMessage
model = ChatMistralAI(
    model="mistral-small-2506"
)

print("Enter 1 for MERN Stack Role: ")
print("Enter 2 for Java full Stack Role: ")
print("Enter 3 for Python full Role: ")

mode = int(input("Enter role: "))
if mode==1:
  prompt = "Behave like MERN Stack senior Developer"
elif mode==2:
  prompt = "Behave like for Java full Stack senior Developer"
else:
  prompt = "Behave like for Python full Stack senior Developer"


messages = [
  SystemMessage(content=prompt)
  
]


print("------------------Enter 0 to exit chat---------------------")

while True:
  prompt = input("you: ")
  messages.append(HumanMessage(content=prompt))
  if prompt == "0":
    break
  response = model.invoke(messages)
  messages.append(AIMessage(content="response.content"))

  print("AI: ", response.content)

