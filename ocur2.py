import os
import sys
import re
from bs4 import BeautifulSoup
from BD import common_bangladeshi_names
from keywords import indian_keywords

# COLOURS
GREEN = "\33[38;5;46m"
WHITE = "\33[1;97m"
RED = "\33[1;91m"
BLUE = "\33[1;97m"
CYAN = "\33[1;97m"
X = f"{WHITE}[\33[1;91m~{WHITE}]"

# LINE
line = "\33[1;97m═" * 40
logo = f"""
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

# Function to read data from a file
def read_data_from_file(file_path):
    print(f"Loading File: {file_path}")
    with open(file_path, 'r') as file:
        data = file.readlines()
    return [line.strip() for line in data]

# Function to prompt user to input file path
def input_file_path():
    custom_path = input("Would you like to input a custom file path? (y/n): ").strip().lower()
    if custom_path == 'y':
        return input("Enter the path to your file: ").strip()
    else:
        return ['/sdcard/1.txt', '/sdcard/2.txt', '/sdcard/3.txt', '/sdcard/4.txt',
                '/sdcard/5.txt', '/sdcard/6.txt', '/sdcard/7.txt', '/sdcard/8.txt']

def is_bangladeshi(name):
    # Define a regex pattern for Bengali characters
    bengali_pattern = re.compile("[\u0980-\u09FF]")
    # Check if the name contains Bengali characters or is in the common Bangladeshi names set
    return bool(bengali_pattern.search(name)) or any(common_name in name for common_name in common_bangladeshi_names)

# Function to filter out non-Bangladeshi names
def filter_bangladeshi_names(data):
    filtered_data = []
    for entry in data:
        if '|' in entry:
            number, name = entry.split('|', 1)  # Split only at the first occurrence of '|'
            if is_bangladeshi(name):
                filtered_data.append(entry)
        else:
            print(f"Ignoring line: {entry} (Does not contain expected format)")
    return filtered_data

# Function to remove duplicate lines
def remove_duplicate_lines(data):
    print("Removing duplicates based on UID...")
    seen_uids = set()
    filtered_data = []
    for entry in data:
        uid = entry.split('|', 1)[0]
        if uid not in seen_uids:
            seen_uids.add(uid)
            filtered_data.append(entry)
    return filtered_data

# Function to sort lines lexicographically in descending order
def sort_lexicographically_descending(data):
    return sorted(data, reverse=True)

# Function to save filtered data to the same file
def save_to_same_file(filtered_data, file_path):
    """Save filtered data to a text file."""
    print(f"Saving filtered data to file: {file_path}")
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            for entry in filtered_data:
                file.write(entry + '\n')
    except IOError:
        print(f"Error saving to file '{file_path}'.")

def save_data_to_file(data, file_path):
    """Save filtered data to a text file."""
    print(f"Saving filtered data to file: {file_path}")
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            for entry in data:
                file.write(entry + '\n')
    except IOError:
        print(f"Error saving to file '{file_path}'.")

def contains_arabic(text):
    arabic_re = re.compile(r'[\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF]')
    return bool(arabic_re.search(text))

def remove_duplicates_by_uid(data):
    """Remove duplicates based on the UID."""
    print("Removing duplicates based on UID...")
    seen_uids = set()
    filtered_data = []
    for entry in data:
        uid = entry.split('|', 1)[0]
        if uid not in seen_uids:
            seen_uids.add(uid)
            filtered_data.append(entry)
    return filtered_data

def filter_names(data, indian_keywords):
    """Filter out data with Indian or Arabic names based on keywords and Arabic characters."""
    print("Filtering Out Others Country Uid...")
    filtered_data = []
    for entry in data:
        uid, name = entry.split('|', 1)
        
        # Check if any part contains Indian keywords or Arabic characters
        if not any(any(keyword in part for keyword in indian_keywords) or contains_arabic(part) for part in name.strip().split()):
            filtered_data.append(entry)
    
    return filtered_data

def sort_data_lexicographically_desc(data):
    return sorted(data, reverse=True)

def method_1():
    file_paths = input_file_path()
    if isinstance(file_paths, str):  # If a single custom file path is provided
        file_paths = [file_paths]
    for file_path in file_paths:
        if not os.path.exists(file_path):
            print(f"File not found: {file_path}")
            continue
        data = read_data_from_file(file_path)
        data = remove_duplicate_lines(data)
        filtered_data = filter_bangladeshi_names(data)
        filtered_data = sort_lexicographically_descending(filtered_data)
        save_data_to_file(sorted_data, file_path)
        print(f"\rProcessing completed Remaining Uid: {len(filtered_data)}\n")
        
def method_2():
    file_paths = input_file_path()
    if isinstance(file_paths, str):  # If a single custom file path is provided
        file_paths = [file_paths]
    for file_path in file_paths:
        if not os.path.exists(file_path):
            print(f"File not found: {file_path}")
            continue
        data = read_data_from_file(file_path)
        data = remove_duplicate_lines(data)
        filtered_data = filter_names(data, indian_keywords)
        sorted_data = sort_data_lexicographically_desc(filtered_data)
        save_data_to_file(sorted_data, file_path)
        print(f"\rProcessing completed Remaining Uid: {len(filtered_data)}\n")

# Main function
def main():
    sys.stdout.write('\x1b]2; INCEPTION \x07')
    line = f"{WHITE}━" * 40
    X = f"{WHITE}[\33[1;91m~{WHITE}]"
    def linex(): print(line)
    def clear(): os.system("clear"); print(logo)
    clear()  # Clear the screen and print the logo

    method_choice = input("Choose the method to run (1 or 2): ").strip()
    if method_choice == '1':
        method_1()
    elif method_choice == '2':
        method_2()
    else:
        print("Invalid choice. Please choose 1 or 2.")

# Execute the main function
if __name__ == "__main__":
    main()
