# SRT Translator Using LLMs

This tool leverages large language models (LLMs) to translate SRT (SubRip Subtitle) files automatically. It handles the translation process by reading the subtitles, performing translation in batches, and then outputting a new SRT file that maintains the original formatting and timing. The system is optimized for English to Persian translation.

## Features

*   **Automated Translation:** Translates SRT files from a source language to a target language using the Google models or OpenAI models accessible via API.
*   **Batch Processing:** The system processes subtitles in configurable batches. Parameter `-b/--bath-size` determines how many subtitle entries are sent to the LLM in each translation request.
*   **Subtitle Format Preservation:**  Maintains the original SRT file structure (timecodes, sequence numbers). The system makes a best effort to preserve the original SRT file structure—including timecodes and sequence numbers—but may occasionally encounter issues that result in formatting discrepancies. Trying different batch sizes and models may fix the issue.
*   **HTML Tag Handling:**  Preserves HTML-like tags (e.g., `<i>`, `<b>`) within the subtitles.
*   **Command-Line Interface:**  Easy to use from the command line with customizable options.

## Prerequisites

*   **Google Gemini or OpenAI API Key:** You need a Google Gemini or OpenAI API key to use this script.  You can obtain a free Google API from [Google AI Studio](https://aistudio.google.com/).
*   **Python Packages:** They are listed in the `requirements.txt` file.

## Installation

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/alimoameri/ai-srt-translator.git
    cd ai-srt-translator
    ```

2.  **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

3.  **Set up your API key:**

    *   **Recommended:** Create a `.env` file in the project directory and add your API key(s):

        ```
        GOOGLE_API_KEY=YOUR_GOOGLE_API_KEY
        OPENAPI_API_KEY=YOUR_GOOGLE_API_KEY
        OPENAPI_BASE_URL=YOUR_OPENAPI_BASE_URL
        ```

    *   Alternatively, you can set these environment variabless directly in your shell.

## Usage

```bash
python3 ai_srt_translator.py -s <source_language> -t <target_language> -f <input_srt_file>
```

**Arguments:**

options:
  * `-h`, `--help`            show this help message and exit

  * `-s`, `--source`
                        Source language (Default is English)

  * `-t`, `--target`
                        Target language (Default is Persian)

  * `-f`, `--file` Input SRT file path

  * `-m`, `--model-name`
                        Model name (One of Gemini or OpenAI models accesible via API)

  * `-b`, `--batch-size`
                        Batch size (Number of subtitle entries sent to the LLM each time; Default is 200)

**Example:**

To translate `Spider-man-TAS-S01E01-Night-of-the-Lizard-English.srt` from English to Persian:

```bash
python3 srt_translator.py -s English -t Persian -f Spider-man-TAS-S01E01-Night-of-the-Lizard-English.srt
```

The translated SRT file will be saved as `Spider-man-TAS-S01E01-Night-of-the-Lizard-English.srt_Persian.srt`.


## Contributing

Contributions are welcome!  Please feel free to submit pull requests or open issues if you find any bugs or have suggestions for improvements.

## License

This project is licensed under the [MIT License](LICENSE).
