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
    #bengali_pattern = re.compile("[\u0980-\u09FF]")
    #return bool(bengali_pattern.search(name)) or any(common_name in name for common_name in bdn)
    return any(common_name in name for common_name in bdn)

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
            if len(name_parts) > 0 and name_parts[0] in ["Md", "MD", "Sk", "Md.", "Mst"]:
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

            
def method_5():
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
            # Filter lines containing 'Md', 'MD', or 'Md.'
            md_lines = [line for line in data if any(prefix in line for prefix in ["Md", "Md.", "Abdul", "Akhtar", "Ali", "Amin", "Anis", "Asif", "Aziz", "Bashir", "Bilal",
        "Faisal", "Farhan", "Habib", "Hassan", "Hossain", "Imran", "Iqbal", "Jamil", "Kamal", "Karim", 
    "Khan", "Mahmud", "Moin", "Monir", "Nasir", "Nawaz", "Rahim", "Rashid", "Rehman", "Salim", 
    "Sami", "Shahid", "Sharif", "Tariq", "Yasin", "Zaman", "Salman", "Wajid", "Sk", "Rahman", 
    "Hasan", "Parvez", "Shakil", "Shahin", "Sohel", "Tarek", "Sajjad", "Raju", "Shamim", 
    "Sumon", "Shahed", "Shakib", "Arif", "Sabbir", "Noman", "Shafi", "Shah", "Shahriar", "Tanvir", 
    "Rafi", "Masud", "Rafiq", "Rakib", "Sobuj", "Shuvo", "Faruk", "Nayeem", "Mehedi", "Munna", 
    "Anwar", "Kabir", "Shuvo", "Rajib", "Sohag", "Sajib", "Rony", "Sakib", "Shahjalal", "Nasim", 
    "Sakil", "Shuvojit", "Sujon", "Ashik", "Shafiq", "Mahfuz", "Habibullah", "Rasel", "Mizan", 
    "Monir", "Mithun", "Mamun", "Shanto", "Mehrab", "Rubel", "Sumon", "Sabbir", "Razib", "Khairul", 
    "Rafat", "Arafat", "Mahbub", "Nizam", "Biplab", "Pavel", "Arman", "Bijoy", "Shanto", "Hasib", 
    "Ranjan", "Masum", "Liton", "Shamim", "Nazim", "Tuhin", "Arman", "Forhad", "Sakif", "Jabed", 
    "Shakir", "Rifat", "Rakib", "Muntasir", "Biplob", "Tuhin", "Rabbi", "Rab", "Sourav", "Jony", 
    "Partha", "Pavel", "Sohan", "Ratul", "Rabiul", "Rifat", "Mizanur", "Jahid", "Alamin", "Tanjim", 
    "Mahir", "Sajal", "Rifat", "Ratul", "Sarwar", "Shihab", "Rajon", "Jamil", "Rasel", "Ahsan", 
    "Maruf", "Tanveer", "Sajjad", "Rifat", "Saiful", "Shohel", "Tuhin", "Anik", "Shuvo", "Ridoy", 
    "Arafat", "Saif", "Hasib", "Bipul", "Jewel", "Sakib", "Sahed", "Sujon", "Mehedi", "Rafat", 
    "Sakib", "Shihab", "Shamim", "Siam", "Munim", "Sharif", "Rana", "Shamim", "Rana", "Kawsar", 
    "Mahmud", "Akash", "Rafi", "Mahbub", "Munna", "Rasel", "Mehedi", "Shohel", "Rakib", "Nayeem", 
    "Rakib", "Mehedi", "Arafat", "Kawsar", "Tahsin", "Rasel", "Arif", "Biplob", "Rakib", "Sajjad", 
    "Tanzim", "Tuhin", "Mehedi", "Mehedi", "Hasan", "Rasel", "Rakib", "Shamim", "Munna", "Rony", 
    "Fahim", "Mehedi", "Jewel", "Rafsan", "Munna", "Shamim", "Najim", "Rakib", "Najim", "Sabbir", 
    "Shanto", "Biplob", "Mithun", "Shamim", "Nazim", "Mukul", "Tahsin", "Anisur", "Abdus", 
    "Mohammad", "Kazi", "Abul", "Nur", "Nazmul", "Sohel", "Monjur", "Arifur", "Mostafizur", 
    "Kamrul", "Sazzad", "Aminul", "Rashed", "Mahfuzur", "Monirul", "Shafiqul", "Imtiaz", "Enamul", 
    "Fakrul", "Mahmudul", "Samsul", "Abdur", "Farid", "Mizanur", "Jahirul", "Helal", "Shahidul", 
    "Liton", "Rezaul", "Jashim", "Selim", "Anwar", "Motiur", "Azizul", "Golam", "Habiba", "Hanif", 
    "Ibrahim", "Jamal", "Kabir", "Harun", "Masud", "Mahim", "Jisan", "Jibon", "Shofik", "Mustakim", 
    "Irfan", "Rahmatullah", "Fazlul", "Shamsul", "Afsar", "Mahbubul", "Shafayat", "Shariful", 
    "Iqra", "Anan", "Ishtiaq", "Ahad", "Ehsanul", "Abdullah", "Shabbir", "Liton", "Masum", 
    "Aklas", "Ashraful", "Atiq", "Mohiuddin", "Najmul", "Feroze", "Jaber", "Ashrafuzzaman", 
    "Mahbubur", "Nazib", "Sadiq", "Shahedul", "Imranul", "Muntashir", "Naushad", "Rashidur", "Touhid", 
    "Wali", "Mahfuzul", "Saad", "Azhar", "Naeem", "Shahiduzzaman", "Tazul", "Helaluddin", "Masudul", 
    "Murshed", "Nure Alam", "Nasrul", "Khalid", "Sayeed", "Maswood", "Shamsuzzaman", "Tanzir", 
    "Nahid", "Shaikh", "Rubayet", "Shadman", "Hasnain", "Shams", "Ibadur", "Arafatul", "Humaun", 
    "Akash", "Tarik", "Shuvo", "Arshad", "Bashar", "Junaid", "Khaled", "Mahin", "Nadir", "Wasim", 
    "Zubair", "Nazrul", "Rashedul", "Zakir", "Aftab", "Anwarul", "Asad", "Fazle", "Khorshed", 
    "Lokman", "Ishraq", "Touhidur", "Hassanuzzaman", "Nusratullah", "Tayef", "Tawfiq", "Zahedul", 
    "Shojib", "Abdulahi", "Shawkat", "Sadat", "Zahidur", "Hossainul", "Adnan", "Tarek", "Saeed",
    "Sk", "Amin", "Emran", "Rana", "Riad", "Shagor", "Kawsar", "Anis", "Ashraf", "Akbar", "Alim", 
    "Arif", "Azim", "Bashir", "Babar", "Badrul", "Baki", "Belal", "Bodi", "Bulbul", "Chowdhury", "Daud", "Dulal", 
    "Emon", "Enamul", "Fahim", "Farhad", "Faisal", "Ferdous", "Gafur", "Gazi", "Habib", "Hasib", "Hasan", "Helal", 
    "Hossain", "Ibrahim", "Imran", "Iqbal", "Ismail", "Jahid", "Jalal", "Jamil", "Jasim", "Kabir", "Kamal", "Karim", 
    "Khaled", "Liton", "Mahi", "Mahfuz", "Mamun", "Manik", "Masud", "Mizan", "Mokbul", "Moin", "Monir", "Mostafa", 
    "Mujib", "Murad", "Nafis", "Naim", "Nasim", "Nazmul", "Niaz", "Noman", "Nur", "Parvez", "Rafiqul", "Rakib", 
    "Rashed", "Razib", "Rezaul", "Sohel", "Riaz", "Ripon", "Rubel", "Sabbir", "Sadiq", "Sajid", "Salam", "Sami", 
    "Sanjib", "Shahid", "Shakib", "Shamsul", "Sharif", "Sohag", "Sumon", "Tariq", "Taufiq", "Touhid", "Wahid", 
    "Yasin", "Zahid", "Zahir", "Zakir", "Zaman", "Zia", "Zubair", "Abdul", "Abid", "Adnan", "Afif", "Ahad", "Ahmad", 
    "Ahsan", "Akash", "Ali", "Alim", "Aminul", "Amzad", "Anik", "Anwar", "Arifur", "Asad", "Ashfaq", "Atiq", "Azhar", 
    "Aziz", "Babu", "Badal", "Basir", "Bijoy", "Bilal", "Chanchal", "Delwar", "Dipu", "Ehsan", "Ershad", "Eshan", 
    "Fakhrul", "Faruq", "Fazle", "Golam", "Hafiz", "Hamid", "Haris", "Hasnat", "Hedayet", "Humayun", "Ilias", 
    "Ishtiaq", "Jabed", "Jafor", "Jamshed", "Johirul", "Junaid", "Kamrul", "Kawsar", "Khalil", "Khorshed", "Lalon", 
    "Latif", "Mahmud", "Majid", "Maksud", "Manjur", "Maruf", "Mazhar", "Mehedi", "Milton", "Minhaj", "Miraz", 
    "Mobarak", "Mohsin", "Morshed", "Muazzam", "Mubin", "Mujibur", "Mustafa", "Nadim", "Nahid", "Nasir", "Nazim", 
    "Niloy", "Nizam", "Noor", "Nure", "Obaid", "Omar", "Pavel", "Rahim", "Rakhat", "Rana", "Rasel", "Rifat", "Riyad", 
    "Rokon", "Ruhul", "Sabit", "Saiful", "Sajjad", "Salim", "Sarwar", "Shafiq", "Shahin", "Shakil", "Shamim", 
    "Shanto", "Sheikh", "Sohail", "Subho", "Tanjil", "Tanvir", "Tipu", "Tuhin", "Uzzal", "Wasim", "Younus", "Zafor", 
    "Zahidul", "Zakaria", "Zamal", "Zulfiqar", "Afsar", "Afzal", "Alam", "Amirul", "Ananta", "Anindya", "Ashik", 
    "Ashim", "Ashraful", "Atikur", "Aynal", "Azad", "Babul", "Bahauddin", "Barkat", "Bashar", "Bokul", "Danish", 
    "Ekram", "Fahad", "Faisal", "Farhan", "Farid", "Fayez", "Ferdous", "Gaziul", "Giyas", "Golam", "Harun", 
    "Hasanuzzaman", "Helal", "Himel", "Hiron", "Hossainul", "Hridoy", "Ibrahim", "Iftekhar", "Imtiaz", "Iqbal", 
    "Ishtiaque", "Jalil", "Jewel", "Jibon", "Kamal", "Kamrul", "Kawser", "Kazi", "Khaledur", "Latifur", "Liton", 
    "Lutfar", "Mahadi", "Mahbub", "Mahdi", "Majed", "Manik", "Maruf", "Masraf", "Masum", "Mazharul", "Mehdi", 
    "Milon", "Mizanur", "Mohammad", "Mohibur", "Moinul", "Mokhlesur", "Monowar", "Morsalin", "Mubarak", "Muhaimin", 
    "Mujahid", "Mustafizur", "Nadim", "Nahiyan", "Najmul", "Nayeem", "Nazir", "Nezam", "Nishat", "Niyaz", "Noorul", 
    "Oli", "Omar", "Parvez", "Rabbani", "Rabbi", "Rafique", "Raihan", "Rakibul", "Rashedul", "Reza", "Riazul", 
    "Rokonuzzaman", "Ruhul", "Rumana", "Saad", "Sabbir", "Sabir", "Sadi", "Saiful", "Sajeeb", "Sajidur", "Sajjadur", 
    "Salman", "Samad", "Samir", "Sanjoy", "Sarwar", "Saud", "Sazzad", "Shahidul", "Shahed", "Shahedul", "Shahriar", 
    "Shakibul", "Shamimul", "Shariful", "Shaukat", "Sohail", "Sujan", "Sumon", "Suruj", "Syed", "Tajul", "Tamal", 
    "Tanveer", "Tariqul", "Taufiqur", "Tipu", "Toufique", "Touhidul", "Uzzal", "Wasim", "Yasinul", "Yunus", 
    "Zahirul", "Zakariah", "Zayed", "Ziaul", "Zillur", "Zubayer", "Zulfiqar"])]
            save_data_to_file(md_lines, file_path)
            print(f"\rProcessing completed. Remaining Uid: {GREEN}{len(md_lines)}{reset_text}\n")
    
    if not_found_files:
        print("The following files were not found:")
        for file_path in not_found_files:
            print(file_path)
        input("Press Enter to go back to the main menu...")
        main()  # Go back to the main menu
            
           

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
    elif method_choice == '5':
        method_5()    
    else:
        print("Invalid choice. Please choose 1 or 2.")

if __name__ == "__main__":
    main()
