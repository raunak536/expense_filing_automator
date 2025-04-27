from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()
client = OpenAI()

def parse_text(text):
    chat_history = [{'role':'system',
                     'content':"You are a helpful assistant."},
                    {'role': 'user',
                     'content': f"""I ran tessearct OCR on a bill and OCR text is this : {text}. 
                     Please extract date of  bill and total bill amount from this
                     and output just these 2 things : 
                     Date : [date here]
                     Total : [total bill amount here]
NOTE : If you cant extract either of these with high confidence please mention Not Found instead."""}]
    response = client.responses.create(model="gpt-4o-mini", input=chat_history)
    return response.output_text

