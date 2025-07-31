import os
from google import genai
from openai import OpenAI
from dotenv import load_dotenv

def get_client(model_name: str):
    client = None
    
    # Load environment variables from .env file
    load_dotenv() 
    
    if "gpt" in model_name: 
        # Initialize OpenAI client
        API_KEY = os.getenv("OPENAI_API_KEY")
        OPENAPI_BASE_URL = os.getenv("OPENAPI_BASE_URL")
        if not API_KEY:
            raise ValueError("OpenAI API key not found. Set OPENAI_API_KEY environment variable or in a .env file.")
        if not OPENAPI_BASE_URL:
            raise ValueError("OpenAI Base Url not found. Set OPENAPI_BASE_URL environment variable or in a .env file.")
        
        client = OpenAI(
           base_url=OPENAPI_BASE_URL,
            api_key=API_KEY
        )
    elif "gemma" in model_name or "gemini" in model_name:
        # Initialize Gemini or Gemma client
        API_KEY = os.getenv("GOOGLE_API_KEY")
        if not API_KEY:
            raise ValueError("Google API key not found. Set GOOGLE_API_KEY environment variable or in a .env file.")
        
        client = genai.Client(api_key=API_KEY)
    else:
        raise Exception("Invalid model name.")
        
    return client

def get_response(client, model_name, prompt):
    response_text = None
    
    if isinstance(client, OpenAI):
        response = client.responses.create(
            model=model_name,
            input=prompt,
        )
        response_text = response.output_text

    elif isinstance(client, genai.client.Client):
        response = client.models.generate_content(
            model=model_name,
            contents=prompt,
        )
        response_text = response.text
        
    return response_text
