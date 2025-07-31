import os
import time
import logging
from tqdm import tqdm
from itertools import islice
from ai_client_utils import get_client, get_response


# Configure logging
logging.basicConfig(
    level=logging.INFO, 
    format="%(asctime)s - %(levelname)s - %(message)s"
)
    
def chunks(iterable, n):
    """Yield successive n-sized chunks from iterable."""
    iterable = iter(iterable)
    while True:
        batch = list(islice(iterable, n))
        if not batch:
            break
        yield batch

def build_batch_prompt(subs, source_lang, target_lang):
    prompt = f"Translate the following {source_lang} subtitles to {target_lang}.\n"
    prompt += "Rules:\n- Translate each line individually.\n"
    prompt += "- Do NOT merge or split lines.\n"
    prompt += f"- Return {target_lang} lines in the same order and count.\n\n"
    
    prompt += f"{source_lang} subtitles:\n"
    for idx, sub in enumerate(subs, 1):
        prompt += f"{idx}. {sub.content.replace("\n",' ').strip()}\n"
    
    prompt += f"\n{target_lang} subtitles:\n"
    return prompt

def extract_lines_from_response(response):
    lines = response.strip().split("\n")
    results = []
    for line in lines:
        if ". " in line:
            parts = line.split(". ", 1)
            results.append(parts[1].strip())
        else:
            results.append(line.strip())
    return results

def batch_translate(subs:list, batch_size: int, source_lang: str, target_lang: str, model_name: str):
    """Translates subtitles in batch of texts using LLM API (OpenAI or Google API)."""
    if model_name == None:
        raise Exception("Specify model name with -m parameter.")
    if not subs:
        return []
    
    translated_texts = []
    total_batches = (len(subs) + batch_size - 1) // batch_size
    
    # Initialize client
    client = get_client(model_name)
    
    GEMINI_RPM_LIMIT = 15
    WAIT_TIME_SECONDS = 30
    for i, batch in enumerate(tqdm(chunks(subs, batch_size), total=total_batches, desc="Translating")):
        prompt = build_batch_prompt(batch, source_lang, target_lang)
        try:
            response_text = get_response(client, model_name, prompt)
            translated_lines = extract_lines_from_response(response_text)
            
            if len(translated_lines) != len(batch):
                logging.error("Mismatch in lines. Batch index: %d", i)
                logging.error("Original: %s", [s.content for s in batch])
                logging.error("Translated: %s", translated_lines)
                raise ValueError("Mismatch in number of lines returned from LLM.")

            for sub, new_text in zip(batch, translated_lines):
                sub.content = new_text

            translated_texts.extend(batch)

        except Exception as e:
            logging.exception("Error translating batch %d: %s", i, e)
        
        if i > 0 and i % GEMINI_RPM_LIMIT == 0:
            logging.info(f"Waiting {WAIT_TIME_SECONDS} seconds for rate limits...")
            time.sleep(WAIT_TIME_SECONDS)

    return translated_texts
