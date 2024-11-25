from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from embedding import vectorstore
from bedrock_client import BedrockClient
from output_format import format_source_documents, print_ww
from langchain.llms.bedrock import Bedrock

class DocumentQA:
    def __init__(self):
        self.boto3_bedrock = BedrockClient.get_client()
        self.llm = Bedrock(model_id='amazon.titan-tg1-large', client=self.boto3_bedrock)
        self.prompt = PromptTemplate(
            template=self._get_prompt_template(),
            input_variables=["context", "question"]
        )
        self.qa = self._initialize_qa()

    def _get_prompt_template(self):
        return """
        H: Use the following pieces of context to provide a concise answer to the question at the end. If you don't know the answer, just say that you don't know, don't try to make up an answer.
        <context>
        {context}
        </context>
        Question: {question}
        A:"""

    def _initialize_qa(self):
        return RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=vectorstore.as_retriever(
                search_type="similarity", search_kwargs={"k": 3}
            ),
            return_source_documents=True,
            chain_type_kwargs={"prompt": self.prompt}
        )

    def query(self, question):
        result = self.qa({"query": question})
        return result

# Initialize the DocumentQA instance
qa_instance = DocumentQA()
qa = qa_instance.qa  # alias for the qa function

if __name__ == '__main__':
    print("Initializing... Please wait...")
    print("Ready for questions!")
    
    while True:
        print("Please input your question (or 'quit' to exit):")
        query = input()
        
        if query.lower() == 'quit':
            break

        result = qa_instance.query(query)
        print_ww(result['result'])
        format_source_documents(result['source_documents'])