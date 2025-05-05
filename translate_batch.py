import os
from tqdm import tqdm
from google import genai
from openai import OpenAI
from dotenv import load_dotenv
from instructions import translation_prompt_template


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
    translated_text_combined = None
    
    if isinstance(client, OpenAI):
        response = client.responses.create(
            model=model_name,
            input=prompt,
        )
        translated_text_combined = response.output_text.strip()

    elif isinstance(client, genai.client.Client):
        response = client.models.generate_content(
            model=model_name,
            contents=prompt,
        )
        translated_text_combined = response.text.strip()
        
    return translated_text_combined
    
def translate_batch(texts:list, source_lang: str, target_lang: str, model_name: str, batch_size: int=200):
    """Translates a batch of texts using the LLM (OpenAI or Google API)."""
    if model_name == None:
        raise Exception("Specify model name with -m parameter.")
    if not texts:
        return []

    TEXT_SEPARATOR = "||SEP||"
    batches = []
    # Constrcuting batches for passing to the LLM one at a time
    for i in range(0, len(texts), batch_size):
        batch = TEXT_SEPARATOR.join(texts[i:i+batch_size])
        batch = batch.replace('\n', ' ')
        batches.append(batch)

    print(f"Sending {len(batches)} chunks of {batch_size} text blocks to {model_name} for translation...")
    
    # Initialize client
    client = get_client(model_name)
    translated_texts = []
    
    for batch in tqdm(batches):
        prompt = translation_prompt_template.invoke(
            {"source_lang": source_lang,
             "target_lang": target_lang,
             "TEXT_SEPARATOR": TEXT_SEPARATOR}).text + batch
        translated_combined = get_response(client, model_name, prompt)
        translated_texts.append(translated_combined.split(TEXT_SEPARATOR))

    return translated_texts
