import os
import re
from datetime import datetime

def get_date_from_filename(filename):
    """Extracts a date from a markdown filename to allow for sorting."""
    base_name = os.path.basename(filename)
    # Attempt to parse dates like '04-04-2025.md' or 'MyRec_0526_2113.md'
    match = re.search(r'(\d{2}-\d{2}-\d{4})', base_name) or re.search(r'MyRec_(\d{2})(\d{2})', base_name)
    if match:
        try:
            if '-' in match.group(0):
                # Format is MM-DD-YYYY
                return datetime.strptime(match.group(1), '%m-%d-%Y')
            else:
                # Format is MyRec_MMDD
                # Assuming the year is 2025 as per the context
                return datetime.strptime(f'2025-{match.group(1)}-{match.group(2)}', '%Y-%m-%d')
        except (ValueError, IndexError):
            # Return a default date for files that don't match to avoid crashing
            return datetime.min
    return datetime.min

def get_week_number(date_obj):
    """Returns the week number of the year for a given date."""
    return date_obj.isocalendar()[1]

def combine_markdown_files(directory=".", output_filename="all_summaries.md"):
    """Finds all .md files, sorts them by date, and combines them into one file."""
    md_files = [f for f in os.listdir(directory) if f.endswith('.md') and f != output_filename and f != 'automate_with_task_scheduler.md']

    if not md_files:
        print("No summary markdown files found to combine.")        
        return    

    # Sort files based on the extracted date    
    sorted_files = sorted(md_files, key=get_date_from_filename)

    print(f"Found {len(sorted_files)} summary files to combine. Combining in the following order:")
    for f in sorted_files:
        print(f"  - {f}")

    # Combine the content of the files
    current_week = None
    with open(os.path.join(directory, output_filename), 'w', encoding='utf-8') as outfile:
        outfile.write("# All Meeting Summaries\n\n")
        for filename in sorted_files:
            filepath = os.path.join(directory, filename)
            file_date = get_date_from_filename(filename)
            week_number = get_week_number(file_date)
            if week_number != current_week:
                current_week = week_number
                outfile.write(f"\n## Week {current_week} (Starting {file_date.strftime('%Y-%m-%d')})\n\n")
            with open(filepath, 'r', encoding='utf-8') as infile:
                outfile.write(infile.read())
                outfile.write("\n\n")

    # Combine the content of the files
    with open(os.path.join(directory, output_filename), 'w', encoding='utf-8') as outfile:
        outfile.write("# All Meeting Summaries\n\n")
        for filename in sorted_files:
            filepath = os.path.join(directory, filename)
            with open(filepath, 'r', encoding='utf-8') as infile:
                outfile.write(infile.read())
                outfile.write("\n\n---\n\n") # Add a separator between files

    print(f"Successfully combined all summaries into '{output_filename}'.")

if __name__ == "__main__":    
    summaries_directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "summaries")
    combine_markdown_files(directory=summaries_directory)
