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

def remove_duplicates_by_uid(entries):
    """Remove duplicates based on the UID."""
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
    filtered_entries = []
    for entry in entries:
        uid, name = entry.split('|', 1)
        
        # Check if any part contains Indian keywords or Arabic characters
        if not any(any(keyword in part for keyword in indian_keywords) or contains_arabic(part) for part in name.strip().split()):
            filtered_entries.append(entry)
    
    return filtered_entries

def get_file_paths():
    """Get input and output file paths from the user."""
    input_file_path = input("Enter the input file path: ")
    return input_file_path

# Get input file path from the user
input_file_path = get_file_paths()

# Load entries from the input file
entries = load_entries_from_file(input_file_path)

# Remove duplicates based on UID
filtered_entries = remove_duplicates_by_uid(entries)

# Filter out entries with Indian or Arabic names
filtered_entries = filter_names(filtered_entries, indian_keywords)

# Save the filtered entries back to the same input file
save_entries_to_file(filtered_entries, input_file_path)

print(f"Filtered entries (Duplicates removed and Indian names removed) saved back to {input_file_path}")
