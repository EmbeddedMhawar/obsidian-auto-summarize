import os
import re
import whisper

# The directory where the script is located
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
# The parent directory, which contains the audio files
BASE_DIR = os.path.dirname(SCRIPT_DIR)
# The directory to save the transcriptions
TRANSCRIPTIONS_DIR = os.path.join(BASE_DIR, 'transcriptions')

def find_audio_files(directory):
    """
    Finds unique audio files, preferring non-suffixed ones like 'file.m4a' over 'file (1).m4a'.

    Args:
        directory (str): The directory to search.

    Returns:
        dict: Maps clean base names to the full path of the preferred audio file.
    """
    audio_extensions = {".m4a", ".mp3", ".wav", ".flac"}
    found_files = {}
    # Sort to ensure 'file.m4a' is processed before 'file (1).m4a'.
    for filename in sorted(os.listdir(directory)):
        base_name, ext = os.path.splitext(filename)
        if ext.lower() in audio_extensions:
            clean_base_name = re.sub(r'\s*\(\d+\)$', '', base_name)
            if clean_base_name not in found_files:
                found_files[clean_base_name] = os.path.join(directory, filename)
    return found_files

def transcribe_audio(model, file_path):
    """
    Transcribes a single audio file, now with robust error handling.

    Args:
        model: The pre-loaded Whisper model.
        file_path (str): The path to the audio file.

    Returns:
        str or None: The transcribed text, or None if an error occurs.
    """
    print(f"Transcribing {os.path.basename(file_path)}...")
    try:
        # The TypeError likely occurs inside this call.
        result = model.transcribe(file_path, fp16=False, verbose=False)
        
        # Defensive check for valid result.
        if isinstance(result, dict) and "text" in result:
            return result["text"]
        else:
            print(f"Warning: Transcription for {os.path.basename(file_path)} returned an invalid result.")
            return None
    except Exception as e:
        # Catch the error from whisper, report it, and allow the script to continue.
        print(f"Error during transcription of '{os.path.basename(file_path)}': {e}")
        return None

def main():
    """Main function to find and transcribe unique audio files."""
    print(f"Searching for unique audio files in: {os.path.abspath(BASE_DIR)}")
    
    audio_files_map = find_audio_files(BASE_DIR)
    
    if not audio_files_map:
        print("No unique audio files found.")
        return
        
    print(f"Found {len(audio_files_map)} unique audio file(s).")

    files_to_process = {}
    for clean_base_name, audio_file in audio_files_map.items():
        output_filename = os.path.join(TRANSCRIPTIONS_DIR, clean_base_name + ".txt")
        if not os.path.exists(output_filename):
            files_to_process[clean_base_name] = audio_file
        else:
            print(f"Skipping '{os.path.basename(audio_file)}' as transcription '{os.path.basename(output_filename)}' already exists.")

    if not files_to_process:
        print("\nAll audio files have already been transcribed.")
        return

    print("\nLoading Whisper model...")
    model = whisper.load_model("base")
    print("Model loaded.")
    
    print(f"\nProcessing {len(files_to_process)} new audio file(s)...")
    for clean_base_name, audio_file in files_to_process.items():
        transcription = transcribe_audio(model, audio_file)
        
        # Process only if transcription was successful and is not empty.
        if transcription and transcription.strip():
            output_filename = os.path.join(TRANSCRIPTIONS_DIR, clean_base_name + ".txt")
            with open(output_filename, "w", encoding="utf-8") as f:
                f.write(transcription.strip())
            print(f"Successfully transcribed and saved to {output_filename}")
        else:
            # This handles both errors during transcription and empty results.
            print(f"Skipping '{os.path.basename(audio_file)}' due to empty or failed transcription.")

if __name__ == "__main__":
    print("Starting transcription process...")
    main()
    print("\nTranscription process finished.")
