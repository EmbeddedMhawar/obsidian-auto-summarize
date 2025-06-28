import os
import re
import whisper
import google.generativeai as genai

# --- Configuration ---
# IMPORTANT: Replace "YOUR_GEMINI_API_KEY" with your actual Gemini API key.
GEMINI_API_KEY = "YOUR_GEMINI_API_KEY"

# Configure the Gemini API
genai.configure(api_key=GEMINI_API_KEY)

def find_audio_files(directory="."):
    """Finds unique audio files in a directory, ignoring duplicates like (1)."""
    audio_extensions = {".m4a", ".mp3", ".wav", ".flac"}
    found_files = {}
    for filename in os.listdir(directory):
        base_name, ext = os.path.splitext(filename)
        if ext.lower() in audio_extensions:
            base_name = re.sub(r'\(\d+\)$', '', base_name)
            if base_name not in found_files:
                found_files[base_name] = os.path.join(directory, filename)
    return list(found_files.values())

def transcribe_audio(file_path):
    """Transcribes a single audio file using Whisper."""
    print("Loading Whisper model...")
    model = whisper.load_model("base")
    print(f"Transcribing {os.path.basename(file_path)}...")
    result = model.transcribe(file_path, fp16=False)
    return result["text"]

def summarize_text(text):
    """Summarizes the given text using the Gemini API."""
    print("Summarizing with Gemini...")
    model = genai.GenerativeModel('gemini-pro')
    prompt = f"Please summarize the following text from a meeting:   
    response = model.generate_content(prompt)
    return response.text

def main():
    """Main function to find, transcribe, and summarize unique audio files."""
    current_directory = "."
    print(f"Searching for unique audio files in: {os.path.abspath(current_directory)}")
    
    audio_files = find_audio_files(current_directory)
    
    if not audio_files:
        print("No unique audio files found.")
        return
        
    print(f"Found {len(audio_files)} unique audio file(s) to process.")
    
    for audio_file in audio_files:
        try:
            # 1. Transcribe
            transcription = transcribe_audio(audio_file)
            
            # 2. Summarize
            summary = summarize_text(transcription)
            
            # 3. Save to Markdown
            base_filename = os.path.splitext(os.path.basename(audio_file))[0]
            # Clean up the base filename to get the date
            date_str = re.sub(r'\(\d+\)$', '', base_filename).replace("MyRec_", "").replace("_", "-")
            md_filename = f"{date_str}.md"
            
            with open(md_filename, "w", encoding="utf-8") as f:
                f.write(f"# Summary for {date_str}\n\n")
                f.write(summary)
                
            print(f"Successfully created summary: {md_filename}")

        except Exception as e:
            print(f"Could not process {audio_file}. Error: {e}")

if __name__ == "__main__":
    if GEMINI_API_KEY == "YOUR_GEMINI_API_KEY":
        print("ERROR: Please replace 'YOUR_GEMINI_API_KEY' in the script with your actual Gemini API key.")
    else:
        print("Starting transcription and summarization process...")
        main()
        print("Process finished.")