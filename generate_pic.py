import json
import base64
import io
from PIL import Image
import boto3
import botocore
from output_format import print_ww
from chat import qa_instance
from bedrock_client import BedrockClient

class DocumentAnalyzer:
    def __init__(self, qa_instance):
        self.qa = qa_instance
    
    def get_document_summary(self):
        query = "What are the main topics and key concepts in this document? Summarize in 2-3 sentences."
        result = self.qa.query(query)
        return result['result']
    
    def get_design_concept(self):
        query = "Based on this document, suggest a professional cover design concept focusing on key visual elements and style."
        result = self.qa.query(query)
        return result['result']

class ImageGenerator:
    def __init__(self, bedrock_client):
        self.client = bedrock_client
        self.model_id = "stability.stable-diffusion-xl-v1"
    
    def create_prompt(self, summary, design_elements):
        return f"""Create a professional document cover design with these specifications:
        - Style: Modern, corporate, minimalist
        - Main focus: {summary}
        - Design elements: {design_elements}
        - Include subtle financial or administrative imagery
        - Use a clean, professional color palette with blues and grays
        - Maintain professional business document aesthetics
        - High quality, photorealistic rendering
        - Centered composition with clear hierarchy
        """
    
    def generate_image(self, prompt):
        body = json.dumps({
            "text_prompts": [{"text": prompt}],
            "cfg_scale": 10,
            "seed": 20,
            "steps": 50,
            "style_preset": "photographic"
        })
        
        try:
            response = self.client.invoke_model(
                body=body,
                modelId=self.model_id,
                accept="application/json",
                contentType="application/json"
            )
            return json.loads(response.get("body").read())
        except botocore.exceptions.ClientError as error:
            self._handle_error(error)
    
    def _handle_error(self, error):
        if error.response['Error']['Code'] == 'AccessDeniedException':
            print(f"\x1b[41m{error.response['Error']['Message']}\n"
                  "To troubleshoot this issue please refer to:\n"
                  "https://docs.aws.amazon.com/IAM/latest/UserGuide/troubleshoot_access-denied.html\n"
                  "https://docs.aws.amazon.com/bedrock/latest/userguide/security-iam.html\x1b[0m\n")
        else:
            raise error

def display_image(base64_str):
    image_bytes = base64.decodebytes(bytes(base64_str, "utf-8"))
    image = Image.open(io.BytesIO(image_bytes))
    image.show()
    return image

def main():
    # Initialize clients
    boto3_bedrock = BedrockClient.get_client()
    
    # Create analyzers
    doc_analyzer = DocumentAnalyzer(qa_instance)
    img_generator = ImageGenerator(boto3_bedrock)
    
    # Generate content
    summary = doc_analyzer.get_document_summary()
    print_ww(summary)
    
    design_concept = doc_analyzer.get_design_concept()
    print_ww(design_concept)
    
    # Generate image
    prompt = img_generator.create_prompt(summary, design_concept)
    response = img_generator.generate_image(prompt)
    
    # Display results
    print(response["result"])
    base64_img = response.get("artifacts")[0].get("base64")
    display_image(base64_img)

if __name__ == "__main__":
    main()