# Audio Transcription and Summarization Scripts

This repository contains Python scripts to automate the transcription of audio recordings and the summarization of the resulting text using OpenAI's Whisper and the Google Gemini API.

## Scripts

*   `transcribe_audio.py`:  This script finds audio files (m4a, mp3, wav, flac) in the specified directory, transcribes them using the Whisper ASR model, and saves the transcriptions as `.txt` files.
*   `summarize_text_files.py`: This script takes the `.txt` transcriptions, extracts dates from the filenames, and generates summaries using the Google Gemini API. The summaries are saved as Markdown files (`.md`).
*   `combine_summaries.py`: This script combines multiple Markdown summary files into a single file, optionally grouping summaries by week.

## Setup

1.  **Install Dependencies:**

    ```bash
    pip install openai-whisper google-generativeai
    ```

2.  **Get a Google Gemini API Key:**

    *   You'll need a Google Gemini API key to use the summarization feature.  You can obtain one from the [Google AI Studio](https://aistudio.google.com/app/apikey).
    *   **Important:**  Store your API key securely.  **Do not commit it directly to the repository.** The scripts are currently configured to read the API key directly from the script files.  For better security, you should use environment variables (see below).

3.  **Configure API Keys (Recommended: Use Environment Variables):**

    *   **Option 1 (Less Secure):** Edit `summarize_text_files.py` and `transcribe_and_summarize.py` and replace  `GEMINI_API_KEY = "YOUR_GEMINI_API_KEY"` with your actual API key.
    *   **Option 2 (More Secure):** Set the `GEMINI_API_KEY` environment variable on your system.  The scripts will automatically use the key from the environment.

## Usage

1.  **Transcribe Audio:**
    ```bash
    python transcribe_audio.py
    ```
    This will transcribe audio files in the same directory as the script and save the transcriptions in the `transcriptions` subdirectory.

2.  **Summarize Transcriptions:**
    ```bash
    python summarize_text_files.py
    ```
    This will summarize the transcriptions found in the `transcriptions` directory and save the summaries as Markdown files in the `summaries` subdirectory.

3.  **Combine Summaries (Optional):**
    ```bash
    python combine_summaries.py
    ```
    This will combine the summary files in the `summaries` directory into a single file named `all_summaries.md`.
