from dotenv import load_dotenv
from langchain_mistralai import ChatMistralAI
from pydantic import BaseModel
from typing import List
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

model = ChatMistralAI(model="mistral-small-2506")

class Movie(BaseModel):
    movie_name: str
    release_year: int
    actors_name: List[str]
    genre: List[str]
    box_office_collection: int
    rating: float
    summary: str

parser = PydanticOutputParser(pydantic_object=Movie)

prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
        Extract movie details from the paragraph.

        {movie_format}
        """
    ),
    (
        "human",
        "{paragraph}"
    )
])

parser = PydanticOutputParser(pydantic_object=Movie)

para = input("Enter movie description: ")

final_prompt = prompt.invoke({
    "movie_format": parser.get_format_instructions(),
    "paragraph": para
})

response = model.invoke(final_prompt)

print("\nParsed Movie Object:")
print(response.content)
