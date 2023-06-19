from dotenv import load_dotenv
import os
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.document_loaders import TextLoader
import pinecone
from langchain.vectorstores import Pinecone

def load_and_split_documents(root_dir, exclude_file):
    with open(exclude_file, 'r') as file:
        exclusions = file.read().splitlines()
    exclude_dirs = [excl.replace('/','') for excl in exclusions if excl.endswith('/')]
    exclude_files = [excl for excl in exclusions if not excl.endswith('/')]

    code_content = []
    for dirpath, dirnames, filenames in os.walk(root_dir):
        # Skip excluded directories
        for excl_dir in exclude_dirs:
            match = excl_dir in dirpath
            if match:
                break
        if match:
            continue
        for file in filenames:
            # Skip excluded file extensions
            if any(file.endswith(excl_file) for excl_file in exclude_files):
                continue
            try:
                loader = TextLoader(os.path.join(dirpath, file), encoding="utf-8")
                code_content.extend(loader.load_and_split())
            except Exception as e:
                pass
    text_splitter = CharacterTextSplitter(chunk_size=3900, chunk_overlap=0)
    return text_splitter.split_documents(code_content)

def init_pinecone(api_key, environment):
    pinecone.init(
        api_key=api_key,
        environment=environment
    )

def upload_vectors_to_pinecone(documents, embeddings, index_name):
    code_db = Pinecone.from_documents(
        documents,
        embeddings,
        index_name=index_name
    )
    return code_db

def main():
    load_dotenv() # loads env variables
    root_dir = input("Enter the fully qualified root directory: ")
    documents = load_and_split_documents(root_dir, 'exclude.txt')
    embeddings = OpenAIEmbeddings(disallowed_special=())
    init_pinecone(
        api_key=os.environ.get('PINECONE_API_KEY'),
        environment=os.environ.get('PINECONE_ENVIRONMENT')
    )
    code_db = upload_vectors_to_pinecone(
        documents,
        embeddings,
        index_name=os.environ.get('PINECONE_INDEX_NAME')
    )

if __name__ == "__main__":
    main()
