import os
import pysubs2
import argparse 
import logging
from batch_translate import batch_translate


DEFAULT_SOURCE_LANG="English"
DEFAULT_TARGET_LANG="Persian"
DEFAULT_MODEL_NAME = "gemini-2.0-flash"
DEFAULT_BATCH_SIZE=200

# configure logging
logging.basicConfig(
    level=logging.INFO, 
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def read_subtitles(path):
    return pysubs2.load(path)

def write_subtitles(path, subtitles):
    subtitles.save(path)

def main(args):
    # 1. Parse SRT file
    try:
        original_subtitles = read_subtitles(args.file)
    except pysubs2.FormatAutodetectionError:
        logging.exception("Invalid subtitle file.")
    
    logging.info("Parsed %i subtitle entries.", len(original_subtitles))
    
    # 2. Translate the texts in batches 
    try:
        translated_subs = batch_translate(
            original_subtitles,
            args.batch_size,
            args.source,
            args.target,
            args.model_name)
    except Exception as e:
        print(f"Translation failed: {e}")
        exit(1)
    
    # 3. Write the output SRT file
    output_file = f"{os.path.splitext(args.file)[0]}_{args.target}{os.path.splitext(args.file)[1]}"
    write_subtitles(output_file, translated_subs)
    logging.info("Successfully saved to %s", output_file)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Translate SRT files using OpenAI or Google LLMs.")
    parser.add_argument("-s", "--source", default=DEFAULT_SOURCE_LANG, help="Source language (e.g., English)")
    parser.add_argument("-t", "--target", default=DEFAULT_TARGET_LANG, help="Target language (e.g., Persian)")
    parser.add_argument("-f", "--file", help="Input SRT file path")
    parser.add_argument("-m", "--model-name", default=DEFAULT_MODEL_NAME, help="Model name (One of Gemini or OpenAI models accessible via API)")
    parser.add_argument("-b", "--batch-size", default=DEFAULT_BATCH_SIZE, help="Batch size (Number of subtitle entries sent to the LLM each time)", type=int)

    args = parser.parse_args()
    
    try:
        logging.info("Input file: %s", args.file)        
        logging.info("Translating from %s to %s.", args.source, args.target)
        logging.info("Model name: %s", args.model_name)
        logging.info("Batch size: %i", args.batch_size)
    except AttributeError:
        logging.exception("You should specify a srt file path with -f argument.")
        exit(1)
    
    main(args)
    