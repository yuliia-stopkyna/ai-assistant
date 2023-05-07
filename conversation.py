import os

from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.memory import VectorStoreRetrieverMemory
from langchain import PromptTemplate, ConversationChain
from langchain.chat_models import ChatOpenAI

OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]


def get_ai_answer(conversation_id: str, is_new: bool, question: str) -> str:
    embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
    vectorstore = Chroma(
        conversation_id, embedding_function=embeddings, persist_directory="chromadb"
    )
    retriever = vectorstore.as_retriever()
    memory = VectorStoreRetrieverMemory(retriever=retriever)

    if is_new:
        memory.save_context(inputs={}, outputs={})

    llm = ChatOpenAI(model_name="gpt-3.5-turbo", openai_api_key=OPENAI_API_KEY)

    template = """The following is a conversation between a human and an AI as a personal assistant. 
    The AI is helpful and should use previous conversation as a context.

    Previous conversation:
    {history}

    Current conversation:
    Human: {input}
    AI:"""

    prompt = PromptTemplate(input_variables=["history", "input"], template=template)
    conversation = ConversationChain(llm=llm, prompt=prompt, memory=memory)
    answer = conversation.predict(input=question)

    return answer
