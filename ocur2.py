import os
import sys
import threading
import time
import re
from bs4 import BeautifulSoup
from BD import bdn
from IN import inn

# COLOURS
GREEN = "\33[38;5;46m"
reset_text = "\033[0m"
WHITE = "\33[1;97m"
RED = "\33[1;91m"
BLUE = "\33[1;97m"
CYAN = "\33[1;97m"
X = f"{WHITE}[\33[1;91m~{WHITE}]"

# LinnE
line = "\33[1;97m═" * 40
logo = f"""
{WHITE}
▀█▀ ░█▄─░█ ░█▀▀█ █▀▀█ 
░█─ ░█░█░█ ░█─── ──▀▄ 
▄█▄ ░█──▀█ ░█▄▄█ █▄▄█

{line}
{WHITE}[\33[1;91m~{WHITE}] AUTHOR    {WHITE} :  {GREEN}INCEPTION
{WHITE}[\33[1;91m~{WHITE}] VERSION   {WHITE} :  {RED}2
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
        clear_screen_and_print_logo()
        file_path = input("Enter the path to your file: ").strip()
        return file_path
    else:
        clear_screen_and_print_logo()
        return ['/sdcard/1.txt', '/sdcard/2.txt', '/sdcard/3.txt', '/sdcard/4.txt',
                '/sdcard/5.txt', '/sdcard/6.txt', '/sdcard/7.txt', '/sdcard/8.txt']

def is_bangladeshi(name):
    # Define a regex pattern for Bengali characters
    bengali_pattern = re.compile("[\u0980-\u09FF]")
    # Check if the name contains Bengali characters or is in the common Bangladeshi names set
    return bool(bengali_pattern.search(name)) or any(common_name in name for common_name in bdn)

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
       
def contains_hindi(text):
    hindi_re = re.compile(r'[\u0900-\u097F]')
    return bool(hindi_re.search(text))    
 
 
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

def filter_names(data, inn):
    print("Removing Indian Uid...")
    filtered_data = []
    for entry in data:
        uid, name = entry.split('|', 1)
        
        # Check if any part contains Indian IN or Arabic characters
        if not any(any(keyword in part for keyword in inn) or contains_arabic(part) or contains_hindi(part) for part in name.strip().split()):
            filtered_data.append(entry)
    
    return filtered_data
    
    
def rm_bd(data, bdn):
    print("Removing Bangladeshi Uid...")
    filtered_data = []
    
    for entry in data:
        if '|' in entry:
            uid, name = entry.split('|', 1)
            
            # If the name is NOT a common Bangladeshi name, keep it
            if not any(common_name in name for common_name in bdn):
                filtered_data.append(entry)
        else:
            print(f"Ignoring line: {entry} (Does not contain expected format)")
    
    return filtered_data



def sort_data_lexicographically_desc(data):
    return sorted(data, reverse=True)

def rm(data):
    updated_data = []
    for entry in data:
        if '|' in entry:  # Check if the entry contains the expected delimiter
            number, name = entry.split('|', 1)
            name_parts = name.split()
            if len(name_parts) > 0 and name_parts[0] in ["Md",  "MD", "Sk", "Md.",  "Mst"]:
                name = " ".join(name_parts[1:])  # Remove 'Md' or 'Mst' if it's the first name
            updated_data.append(f"{number}|{name}")
        else:
            print(f"Ignoring entry: {entry} (Does not contain expected format)")
            updated_data.append(entry)  # Keep the entry as is if it's not in the expected format
    return updated_data


def clear_screen_and_print_logo():
    os.system("clear")  # Clear the screen
    print(logo)         # Print the logo

def method_1():
    clear_screen_and_print_logo()
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
            print(f"\rProcessing completed Remaining Uid: {GREEN}{len(filtered_data)}{reset_text}\n")
    if not_found_files:
        print("The following files were not found:")
        for file_path in not_found_files:
            print(file_path)
        input("Press Enter to go back to the main menu...")
        main()  # Go back to the main menu

def method_2():
    clear_screen_and_print_logo()
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
            filtered_data = filter_names(data, inn)
            sorted_data = sort_data_lexicographically_desc(filtered_data)
            save_data_to_file(sorted_data, file_path)
            print(f"\rProcessing completed Remaining Uid: {GREEN}{len(filtered_data)}{reset_text}\n")
    
    if not_found_files:
        print("The following files were not found:")
        for file_path in not_found_files:
            print(file_path)
        input("Press Enter to go back to the main menu...")
        main()  # Go back to the main menu

def dup():
    clear_screen_and_print_logo()
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
            data = rm(data)
            save_data_to_file(data, file_path)
            print(f"\rProcessing completed Remaining Uid: {GREEN}{len(data)}{reset_text}\n")

    if not_found_files:
        print("The following files were not found:")
        for file_path in not_found_files:
            print(file_path)
        input("Press Enter to go back to the main menu...")
        main()  # Go back to the main menu    

def chk():
    clear_screen_and_print_logo()
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
            filtered_data = rm_bd(data, bdn)
            sorted_data = sort_data_lexicographically_desc(filtered_data)
            save_data_to_file(sorted_data, file_path)
            print(f"\rProcessing completed Remaining Uid: {GREEN}{len(filtered_data)}{reset_text}\n")

def main():
    sys.stdout.write('\x1b]2; INCEPTION \x07')
    clear_screen_and_print_logo()

    print('[1] Save Only Bangladeshi Uid')
    print('[2] Remove Indian Uid')
    print('[3] Remove Duplicate Uid')
    print('[4] Remove Bangladeshi uid\n')

    method_choice = input('[?] Your Choice : ').strip()

    if method_choice == '1':
        method_1()
    elif method_choice == '2':
        method_2()
    elif method_choice == '3':
        dup()
    elif method_choice == '4':
        chk()
    else:
        print("Invalid choice. Please choose 1 or 2.")

if __name__ == "__main__":
    main()
