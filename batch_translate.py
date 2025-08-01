import time
import logging
from tqdm import tqdm
from itertools import islice
from ai_client_utils import get_client, get_response

# Configure logging to print timestamped info messages
logging.basicConfig(
    level=logging.INFO, 
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def chunks(iterable, n):
    """
    Split an iterable into chunks of size n.
    Used to divide subtitles into batches.
    """
    iterable = iter(iterable)
    while True:
        batch = list(islice(iterable, n))
        if not batch:
            break
        yield batch

def build_batch_prompt(subs, source_lang, target_lang):
    """
    Build a prompt for batch translation by including all subtitle lines,
    while enforcing rules to maintain structure (1:1 line correspondence).
    """
    prompt = f"Translate the following {source_lang} subtitles to {target_lang}.\n"
    prompt += "Rules:\n- Translate each line individually.\n"
    prompt += "- Do NOT merge or split lines.\n"
    prompt += f"- Return {target_lang} lines in the same order and count.\n\n"
    
    prompt += f"{source_lang} subtitles:\n"
    for idx, sub in enumerate(subs, 1):
        # Remove line breaks (\N when parsing with pysub2) inside the subtitle content for better formatting
        prompt += f"{idx}. {sub.text.replace('\\N',' ').strip()}\n"
    
    prompt += f"\n{target_lang} subtitles:\n"
    return prompt

def extract_lines_from_response(response):
    """
    Parse LLM response into separate translated lines by splitting on newlines
    and stripping index numbers like "1. ...".
    """
    lines = response.strip().split("\n")
    results = []
    for line in lines:
        if ". " in line:
            # Remove the line index (e.g., "1. سلام!")
            parts = line.split(". ", 1)
            results.append(parts[1].strip())
        else:
            results.append(line.strip())
    return results

def batch_translate(subtitles: list, batch_size: int, source_lang: str, target_lang: str, model_name: str):
    """
    Main function to translate subtitles in batches using a specified LLM model.
    
    Args:
        subtitles: list of subtitle objects (each with `.content`)
        batch_size: number of subtitles per translation batch
        source_lang: source language name (e.g., "English")
        target_lang: target language name (e.g., "Persian")
        model_name: name of the LLM model to use (e.g., "gemini-2.5-flash")
    
    Returns:
        A list of subtitle objects with their `.content` translated.
    """
    # Validate model selection
    if model_name == None:
        raise Exception("Specify model name with -m parameter.")
    if not subtitles:
        return []
    
    dialogue_lines = [s for s in subtitles if s.text.strip()]
    total_batches = (len(dialogue_lines) + batch_size - 1) // batch_size # total # of batches

    # Get API client instance from utility
    client = get_client(model_name)
    
    # Constants for Gemini rate limits
    GEMINI_RPM_LIMIT = 15  # Gemini's rate limit: requests per minute
    WAIT_TIME_SECONDS = 30  # wait time after hitting rate limit

    # Process each batch
    for i, batch in enumerate(tqdm(chunks(subtitles, batch_size), total=total_batches, desc="Translating")):
        prompt = build_batch_prompt(batch, source_lang, target_lang)
        
        try:
            # Send prompt to LLM model
            response_text = get_response(client, model_name, prompt)
            
            # Extract the translated lines
            translated_lines = extract_lines_from_response(response_text)
            
            # Ensure response has the same number of lines
            if len(translated_lines) != len(batch):
                logging.error("Mismatch in lines. Batch index: %d", i)
                logging.error("Original: %s", [s.text for s in batch])
                logging.error("Translated: %s", translated_lines)
                raise ValueError("Mismatch in number of lines returned from LLM.")

            # Assign translated text back to subtitle objects
            for sub, new_text in zip(batch, translated_lines):
                sub.text = new_text

        except Exception as e:
            logging.exception("Error translating batch %d: %s", i, e)
        
        # Respect LLM API's RPM limit
        if i > 0 and i % GEMINI_RPM_LIMIT == 0:
            logging.info(f"Waiting {WAIT_TIME_SECONDS} seconds for rate limits...")
            time.sleep(WAIT_TIME_SECONDS)

    return subtitles
