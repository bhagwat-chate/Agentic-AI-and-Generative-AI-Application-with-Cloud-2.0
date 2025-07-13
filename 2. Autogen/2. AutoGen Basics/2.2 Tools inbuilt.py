import os
import asyncio
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.agents import AssistantAgent
from autogen_core.tools import FunctionTool
from autogen_ext.tools.http import HttpTool
from dotenv import load_dotenv

import asyncio


load_dotenv()

api_key = os.getenv('GEMINI_API_KEY')

if not api_key:
    raise ValueError('GEMINI_API_KEY is missing')

llm_client = OpenAIChatCompletionClient(model="gemini-1.5-flash-8b", api_key=api_key)

schema = {
        "type": "object",
        "properties": {
            "fact": {
                "type": "string",
                "description": "A random cat fact"
            },
            "length": {
                "type": "integer",
                "description": "Length of the cat fact"
            }
        },
        "required": ["fact", "length"],
    }

http_tool = HttpTool(
        name="cat_facts",
        description="get a cool cat info",
        scheme="https",
        host="catfact.ninja",
        port=443,
        path="/fact",
        method="GET",
        return_type='json',
        json_schema=schema
    )

agent = AssistantAgent(
    name='cat_agent',
    model_client=llm_client,
    tools=[http_tool],
    reflect_on_tool_use=True,
    system_message=(
        "You are a helpful agent that uses the cat_facts tool. "
        "The tool returns a JSON with 'fact' and 'length'. "
        "Respond only using those two fields formatted as numbered points."),
    )

async def main():
    result = await agent.run(task="Give ma a random cat facts. I expect 5 points")
    print(result.messages[-1].content)

if (__name__=='__main__'):
    asyncio.run(main())
