import json
import os
import sys

import boto3
import botocore
from bedrock_client import BedrockClient
from langchain.embeddings import BedrockEmbeddings
boto3_bedrock = BedrockClient.get_client()
bedrock_embeddings = BedrockEmbeddings(model_id="amazon.titan-embed-text-v1", client=boto3_bedrock)

#boto3_bedrock = boto3.client('bedrock-runtime', region_name='us-east-1')

import warnings

from io import StringIO
import sys
import textwrap
import os
from typing import Optional

# External Dependencies:
import boto3
from botocore.config import Config

warnings.filterwarnings('ignore')

from langchain.chains.question_answering import load_qa_chain
from langchain.vectorstores import FAISS
from langchain.indexes import VectorstoreIndexCreator
from langchain.indexes.vectorstore import VectorStoreIndexWrapper

# TODO: 
## 1. if local index exists, get the new documents (reminder: use s3 lamda trigger/input the increment document name)
## 2. add the new documents to the existing index
## existing_vectorstore.add_documents(new_docs)

index_path = "faiss_index"
vectorstore = FAISS.load_local(index_path, bedrock_embeddings, allow_dangerous_deserialization=True)