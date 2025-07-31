import srt
import chardet
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

def read_srt_file(path):
    try:
        with open(path, 'rb') as f:  # Open in binary mode
            raw_data = f.read()

        # Detect the encoding
        result = chardet.detect(raw_data)
        encoding = result['encoding']

        if encoding is None:
            logging.warning("Error: Could not detect encoding.  Trying utf-8 as a fallback.")
            encoding = 'utf-8'  # Fallback to UTF-8 if detection fails

        # Decode the data using the detected encoding
        srt_content = raw_data.decode(encoding)
        return srt_content

    except FileNotFoundError:
        logging.exception("Error: Input file not found at %s", path)
        exit(1)
    except Exception as e:
        logging.exception("Error reading input file: %s", e)
        exit(1)

def write_srt_file(path, content):
    try:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        logging.info("Successfully saved to %s", path)
    except Exception as e:
        logging.info("Error writing output file: %s", e)
        exit(1)

def parse_srt_file(file_path):
    # Read the input SRT file
    srt_content = read_srt_file(args.file)

    # Parse the SRT content
    logging.info("Parsing %s file...", args.file)
    
    try:
        original_subtitles = list(srt.parse(srt_content))
    except srt.SRTParseError:
        logging.exception("Error: Failed to parse the SRT file.")
        exit(1)
        
    return original_subtitles

def main(args):
    # 1. Parse SRT file
    original_subtitles = parse_srt_file(args.file)
    if not original_subtitles:
        logging.error("Error: No subtitles found.")
        
    logging.info("Parsed %i subtitle entries.", len(original_subtitles))

    # 3. Translate the texts in batches
    try:
        translated_subtitles = batch_translate(original_subtitles, args.batch_size, args.source, args.target, args.model_name)
    except Exception as e:
        print(f"Translation failed: {e}")
        exit(1)
    
    translated_srt = srt.compose(translated_subtitles)

    # 4. Write the output SRT file
    write_srt_file(output_file, translated_srt)

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
        output_file = args.file.replace(".txt", ".srt") if args.file.endswith(".txt") else args.file + f"_{args.target}.srt"
        logging.info("Output file: %s", output_file)
        logging.info("Model name: %s", args.model_name)
        logging.info("Batch size: %i", args.batch_size)
    except AttributeError:
        logging.exception("You should specify a srt file path with -f argument.")
        exit(1)
    
    main(args)
    