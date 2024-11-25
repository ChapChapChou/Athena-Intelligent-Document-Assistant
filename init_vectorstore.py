# usage: python init_vectorstore.py
#
# This script initializes the vectorstore with the Titan Embeddings Model.
# It loads the PDFs from the IRS website and splits them into smaller chunks.
# It then creates a vectorstore from the chunks and saves it to disk.
#
import os
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders.pdf import PyPDFDirectoryLoader
from langchain.vectorstores import FAISS
from bedrock_client import BedrockClient
from langchain.embeddings import BedrockEmbeddings
from langchain.llms.bedrock import Bedrock
def initialize_vectorstore():
    from bedrock_client import BedrockClient
    boto3_bedrock = BedrockClient.get_client()

    # We will be using the Titan Embeddings Model to generate our Embeddings.
    bedrock_embeddings = BedrockEmbeddings(model_id="amazon.titan-embed-text-v1", client=boto3_bedrock)

    from urllib.request import urlretrieve
    
    # TODO: import the PDFs from S3
    os.makedirs("data", exist_ok=True)
    files = [
        "https://www.irs.gov/pub/irs-pdf/p1544.pdf",
        "https://www.irs.gov/pub/irs-pdf/p15.pdf",
        "https://www.irs.gov/pub/irs-pdf/p1212.pdf",
    ]
    for url in files:
        file_path = os.path.join("data", url.rpartition("/")[2])
        urlretrieve(url, file_path)

    import numpy as np
    from langchain.text_splitter import CharacterTextSplitter, RecursiveCharacterTextSplitter
    #from langchain.document_loaders import PyPDFLoader, PyPDFDirectoryLoader
    from langchain_community.document_loaders.pdf import PyPDFLoader, PyPDFDirectoryLoader

    loader = PyPDFDirectoryLoader("./data/")

    documents = loader.load()
    # - in our testing Character split works better with this PDF data set
    text_splitter = RecursiveCharacterTextSplitter(
        # Set a really small chunk size, just to show.
        chunk_size = 1000,
        chunk_overlap  = 100,
    )
    docs = text_splitter.split_documents(documents)

    # Print some stats
    avg_doc_length = lambda documents: sum([len(doc.page_content) for doc in documents])//len(documents)
    avg_char_count_pre = avg_doc_length(documents)
    avg_char_count_post = avg_doc_length(docs)
    print(f'Average length among {len(documents)} documents loaded is {avg_char_count_pre} characters.')
    print(f'After the split we have {len(docs)} documents more than the original {len(documents)}.')
    print(f'Average length among {len(docs)} documents (after split) is {avg_char_count_post} characters.')
    
    # Create directory for storing FAISS index
    index_path = "faiss_index"
    os.makedirs(index_path, exist_ok=True)
    
    vectorstore = FAISS.from_documents(docs, bedrock_embeddings)
    vectorstore.save_local(index_path)

if __name__ == "__main__":
    initialize_vectorstore()