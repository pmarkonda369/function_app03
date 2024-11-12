import openai
import requests
from dotenv import load_dotenv
import os

load_dotenv()
load_dotenv(override=True)

openai.api_type = os.getenv('OPENAI_API_TYPE')
openai.api_base = os.getenv('OPENAI_API_BASE')
openai.api_key = os.getenv('OPENAI_API_KEY')
openai.api_version = os.getenv('OPENAI_API_VERSION')

search_endpoint = os.getenv('SEARCH_ENDPOINT')
search_key = os.getenv('SEARCH_KEY')
search_index = os.getenv('SEARCH_INDEX')

def search_azure_cognitive(query1):
    headers = {
        'Content-Type': 'application/json',
        'api-key': search_key
    }
    
    search_url = f"{search_endpoint}/indexes/{search_index}/docs/search?api-version=2021-04-30-Preview"

    search_payload = {
        "search": query1,
        "queryType": "semantic",
        "top": 5,
        "queryLanguage": "en-us",
        "semanticConfiguration": "default"
    }
    
    response = requests.post(search_url, json=search_payload, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        return f"Search Error: {response.status_code}, {response.text}"

def generate_openai_response(query1):
    search_results = search_azure_cognitive(query1)
    
 
    chat_prompt = [
        {"role": "system", "content": "You are an AI assistant that helps people find information."},
        {"role": "user", "content": query1}
    ]

 
    if isinstance(search_results, dict) and 'value' in search_results:
        search_content = "\n".join([result['content'] for result in search_results['value']])
        chat_prompt.append({"role": "system", "content": f"Here is some relevant information from documents:\n{search_content}"})        


    response = openai.ChatCompletion.create(
        engine="gpt-35-turbo-16k",
        messages=chat_prompt,
        max_tokens=800,
        temperature=0.7,
        top_p=0.95,
        frequency_penalty=0,
        presence_penalty=0,
        
    )
    
    return response.choices[0].message['content']

