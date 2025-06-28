# Automating Transcription with Windows Task Scheduler

This guide explains how to set up a scheduled task on Windows to automatically run the `transcribe_audio.py` script. This will help you keep your audio recordings transcribed without manual intervention.

## Prerequisites

1.  **Python Installed:** Ensure you have Python installed on your system and that it's added to your system's PATH. You can download it from [python.org](https://www.python.org/).
2.  **Whisper Library Installed:** You must install the `openai-whisper` library. Open Command Prompt or PowerShell and run:
    ```bash
    pip install openai-whisper
    ```
    You will also need `ffmpeg` on your system, which Whisper uses for audio processing. You can download it from [ffmpeg.org](https://ffmpeg.org/download.html) and add it to your system's PATH.

## Steps to Create the Scheduled Task

1.  **Open Task Scheduler:**
    *   Press `Win + R` to open the Run dialog.
    *   Type `taskschd.msc` and press Enter.

2.  **Create a New Task:**
    *   In the right-hand "Actions" pane, click on **"Create Basic Task..."**.

3.  **Name the Task:**
    *   **Name:** `Automated Audio Transcription`
    *   **Description:** `Runs a Python script to transcribe new audio files in my recordings folder.`
    *   Click **Next**.

4.  **Set the Trigger:**
    *   Choose how often you want the script to run (e.g., **"Daily"** or **"Weekly"**).
    *   Click **Next** and specify the time you want the task to start. A time when your computer is likely to be on but not under heavy use is ideal.
    *   Click **Next**.

5.  **Define the Action:**
    *   Select **"Start a program"** and click **Next**.

6.  **Configure the Program/Script:**
    *   **Program/script:** Enter the full path to your Python executable. If you don't know it, you can find it by running `where python` in Command Prompt. It's often something like `C:\Python39\python.exe`.
    *   **Add arguments (optional):** Enter the full path to the Python script. In this case: `C:\Users\mhawa\My Drive (mhawar2020@gmail.com)\Obsidian\0.2 Excalidraw\Recordings\Raw\transcribe_audio.py`
    *   **Start in (optional):** This is **very important**. Set this to the directory where your audio files and the script are located. In this case: `C:\Users\mhawa\My Drive (mhawar2020@gmail.com)\Obsidian\0.2 Excalidraw\Recordings\Raw`

7.  **Finalize the Task:**
    *   Review the summary and click **Finish**.

## Verifying the Task

You can run the task manually to ensure it works correctly:
1.  Find the task in the Task Scheduler Library.
2.  Right-click on it and select **"Run"**.
3.  Check the folder for new `.txt` files corresponding to your audio files.

That's it! The script will now run automatically according to the schedule you set.

## Automating Summarization with the Gemini API

To fully automate the process, you can modify the Python script to also summarize the transcribed text using the Gemini API. This creates a single, powerful script that handles everything from transcription to summarization.

### 1. Get a Gemini API Key

First, you need an API key to use the Gemini API.

1.  Go to the [Google AI for Developers](https://ai.google.dev/) website.
2.  Click on **"Get API key in Google AI Studio"**.
3.  Sign in with your Google account.
4.  Create a new API key. Make sure to copy and save it in a secure location.

### 2. Install the Google Generative AI Library

Next, install the necessary Python library. Open Command Prompt or PowerShell and run:

```bash
pip install google-generativeai
```

### 3. Update the Python Script

Now, you'll need to modify the `transcribe_audio.py` script to include the summarization logic. I will create a new script called `transcribe_and_summarize.py` that includes this new functionality.

This updated script will:
1.  Transcribe the audio to text (as before).
2.  Take the transcribed text and send it to the Gemini API with a prompt asking for a summary.
3.  Save the summary directly to a Markdown file.

You will need to add your Gemini API key to this new script.

This end-to-end automation is a more robust and efficient way to achieve your goal.

