from dotenv import load_dotenv
import os
from langchain.chat_models import ChatOpenAI
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chains import ConversationalRetrievalChain
from langchain.vectorstores import Pinecone
import pinecone

def get_retriever(index_name):
    code_db = Pinecone.from_existing_index(index_name=index_name, embedding=OpenAIEmbeddings())
    return code_db.as_retriever()

def create_conversational_chain(retriever):
    model = ChatOpenAI(model_name="gpt-3.5-turbo")
    qa = ConversationalRetrievalChain.from_llm(model, retriever=retriever)
    return qa

def ask_question(qa, question, chat_history):
    result = qa({"question": question, "chat_history": chat_history})
    chat_history.append((question, result["answer"]))
    return result["answer"], chat_history

def main():
    load_dotenv() # loads env variables
    pinecone.init(
        api_key=os.environ.get('PINECONE_API_KEY'),
        environment=os.environ.get('PINECONE_ENVIRONMENT')
    )
    retriever = get_retriever(index_name=os.environ.get('PINECONE_INDEX_NAME'))
    qa = create_conversational_chain(retriever)
    chat_history = []
    while True:
        question = input("Enter your question: ")
        if question == 'exit':
            return
        answer, chat_history = ask_question(qa, question, chat_history)
        print(f"Answer: \n{answer}\n")

if __name__ == "__main__":
    main()
