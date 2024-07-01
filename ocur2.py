import os
import sys
import threading
import time
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

# Function to simulate an animation
def animate_message(message, delay=0.5, animation_length=3):
    sys.stdout.write(message)
    sys.stdout.flush()
    for i in range(animation_length):
        time.sleep(delay)
        sys.stdout.write(".")
        sys.stdout.flush()

# Function to display a spinner animation
def display_spinner(duration=2, delay=0.1):
    spinner = "|/-\\"
    end_time = time.time() + duration
    while time.time() < end_time:
        for char in spinner:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(delay)
            sys.stdout.write("\b")  # Erase the last character
            sys.stdout.flush()

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
    print("Saving Only Bangladeshi Uid", end="")
    animate_message("...")
    display_spinner()
    print(" Done!")
    filtered_data = []
    for entry in data:
        if '|' in entry:
            number, name = entry.split('|', 1)  # Split only at the first occurrence of '|'
            if is_bangladeshi(name):
                filtered_data.append(entry)
        else:
            print(f"Ignoring line: {entry} (Does not contain expected format)")
    return filtered_data

# Function to sort lines lexicographically in descending order
def sort_lexicographically_descending(data):
    return sorted(data, reverse=True)

def save_data_to_file(data, file_path):
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
    print("Removing duplicates UID...")
    seen_uids = set()
    filtered_data = []
    for entry in data:
        uid = entry.split('|', 1)[0]
        if uid not in seen_uids:
            seen_uids.add(uid)
            filtered_data.append(entry)
    return filtered_data

def filter_names(data, indian_keywords):
    print("Removing Indian Uid...")
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
    
    not_found_files = []
    
    for file_path in file_paths:
        if not os.path.exists(file_path):
            not_found_files.append(file_path)
        else:
            data = read_data_from_file(file_path)
            data = remove_duplicates_by_uid(data)
            filtered_data = filter_bangladeshi_names(data)
            filtered_data = sort_lexicographically_descending(filtered_data)
            save_data_to_file(filtered_data, file_path)
            print(f"\rProcessing completed Remaining Uid: {len(filtered_data)}\n")
    
    if not_found_files:
        print("The following files were not found:")
        for file_path in not_found_files:
            print(file_path)
    
    return_to_menu = input("Do you want to return to the main menu? (y/n): ").strip().lower()
    if return_to_menu != 'y':
        sys.exit(0)  # Exit the program

def method_2():
    file_paths = input_file_path()
    if isinstance(file_paths, str):  # If a single custom file path is provided
        file_paths = [file_paths]
    
    not_found_files = []
    
    for file_path in file_paths:
        if not os.path.exists(file_path):
            not_found_files.append(file_path)
        else:
            data = read_data_from_file(file_path)
            data = remove_duplicates_by_uid(data)
            filtered_data = filter_names(data, indian_keywords)
            sorted_data = sort_data_lexicographically_desc(filtered_data)
            save_data_to_file(sorted_data, file_path)
            print(f"\rProcessing completed Remaining Uid: {len(filtered_data)}\n")
    
    if not_found_files:
        print("The following files were not found:")
        for file_path in not_found_files:
            print(file_path)
    
    return_to_menu = input("Do you want to return to the main menu? (y/n): ").strip().lower()
    if return_to_menu != 'y':
        sys.exit(0)  # Exit the program

def main():
    sys.stdout.write('\x1b]2; INCEPTION \x07')
    line = f"{WHITE}━" * 40
    X = f"{WHITE}[\33[1;91m~{WHITE}]"
    
    def linex(): 
        print(line)
    
    def clear(): 
        os.system("clear")  # Clear the screen
        print(logo)  # Print your logo after clearing

    clear()

    while True:
        print('[1] Save Only Bangladeshi Uid')
        print('[2] Remove Indian Uid')
        print()  # Add a new line for spacing

        method_choice = input('[?] Your Choice: ').strip()

        if method_choice == '1':
            clear_above_lines(4)
            method_1()
        elif method_choice == '2':
            clear_above_lines(4)  # Clear menu options, prompt, and input line
            method_2()
        else:
            break

def clear_above_lines(n):
    # ANSI escape code: move cursor up 'n' lines and clear each line
    for _ in range(n):
        sys.stdout.write('\x1b[1A')  # Move cursor up one line
        sys.stdout.write('\x1b[2K')  # Clear the line

if __name__ == "__main__":
    main()
