import os
import json
import tkinter as tk
from tkinter import scrolledtext
import matplotlib.pyplot as plt

# 1. Sherlock Function with Enhanced Debugging
def run_sherlock(username):
    """Run Sherlock tool for a given username and parse JSON output."""
    sherlock_output_file = "sherlock_output.json"
    command = f'python3 sherlock/sherlock_project/sherlock.py "{username}" --output json > sherlock_output.json --timeout 10'
    print(f"Running Sherlock command: {command}")  # Log command
    
    # Execute Sherlock command
    os.system(command)
    print("Path exists:", os.path.exists(sherlock_output_file))
    if os.path.exists(sherlock_output_file):
        with open(sherlock_output_file, 'r') as json_file:
            raw_data = json_file.read().strip()
            jsonFile = '{ '
            raw_data_line_list = raw_data.splitlines()[3:]  # Skip metadata
            for line in raw_data_line_list:
                parts = line[4:].split(": ")
                try:
                    jsonFile += f'"{parts[0]}": "{parts[1]}", '
                except:
                    print("Error parsing line:", parts)
            jsonFile = jsonFile[:-2] + ' }'
            
            try:
                if raw_data:
                    return json.loads(jsonFile)
            except json.JSONDecodeError as e:
                print(f"Error parsing Sherlock JSON output: {e}")
    else:
        print("Sherlock output file is empty or missing.")
    return None

# 2. DetectDee Functions for Username, Email, and Phone Number
def run_detectdee_username(username):
    """Run DetectDee for username."""
    return run_detectdee_generic("detect -n", username)

def run_detectdee_email(email):
    """Run DetectDee for email."""
    return run_detectdee_generic("detect -e", email)

def run_detectdee_phoneno(phone_no):
    """Run DetectDee for phone number."""
    return run_detectdee_generic("detect -p", phone_no)

def run_detectdee_generic(command_option, value):
    """Run DetectDee with a generic option."""
    detectdee_output_file = "DetectDee/DetectDee_output.json"
    command = f'cd DetectDee && go run DetectDee {command_option} "{value}" --timeout 10 -o DetectDee_output.json'
    print(f"Running DetectDee command: {command}")
    os.system(command)
    
    if os.path.exists(detectdee_output_file):
        with open(detectdee_output_file, 'r') as json_file:
            raw_data = json_file.read().strip()
            jsonFile = '{ '
            raw_data_line_list = raw_data.splitlines()
            for line in raw_data_line_list:
                parts = line.split(",")
                try:
                    jsonFile += f'"{parts[1][1:]}": "{parts[2][1:]}", '
                except:
                    print("Error parsing line:", parts)
            jsonFile = jsonFile[:-2] + ' }'
            
            try:
                if raw_data:
                    return json.loads(jsonFile)
            except json.JSONDecodeError as e:
                print(f"Error parsing DetectDee JSON output: {e}")
    else:
        print("DetectDee output file is empty or missing.")
    return None

# 3. Comparison and Visualization Functions
def compare_results(data1, data2):
    """Compare results between two data sets."""
    if data1 and data2:
        set1 = set(data1.keys())
        set2 = set(data2.keys())
        return list(set1 & set2)
    return []

def visualize_comparison(sherlock_data, username_data, email_data, phone_data, comparison1, comparison2):
    """Visualize comparison results."""
    sherlock_count = len(sherlock_data) if sherlock_data else 0
    username_count = len(username_data) if username_data else 0
    email_count = len(email_data) if email_data else 0
    phone_count = len(phone_data) if phone_data else 0
    comparison1_count = len(comparison1)
    comparison2_count = len(comparison2)

    labels = ['Sherlock', 'DetectDee U', 'DetectDee E', 'DetectDee P', 'Comparison 1', 'Comparison 2']
    counts = [sherlock_count, username_count, email_count, phone_count, comparison1_count, comparison2_count]

    plt.bar(labels, counts, color=['blue', 'green', 'orange', 'purple', 'red', 'cyan'])
    plt.xlabel('Category')
    plt.ylabel('Number of Matches')
    plt.title('OSINT Results Comparison')
    plt.show()

# 4. GUI Setup and Execution
def run_osint():
    """Run OSINT tools and display results."""
    username = entry_username.get()
    email = entry_email.get()
    phone_no = entry_phone_no.get()

    sherlock_data = run_sherlock(username)
    detectdee_username_data = run_detectdee_username(username)
    detectdee_email_data = run_detectdee_email(email)
    detectdee_phone_data = run_detectdee_phoneno(phone_no)

    text_output.delete("1.0", tk.END)
    text_output.insert(tk.END, "Sherlock Results:\n")
    if sherlock_data:
        for site, url in sherlock_data.items():
            text_output.insert(tk.END, f"{site}: {url}\n")
    else:
        text_output.insert(tk.END, "No results found from Sherlock.\n")
    
    text_output.insert(tk.END, "\nDetectDee Username Results:\n")
    if detectdee_username_data:
        for site, url in detectdee_username_data.items():
            text_output.insert(tk.END, f"{site}: {url}\n")
    else:
        text_output.insert(tk.END, "No results found for username in DetectDee.\n")
    
    text_output.insert(tk.END, "\nDetectDee Email Results:\n")
    if detectdee_email_data:
        for site, url in detectdee_email_data.items():
            text_output.insert(tk.END, f"{site}: {url}\n")
    else:
        text_output.insert(tk.END, "No results found for email in DetectDee.\n")

    text_output.insert(tk.END, "\nDetectDee Phone Number Results:\n")
    if detectdee_phone_data:
        for site, url in detectdee_phone_data.items():
            text_output.insert(tk.END, f"{site}: {url}\n")
    else:
        text_output.insert(tk.END, "No results found for phone number in DetectDee.\n")
    
    comparison1 = compare_results(sherlock_data, detectdee_username_data)
    comparison2 = compare_results(detectdee_email_data, detectdee_phone_data)

    text_output.insert(tk.END, "\nComparison Between Sherlock and Username DetectDee:\n")
    if comparison1:
        for site in comparison1:
            text_output.insert(tk.END, f"{site}\n")
    else:
        text_output.insert(tk.END, "No common results found.\n")

    text_output.insert(tk.END, "\nComparison Between Email and Phone Number in DetectDee:\n")
    if comparison2:
        for site in comparison2:
            text_output.insert(tk.END, f"{site}\n")
    else:
        text_output.insert(tk.END, "No common results found.\n")

    visualize_comparison(
        sherlock_data,
        detectdee_username_data,
        detectdee_email_data,
        detectdee_phone_data,
        comparison1,
        comparison2
    )

# GUI Setup
root = tk.Tk()
root.title("OSINT Automation - Sherlock and DetectDee")

label_username = tk.Label(root, text="Enter Username:")
label_username.pack()
entry_username = tk.Entry(root, width=30)
entry_username.pack()

label_email = tk.Label(root, text="Enter Email:")
label_email.pack()
entry_email = tk.Entry(root, width=30)
entry_email.pack()

label_phone_no = tk.Label(root, text="Enter Phone Number:")
label_phone_no.pack()
entry_phone_no = tk.Entry(root, width=30)
entry_phone_no.pack()

btn_run = tk.Button(root, text="Run OSINT", command=run_osint)
btn_run.pack()

text_output = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=80, height=25)
text_output.pack()

root.mainloop()
