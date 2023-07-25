from langchain.agents import AgentType
from langchain.chat_models import ChatOpenAI
from langchain.agents import initialize_agent
from langchain.agents.agent_toolkits import PlayWrightBrowserToolkit
from langchain.tools.playwright.utils import (
    create_async_playwright_browser,
    create_sync_playwright_browser, # A synchronous browser is available, though it isn't compatible with jupyter.
)
from langchain.prompts import MessagesPlaceholder
from langchain.memory import ConversationBufferMemory
from langchain.callbacks.streaming_stdout_final_only import (
    FinalStreamingStdOutCallbackHandler,
)


chat_history = MessagesPlaceholder(variable_name="chat_history")
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

llm = ChatOpenAI(
    openai_api_key = "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",
    temperature=0,
    streaming=True,
    callbacks=[FinalStreamingStdOutCallbackHandler()]
    ) # Also works well with Anthropic models


agent_chain = initialize_agent(
    tools=[],
    llm=llm,
    agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
    memory=memory,
    agent_kwargs = {
        "memory_prompts": [chat_history],
        "input_variables": ["input", "agent_scratchpad", "chat_history"]
    },
    verbose=True
    )


if __name__ == '__main__':
    while True:
        query = input("User: ")
        agent_chain.run(input=query)
        response = "test"
        print("Bot: ", response)