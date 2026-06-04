from dotenv import load_dotenv
from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate


load_dotenv()

model = ChatMistralAI(
    model="mistral-small-2506"
)

prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
        Extract all available information from the provided player description.

        Return the result in the following format:

        Name:
        Date of Birth:
        Place of Birth:
        Batting Style:
        Bowling Style:
        Role:

        ODI Statistics:
        - Matches:
        - Runs:
        - Average:
        - Centuries:

        Test Statistics:
        - Matches:
        - Runs:
        - Average:
        - Centuries:

        T20I Statistics:
        - Matches:
        - Runs:
        - Average:
        - Centuries:

        IPL Statistics:
        - Team:
        - Matches:
        - Runs:
        - Average:
        - Centuries:

        Achievements:
        - International Centuries:
        - ICC Trophies:
        - Major Records:

        Career Summary:
        (Provide a concise summary.)
        """
    ),
    (
        "human",
        """
        Player Description:
        {player_text}
        """
    )
])

player_description = input("Enter player description:\n")



response = prompt.invoke({
    "player_text": player_description
})

message = model.invoke(response)
print("\nResponse:\n")
print(message.content)