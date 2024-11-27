from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from bedrock_client import BedrockClient
from output_format import print_ww
from langchain.llms.bedrock import Bedrock

class Translator:
    def __init__(self):
        self.boto3_bedrock = BedrockClient.get_client()
        self.llm = Bedrock(model_id='anthropic.claude-instant-v1', client=self.boto3_bedrock)
        self.prompt = PromptTemplate(
            template=self._get_prompt_template(),
            input_variables=["source_language", "target_language", "text_to_translate"]
        )
        self.qa = self._initialize_qa()

    def _get_prompt_template(self):
        return """
        Translate the following text from {source_language} to {target_language}:

        Text:
        {text_to_translate}

        Translation:"""

    def _initialize_qa(self):
        return LLMChain(
            llm=self.llm,
            prompt=self.prompt
        )

    def query(self, source_language, target_language, text_to_translate):
        result = self.qa.run({
            "source_language": source_language,
            "target_language": target_language,
            "text_to_translate": text_to_translate
        })
        return result

# Initialize the Translator instance
translator = Translator()

if __name__ == '__main__':
    print("Initializing... Please wait...")
    print("Ready for translation!")

    while True:
        print("Please input the source language (or 'quit' to exit):")
        source_language = input()
        if source_language.lower() == 'quit':
            break

        print("Please input the target language:")
        target_language = input()

        print("Please input the text to translate:")
        text_to_translate = input()

        result = translator.query(source_language, target_language, text_to_translate)
        print_ww(result)