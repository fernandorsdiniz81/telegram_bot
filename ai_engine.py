import os
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from dotenv import load_dotenv

class AIEngine:
    def __init__(self) -> None:
        load_dotenv()
        OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]


    def answer_messages_with_ai(self, chat_id: str, human_message: str):

        def get_session_history(session_id: str) -> BaseChatMessageHistory:
            store = {}
            if session_id not in store:
                store[session_id] = ChatMessageHistory()
            return store[session_id]

        model = ChatOpenAI(model="gpt-3.5-turbo")
        with_message_history = RunnableWithMessageHistory(model, get_session_history)
        config = {"configurable": {"session_id": f"{chat_id}"}}

        ai_output = with_message_history.invoke(
            [HumanMessage(content=f"{human_message}")],
            config=config,
        )

        return ai_output
