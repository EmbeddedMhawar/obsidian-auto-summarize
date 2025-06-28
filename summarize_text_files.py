import os
import re
import google.generativeai as genai
from datetime import datetime

# The directory where the script is located
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
# The parent directory, which contains the audio files
BASE_DIR = os.path.dirname(SCRIPT_DIR)
# The directory where the transcriptions are located
TRANSCRIPTIONS_DIR = os.path.join(BASE_DIR, 'transcriptions')
# The directory to save the summaries
SUMMARIES_DIR = os.path.join(BASE_DIR, 'summaries')

# --- Configuration ---
# IMPORTANT: Replace "YOUR_GEMINI_API_KEY" with your actual Gemini API key.
GEMINI_API_KEY = "AIzaSyA1Hq-xxxxxxxxx"  # Replace with your actual key

# Configure the Gemini API
genai.configure(api_key=GEMINI_API_KEY)

def find_text_files(directory):
    """Finds all .txt files in a directory."""
    text_files = []
    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            text_files.append(os.path.join(directory, filename))
    return text_files

def summarize_text(text):
    """Summarizes the given text using the Gemini API."""
    print("Summarizing with Gemini...")
    model = genai.GenerativeModel('gemini-1.5-flash-latest')  # Updated model
    # The prompt is now more generic to handle different types of text.
    prompt = f"""Please provide a concise summary of the following text:

{text}
"""
    response = model.generate_content(prompt)
    return response.text

def get_date_from_filename(filename):
    """Extracts a date from the filename to allow for sorting."""
    base_name = os.path.basename(filename)
    # Regex for MM-DD-YYYY
    match1 = re.search(r'(\d{2}-\d{2}-\d{4})', base_name)
    if match1:
        try:
            return datetime.strptime(match1.group(0), '%m-%d-%Y')
        except ValueError:
            pass
    
    # Regex for MyRec_MMDD_HHMM format
    match2 = re.search(r'MyRec_(\d{2})(\d{2})_\d{4}', base_name)
    if match2:
        try:
            # Assuming the current year for these recordings
            year = datetime.now().year
            month = int(match2.group(1))
            day = int(match2.group(2))
            return datetime(year, month, day)
        except ValueError:
            pass

    return None

def main():
    """Main function to find, sort, and summarize text files."""
    print(f"Searching for text files in: {os.path.abspath(TRANSCRIPTIONS_DIR)}")
    
    text_files = find_text_files(TRANSCRIPTIONS_DIR)
    
    if not text_files:
        print("No text files found.")
        return

    # Create a list of tuples (file, date) for files where a date can be extracted
    dated_files = []
    for text_file in text_files:
        date = get_date_from_filename(text_file)
        if date:
            dated_files.append((text_file, date))
        else:
            print(f"Warning: Could not extract date from '{os.path.basename(text_file)}'. Skipping this file.")

    # Sort files by date, descending    
    sorted_files = sorted(dated_files, key=lambda item: item[1], reverse=True)
        
    print(f"\nFound {len(sorted_files)} text file(s) with valid dates to process.")
    
    for text_file, _ in sorted_files:
        try:
            with open(text_file, "r", encoding="utf-8") as f:
                transcription = f.read()
            
            # Skip empty files
            if not transcription.strip():
                print(f"Skipping empty file: {os.path.basename(text_file)}")
                continue

            summary = summarize_text(transcription)
            
            base_filename = os.path.splitext(os.path.basename(text_file))[0]
            md_filename = os.path.join(SUMMARIES_DIR, f"{base_filename}.md")
            
            with open(md_filename, "w", encoding="utf-8") as f:
                f.write(f"# Summary for {base_filename}\n\n")
                f.write(summary)
                
            print(f"Successfully created summary: {md_filename}")

        except Exception as e:
            print(f"Could not process {text_file}. Error: {e}")

if __name__ == "__main__":
    if not GEMINI_API_KEY or GEMINI_API_KEY == "YOUR_GEMINI_API_KEY":
        print("ERROR: Please replace 'YOUR_GEMINI_API_KEY' in the script with your actual Gemini API key.")
    else:
        print("Starting summarization process...")
        main()
        print("\nProcess finished.")