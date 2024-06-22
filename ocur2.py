#Original Code Written by Raysul_Rabby

import re
from keywords import indian_keywords

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
        name = entry.split('|')[1]
        if not any(keyword in name for keyword in indian_keywords) and not contains_arabic(name):
            filtered_entries.append(entry)
    return filtered_entries

def get_file_paths():
    """Get input and output file paths from the user."""
    input_file_path = input("Enter the input file path: ")
    output_file_path = input("Enter the output file path: ")
    return input_file_path, output_file_path

# Get input and output file paths from the user
input_file_path, output_file_path = get_file_paths()

# Load entries from the input file
entries = load_entries_from_file(input_file_path)

# Filter out entries with Indian or Arabic names
filtered_entries = filter_names(entries, indian_keywords)

# Save the filtered entries to the output file
save_entries_to_file(filtered_entries, output_file_path)

print(f"Filtered entries saved to {output_file_path}")
