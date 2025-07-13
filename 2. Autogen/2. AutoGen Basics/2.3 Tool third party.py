import os
import asyncio
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.agents import AssistantAgent
from langchain_community.utilities import GoogleSerperAPIWrapper
from dotenv import load_dotenv

load_dotenv()
os.environ['SERPER_API_KEY'] = os.getenv('SERPER_API_KEY')
os.environ['GEMINI_API_KEY'] = os.getenv('GEMINI_API_KEY')


if not os.environ['SERPER_API_KEY'] or not os.environ['GEMINI_API_KEY']:
    raise ValueError('SERPER_API_KEY or GEMINI_API_KEY is/are missing')

llm_client = OpenAIChatCompletionClient(model="gemini-1.5-flash-8b")


def search_web(query: str) -> str:
    """
    search the web for the given quey and return the result.
    """

    if not query:
        raise ValueError(f"invalid query: {query}")
    
    try:
        serpapi_wrapper = GoogleSerperAPIWrapper(type='search')

        result = serpapi_wrapper.run(query)

        return result
    
    except Exception as e:
        return "No results found"
    
agent = AssistantAgent(name='web_search',
                       model_client=llm_client,
                       system_message="You are a helpful assistant that can search the web for information using the search_web tool.Please make sure that you use the search_web tool to find information before you return the answer.don't send the year in query, rather use latest or recently etc.",
                       reflect_on_tool_use=True,
                       tools=[search_web],
                       description='An agent that can search the web for information.')

async def main():
    result = await agent.run(task="Who was the Peshwa Bajirao I. Give me 5 facts about him")
    print(result.messages[-1].content)


if (__name__=='__main__'):
    asyncio.run(main())
