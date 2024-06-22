import os
import re
from bs4 import BeautifulSoup
from keywords import indian_keywords  # Importing the keywords list

os.system('clear')

# COLOURS
GREEN = "\33[38;5;46m"
WHITE = "\33[1;97m"
RED = "\33[1;91m"
BLUE = "\33[1;97m"
CYAN = "\33[1;97m"
X = f"{WHITE}[\33[1;91m~{WHITE}]"

# LINE
line = "\33[1;97m═" * 40

# Logo and program information
program_info = f"""
{WHITE}
▀█▀ ░█▄─░█ ░█▀▀█ █▀▀█ 
░█─ ░█░█░█ ░█─── ──▀▄ 
▄█▄ ░█──▀█ ░█▄▄█ █▄▄█

{line}
{WHITE}[\33[1;91m~{WHITE}] AUTHOR    {WHITE} :  {GREEN}INCEPTION
{WHITE}[\33[1;91m~{WHITE}] VERSION   {WHITE} :  {RED}BETA
{WHITE}[\33[1;91m~{WHITE}] FEATURE   {WHITE} : {WHITE} OUT C UID RMVR
{line}
"""


def load_entries_from_file(file_path):
    """Load entries from a text file."""
    print(f"Loading entries from file: {file_path}")
    entries = []
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            entries = file.readlines()
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
    return [entry.strip() for entry in entries]

def save_entries_to_file(entries, file_path):
    """Save filtered entries to a text file."""
    print(f"Saving filtered entries to file: {file_path}")
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            for entry in entries:
                file.write(entry + '\n')
    except IOError:
        print(f"Error saving to file '{file_path}'.")

def contains_arabic(text):
    """Check if the text contains Arabic characters."""
    arabic_re = re.compile(r'[\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF]')
    return bool(arabic_re.search(text))

def remove_duplicates_by_uid(entries):
    """Remove duplicates based on the UID."""
    print("Removing duplicates based on UID...")
    seen_uids = set()
    filtered_entries = []
    for entry in entries:
        uid = entry.split('|', 1)[0]
        if uid not in seen_uids:
            seen_uids.add(uid)
            filtered_entries.append(entry)
    return filtered_entries

def filter_names(entries, indian_keywords):
    """Filter out entries with Indian or Arabic names based on keywords and Arabic characters."""
    print("Filtering Out Others Country Uid...")
    filtered_entries = []
    for entry in entries:
        uid, name = entry.split('|', 1)
        
        # Check if any part contains Indian keywords or Arabic characters
        if not any(any(keyword in part for keyword in indian_keywords) or contains_arabic(part) for part in name.strip().split()):
            filtered_entries.append(entry)
    
    return filtered_entries

def sort_entries_lexicographically_desc(entries):
    """Sort entries lexicographically in descending order."""
    print("Sorting entries lexicographically in descending order")
    return sorted(entries, reverse=True)

def get_file_paths():
    """Get input file paths from user input or use predefined paths."""
    custom_path = input("Would you like to input a custom file path? (y/n): ").strip().lower()
    if custom_path == 'y':
        return [input("Enter the path to your file: ").strip()]
    else:
        return [
            '/sdcard/1.txt', '/sdcard/2.txt', '/sdcard/3.txt', '/sdcard/4.txt',
            '/sdcard/5.txt', '/sdcard/6.txt', '/sdcard/7.txt', '/sdcard/8.txt'
        ]

def process_file(file_path, indian_keywords):
    """Process a single file: remove duplicates, filter names, and sort."""
    # Load entries from the input file
    entries = load_entries_from_file(file_path)

    # If entries are empty (indicating file not found or other error), return
    if not entries:
        return

    # Remove duplicates based on UID
    filtered_entries = remove_duplicates_by_uid(entries)

    # Filter out entries with Indian or Arabic names
    filtered_entries = filter_names(filtered_entries, indian_keywords)

    # Sort entries lexicographically in descending order
    sorted_entries = sort_entries_lexicographically_desc(filtered_entries)

    # Save the sorted entries back to the same input file
    save_entries_to_file(sorted_entries, file_path)
    print(f"Processing completed Remaining Uid: {len(filtered_entries)}")

if __name__ == "__main__":
    # Print program information and logo at the start
    print(program_info)

    # Get file paths either custom or predefined
    file_paths = get_file_paths()

    # Process each file in the list
    for file_path in file_paths:
        process_file(file_path, indian_keywords)

    # Print completion message at the end
    print(f"{X} {GREEN}Program completed successfully! Thank you for using.")
