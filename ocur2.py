import re
from keywords import indian_keywords  # Importing the keywords list

def load_entries_from_file(file_path):
    """Load entries from a text file."""
    with open(file_path, 'r', encoding='utf-8') as file:
        entries = file.readlines()
    return [entry.strip() for entry in entries]

def save_entries_to_file(entries, file_path):
    """Save filtered entries to a text file."""
    with open(file_path, 'w', encoding='utf-8') as file:
        for entry in entries:
            file.write(entry + '\n')

def contains_arabic(text):
    """Check if the text contains Arabic characters."""
    arabic_re = re.compile(r'[\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF]')
    return bool(arabic_re.search(text))

def filter_names(entries, indian_keywords):
    """Filter out entries with Indian or Arabic names based on keywords and Arabic characters."""
    filtered_entries = []
    for entry in entries:
        uid, name = entry.split('|', 1)
        name = name.strip()
        if not any(keyword in name for keyword in indian_keywords) and not contains_arabic(name):
            filtered_entries.append(f"{uid}|{name}")
    return filtered_entries

def filter_and_save_to_same_file(file_path, indian_keywords):
    """Filter entries and save to the same file."""
    entries = load_entries_from_file(file_path)
    filtered_entries = filter_names(entries, indian_keywords)
    
    # Save filtered entries back to the same input file
    with open(file_path, 'w', encoding='utf-8') as file:
        for entry in filtered_entries:
            file.write(entry + '\n')

# Get input file path from the user
input_file_path = input("Enter the input file path: ")

# Filter entries and save to the same input file
filter_and_save_to_same_file(input_file_path, indian_keywords)

print(f"Filtered entries saved back to {input_file_path}")
