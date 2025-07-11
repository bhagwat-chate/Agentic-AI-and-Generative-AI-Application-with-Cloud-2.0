# import os
# import asyncio
# from autogen_ext.models.openai import OpenAIChatCompletionClient
# from autogen_core.tools import FunctionTool
# from autogen_agentchat.agents import AssistantAgent


# def addition(a: int, b: int) -> dict:
#     """
#     Description: This function add the two numbers.
#     Args:
#         a: int
#         b: int
    
#     return:
#         result
#     """

#     if a and b:
#         result = a + b
#         return {"result": result}

# def subtract(a: int, b: int) -> dict:
#     """
#     This tool subtract the 2nd element (b) from first element (a).

#     Args:
#         a: int
#         b: int
#     return:
#         result
#     """

#     if a and b:
#         result = a - b
#         return {"result": result}
    

# def multiplication(a: int, b: int) -> dict:
#     """
#     Multiply the two numbers.
#     Args:
#         a: int
#         b: int
#     return:
#         result: int
#     """

#     if a and b:
#         result = a * b
#         return {"result": result}


# def division(a: float, b: float) -> dict:
#     """
#     This function/tool divide the first element (a) with 2nd element (b).
#     Args:
#         a: float
#         b: float

#     return:
#         result: float
#     """

#     if a and b:
#         result = a / b
#         return {"result": result}
    

# addition_tool = FunctionTool(addition, description="add the two numbers")
# subtract_tool = FunctionTool(subtract, description="subtract the secand argument (a) from first argument (b)")
# multiply_tool = FunctionTool(multiplication, description='multiply the two numbers')
# divide_tool = FunctionTool(division, description='divide the first argument (a) by secand argument (b)')

# tool_lst = [addition_tool, subtract_tool, multiply_tool, divide_tool]

# llm_client = OpenAIChatCompletionClient(model="gemini-1.5-flash-8b", api_key="AIzaSyCwW60xAREUBI1ScBpAAgx3b5CyDZmPNYI")

# system_message="""
# You are a helpful assistant that performs multi-step arithmetic using only the registered tools.
# Plan the steps first. For each step:
# 1. Execute a tool.
# 2. Take the result and use it as input for the next tool.
# 3. Continue until the final answer is reached.
# Always maintain logical flow from step to step, using prior outputs as new inputs.
# """

# assistant = AssistantAgent(name='arithmatic_assistant', 
#                            model_client=llm_client,
#                            tools=tool_lst,
#                            system_message=system_message
#                            )
# async def main():
#     result = await assistant.run(task="Add 2 and 3. Use the result to multiply with 2. Then use that result to subtract 3.")
#     print(result)
#     print(f"assistant response: {result.messages[-1].content}")


# if (__name__ == "__main__"):
#     asyncio.run(main())

######################################################################

import os
import asyncio
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_core.tools import FunctionTool
from autogen_agentchat.agents import AssistantAgent
from autogen import UserProxyAgent, GroupChat, GroupChatManager

def addition(a: int, b: int) -> dict:
    """
    Description: This function add the two numbers.
    Args:
        a: int
        b: int
    
    return:
        result
    """

    if a and b:
        result = a + b
        return {"result": result}

def subtract(a: int, b: int) -> dict:
    """
    This tool subtract the 2nd element (b) from first element (a).

    Args:
        a: int
        b: int
    return:
        result
    """

    if a and b:
        result = a - b
        return {"result": result}
    
def multiplication(a: int, b: int) -> dict:
    """
    Multiply the two numbers.
    Args:
        a: int
        b: int
    return:
        result: int
    """

    if a and b:
        result = a * b
        return {"result": result}

def division(a: float, b: float) -> dict:
    """
    This function/tool divide the first element (a) with 2nd element (b).
    Args:
        a: float
        b: float

    return:
        result: float
    """

    if a and b:
        result = a / b
        return {"result": result}
    

addition_tool = FunctionTool(addition, description="add the two numbers")
subtract_tool = FunctionTool(subtract, description="subtract the secand argument (a) from first argument (b)")
multiply_tool = FunctionTool(multiplication, description='multiply the two numbers')
divide_tool = FunctionTool(division, description='divide the first argument (a) by secand argument (b)')

tool_lst = [addition_tool, subtract_tool, multiply_tool, divide_tool]

llm_client = OpenAIChatCompletionClient(model="gemini-1.5-flash-8b", api_key="AIzaSyCwW60xAREUBI1ScBpAAgx3b5CyDZmPNYI")

system_message="""
You are a helpful assistant that performs multi-step arithmetic using only the registered tools.
Plan the steps first. For each step:
1. Execute a tool.
2. Take the result and use it as input for the next tool.
3. Continue until the final answer is reached.
Always maintain logical flow from step to step, using prior outputs as new inputs.
"""

assistant = AssistantAgent(name='arithmatic_assistant', 
                           model_client=llm_client,
                           tools=tool_lst,
                           system_message=system_message
                           )

user = UserProxyAgent(name='user', code_execution_config=False)

allowed_speaker_transitions_dict = {
    user: [assistant],
    assistant: [user]
}

group_chat = GroupChat(
    agents=[user, assistant],
    messages=[],
    max_round=25,
    allowed_speaker_transitions_dict=allowed_speaker_transitions_dict
)

manager = GroupChatManager(groupchat=group_chat)


async def main():
    result = await manager.run(task="Add 2 and 3. Use the result to multiply with 2. Then use that result to subtract 3.")
    print(result)
    print(f"assistant response: {result.messages[-1].content}")


if (__name__ == "__main__"):
    asyncio.run(main())
