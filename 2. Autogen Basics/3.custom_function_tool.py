import os
import asyncio
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.agents import AssistantAgent
from autogen_core.tools import FunctionTool
from dotenv import load_dotenv

load_dotenv()


llm_client = OpenAIChatCompletionClient(model="gemini-1.5-flash-8b", api_key=os.getenv('GOOGLE_API_KEY'))

def reverse_txt(input_txt: str) -> str:
    """
    Description: This tool reverse the input string and return the reversed string
    Args:
    input_txt: str

    output: str
    """

    if input_txt:
        return input_txt[::-1]
    
reverse_txt_tool = FunctionTool(reverse_txt, description="A tool to reverse the input text.")

my_agent = AssistantAgent(
    name="reverse_txt_agent",
    model_client=llm_client,
    tools=[reverse_txt_tool],
    system_message='You are a helpful assistant, you are capable to reverse the input text with the help of reverse_txt tool.'
)


async def main(): 
    result = await my_agent.run(task = 'Reverse the string "india is great"')

    print(result.messages[-1].content)

if (__name__ == "__main__"):
    asyncio.run(main())
