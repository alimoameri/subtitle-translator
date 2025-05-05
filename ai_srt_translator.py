import argparse 
from srt_to_json import parse_srt
from translate_batch import translate_batch

DEFAULT_SOURCE_LANG="English"
DEFAULT_TARGET_LANG="Persian"
DEFAULT_BATCH_SIZE=200

def read_srt_file(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            srt_content = f.read()
            return srt_content
    except FileNotFoundError:
        print(f"Error: Input file not found at {path}")
        exit(1)
    except Exception as e:
        print(f"Error reading input file: {e}")
        exit(1)

def reconstruct_srt(subtitles, translated_texts):
    """Reconstructs the SRT file content from original data and translated text."""
    srt_output = []
    for i, sub in enumerate(subtitles):
        try:
            entry = f"{sub['index']}\n{sub['timecode']}\n{translated_texts[i]}\n"  # Access the first element of the list
            srt_output.append(entry)
        except IndexError:
            print(f"Warning: Skipping subtitle {i} due to translation error.")
            continue

    return "\n".join(srt_output)

def main():
    parser = argparse.ArgumentParser(description="Translate SRT files using OpenAI or Google LLMs.")
    parser.add_argument("-s", "--source", default=DEFAULT_SOURCE_LANG, help="Source language (e.g., English)")
    parser.add_argument("-t", "--target", default=DEFAULT_TARGET_LANG, help="Target language (e.g., Persian)")
    parser.add_argument("-f", "--file", help="Input SRT file path")
    parser.add_argument("-m", "--model-name", help="Model name (One of Gemini or OpenAI models accessible via API)")
    parser.add_argument("-b", "--batch-size", default=DEFAULT_BATCH_SIZE, help="Batch size (Number of subtitle entries sent to the LLM each time)")

    args = parser.parse_args()

    print(f"Starting SRT translation from {args.source} to {args.target}")
    try:
        print(f"Input file: {args.file}")
        output_file = args.file.replace(".txt", ".srt") if args.file.endswith(".txt") else args.file + f"_{args.target}.srt"
        print(f"Output file: {output_file}")
        print(f"Model name: {args.model_name}")
    except AttributeError:
        print(f"You should specify a srt file path with -f argument.")
        exit(1)
        

    # 1. Read the input SRT file
    srt_content = read_srt_file(args.file)

    # 2. Parse the SRT content
    print(f"Parsing {args.file} file...")
    original_subtitles = parse_srt(srt_content)

    if not original_subtitles:
        print("Error: No subtitles found or failed to parse the SRT file.")
        exit(1)
    print(f"Parsed {len(original_subtitles)} subtitle entries.")

    # 3. Extract texts for translation
    texts_to_translate = [sub['text'] for sub in original_subtitles]

    # 4. Translate the texts in batches
    try:
        translated_chunks = translate_batch(texts_to_translate, args.source, args.target, args.model_name, args.batch_size)
    except Exception as e:
        print(f"Translation failed: {e}")
        exit(1)

    translated_texts = []
    for chunk in translated_chunks:
      translated_texts += chunk
  
    # 5. Reconstruct the SRT file with translated text
    print("Reconstructing translated SRT file...")
    try:
        final_srt_content = reconstruct_srt(original_subtitles, translated_texts)
    except ValueError as e:
        print(f"Error during reconstruction: {e}")
        exit(1)

    # 6. Write the output SRT file
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(final_srt_content)
        print(f"Successfully translated and saved to {output_file}")
    except Exception as e:
        print(f"Error writing output file: {e}")
        exit(1)

if __name__ == "__main__":
    main()