import os
import re
import google.generativeai as genai

# --- Configuration ---
# IMPORTANT: Replace "YOUR_GEMINI_API_KEY" with your actual Gemini API key.
GEMINI_API_KEY = "AIzaSyA1Hq-xxxxxxxx"  # Replace with your actual key

# Configure the Gemini API
genai.configure(api_key=GEMINI_API_KEY)

def find_text_files(directory="."):
    """Finds all .txt files in a directory."""
    text_files = []
    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            text_files.append(os.path.join(directory, filename))
    return text_files

def extract_action_items(text):
    """Extracts action items from the given text using the Gemini API."""
    print("Extracting action items with Gemini...")
    model = genai.GenerativeModel('gemini-1.5-flash-latest')
    prompt = f"From the following meeting transcription, identify and list all action items. Format them as a simple sprint backlog, using bullet points. If possible, infer who is responsible and a rough due date (e.g., 'next week', 'end of sprint'). If no action items are found, state 'No action items identified.'.\n\n---\n{text}\n---\n"
    
    response = model.generate_content(prompt)
    return response.text

def main():
    """Main function to find text files and extract action items."""
    current_directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "transcriptions")
    print(f"Searching for text files in: {os.path.abspath(current_directory)}")
    
    text_files = find_text_files(current_directory)
    
    if not text_files:
        print("No text files found to extract action items from.")
        return
        
    print(f"Found {len(text_files)} text file(s) to process.")
    
    output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "action_items")
    os.makedirs(output_dir, exist_ok=True)  # Create the directory if it doesn't exist
    output_filename = os.path.join(output_dir, "sprint_backlog.md")
    with open(output_filename, "w", encoding="utf-8") as outfile:
        outfile.write("# Sprint Backlog - Action Items\n\n")
        
        for text_file in text_files:
            try:
                with open(text_file, "r", encoding="utf-8") as f:
                    transcription = f.read()
                
                action_items = extract_action_items(transcription)
                
                outfile.write(f"## From: {os.path.basename(text_file)}\n")
                outfile.write(action_items)
                outfile.write("\n\n---\n\n") # Separator
                
                print(f"Successfully extracted action items from {os.path.basename(text_file)}")

            except Exception as e:
                print(f"Could not process {text_file}. Error: {e}")

    print(f"All action items compiled into {output_filename}")

if __name__ == "__main__":
    if GEMINI_API_KEY == "YOUR_GEMINI_API_KEY":
        print("ERROR: Please replace 'YOUR_GEMINI_API_KEY' in the script with your actual Gemini API key.")
    else:
        print("Starting action item extraction process...")
        main()
        print("Process finished.")
