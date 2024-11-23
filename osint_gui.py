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
    # Read and log raw Sherlock output
    if os.path.exists(sherlock_output_file):
        with open(sherlock_output_file, 'r') as json_file:
            raw_data = json_file.read().strip()
            # print("Raw Sherlock JSON output:", raw_data)  # Debug log
            jsonFile = '{ '
            raw_data_line_list = raw_data.splitlines()
            # print("Raw Sherlock JSON output:", raw_data_line_list)
            raw_data_line_list = raw_data_line_list[3:]
            for i in raw_data_line_list:
                p = i[4:].split(": ")
                try:
                    jsonFile = jsonFile + '"' + p[0] + '":' + '"' + p[1] + '"' + ', '
                except:
                    print("Error:", p)
                # print("Raw Sherlock JSON output:", p, "\n")
            jsonFile = jsonFile[0:-2] + ' }'
            # print("JSON File output:", jsonFile, "\n")
            
            # Try parsing JSON after confirming content
            try:
                if raw_data:  # Check for non-empty output
                    parsed_data = json.loads(jsonFile)
                    return parsed_data
            except json.JSONDecodeError as e:
                print(f"Error parsing Sherlock JSON output: {e}")
    else:
        print("Sherlock output file is empty or missing.")
    return None

# 2. DetectDee Function with Enhanced Debugging
def run_detectdee(username):
    """Run DetectDee tool for a given username and parse JSON output."""
    detectdee_output_file = "DetectDee/DetectDee_output.json"
    command = f'cd DetectDee && go run DetectDee detect -n "{username}" --timeout 10 -o DetectDee_output.json '
    print(f"Running DetectDee command: {command}")  # Log command
    os.system(command)
    
    # Read and log raw DetectDee output
    if os.path.exists(detectdee_output_file):
        with open(detectdee_output_file, 'r') as json_file:
            raw_data = json_file.read().strip()
            # print("Raw DetectDee JSON output:", raw_data)  # Debug log
            
            jsonFile = '{ '
            raw_data_line_list = raw_data.splitlines()
            # print("Raw DetectDee JSON output:", raw_data_line_list)
            for i in raw_data_line_list:
                p = i.split(",")
                try:
                    jsonFile = jsonFile + '"' + p[1][1:] + '":' + '"' + p[2][1:] + '"' + ', '
                except:
                    print("Error:", p)
                # print("JSON output Line:", p, "\n")
            jsonFile = jsonFile[0:-2] + ' }'
            # print("JSON File output:", jsonFile, "\n")
            
            # Try parsing JSON after confirming content
            try:
                if raw_data:  # Check for non-empty output
                    parsed_data = json.loads(jsonFile)
                    return parsed_data
            except json.JSONDecodeError as e:
                print(f"Error parsing DetectDee JSON output: {e}")
    else:
        print("DetectDee output file is empty or missing.")
    return None

# 3. Comparison and Visualization Functions (unchanged)
def compare_results(sherlock_data, detectdee_data):
    """Compare Sherlock and DetectDee results to find common usernames and sites."""
    common_data = []
    if sherlock_data and detectdee_data:
        sherlock_sites = set(sherlock_data.keys())
        detectdee_sites = set(detectdee_data.keys())
        common_data = list(sherlock_sites & detectdee_sites)
    return common_data

def visualize_comparison(sherlock_data, detectdee_data, common_data):
    sherlock_count = len(sherlock_data) if sherlock_data else 0
    detectdee_count = len(detectdee_data) if detectdee_data else 0
    common_count = len(common_data)

    labels = ['Sherlock', 'DetectDee', 'Common']
    counts = [sherlock_count, detectdee_count, common_count]

    plt.bar(labels, counts, color=['blue', 'green', 'orange'])
    plt.xlabel('Tool')
    plt.ylabel('Number of Matches')
    plt.title('Comparison of Sherlock and DetectDee Results')
    plt.show()

# 4. GUI Setup and Execution
def run_osint():
    username = entry_username.get()
    sherlock_data = run_sherlock(username)
    detectdee_data = run_detectdee(username)
    
    print("sherlock_data: ",sherlock_data)
    print("detectdee_data: ", detectdee_data)

    text_output.delete("1.0", tk.END)
    text_output.insert(tk.END, "Sherlock Results:\n")
    if sherlock_data:
        for site, url in sherlock_data.items():
            text_output.insert(tk.END, f"{site}: {url}\n")
    else:
        text_output.insert(tk.END, "No results found from Sherlock.\n")
    
    text_output.insert(tk.END, "\nDetectDee Results:\n")
    if detectdee_data:
        for site, url in detectdee_data.items():
            text_output.insert(tk.END, f"{site}: {url}\n")
    else:
        text_output.insert(tk.END, "No results found from DetectDee.\n")

    common_results = compare_results(sherlock_data, detectdee_data)
    print("common_results: ", common_results)
    
    text_output.insert(tk.END, "\nCommon Findings:\n")
    if common_results:
        for site in common_results:
            text_output.insert(tk.END, f"{site}\n")
    else:
        text_output.insert(tk.END, "No common results found.\n")

    visualize_comparison(sherlock_data, detectdee_data, common_results)

# Initialize GUI
root = tk.Tk()
root.title("OSINT Automation - Sherlock vs DetectDee")

label_username = tk.Label(root, text="Enter Username:")
label_username.pack()

entry_username = tk.Entry(root, width=30)
entry_username.pack()

btn_run = tk.Button(root, text="Run OSINT", command=run_osint)
btn_run.pack()

text_output = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=60, height=20)
text_output.pack()

root.mainloop()
