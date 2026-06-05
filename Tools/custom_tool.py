from langchain.tools import tool

@tool
def greetUser(name: str)->str :
  """Generating a greeeting message to user"""
  return f"Hi, {name} happy new year"

greet = greetUser.invoke({"name": "Nikhil"})
print(greet)
print(greetUser.name)
print(greetUser.description) 
print(greetUser.args)