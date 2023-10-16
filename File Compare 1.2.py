import tkinter as tk
from tkinter import filedialog, messagebox
import difflib
from datetime import datetime
import os

# Function to open a file with the default application
def open_file(file_path):
    try:
        os.system(f'start "" "{file_path}"')
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while opening the file: {str(e)}")

# Function to compare two text files for inconsistencies
def compare_text_files(file1_path, file2_path):
    try:
        # Check if file paths are provided
        if not file1_path or not file2_path:
            messagebox.showerror("Error", "Please provide file paths for both File 1 and File 2.")
            return

        # Check and strip any leading/trailing double quotes from file paths
        file1_path = file1_path.strip('"')
        file2_path = file2_path.strip('"')

        # Check if the file paths are valid and files exist
        if not (is_valid_file(file1_path) and is_valid_file(file2_path)):
            return

        # Read the content of both files
        with open(file1_path, 'r', encoding='utf-8') as file1, open(file2_path, 'r', encoding='utf-8') as file2:
            file1_lines = file1.readlines()
            file2_lines = file2.readlines()

        # Check if both files have the same number of lines
        if len(file1_lines) != len(file2_lines):
            messagebox.showerror("Error", f"These files do not contain the same amount of lines.\n\nFile 1 contains {len(file1_lines)} lines.\nFile 2 contains {len(file2_lines)} lines.\n\nPlease compare files with the same amount of lines.")
            return

        # Use difflib to compare the files and find differences
        differ = difflib.Differ()
        diff = list(differ.compare(file1_lines, file2_lines))

        # Filter out common lines and whitespace differences
        diff_lines = [line for line in diff if line.startswith('- ') or line.startswith('+ ')]

        # Count the number of differences found
        diff_count = len(diff_lines)

        # Get the directory path of file1
        file1_directory = os.path.dirname(file1_path)

        # Create a results file name with date and time appended
        current_datetime = datetime.now().strftime("%m-%d-%Y_%I-%M-%p")
        results_file_name = os.path.join(file1_directory, f"Results_{current_datetime}.txt")

        # Check if differences were found and no exceptions occurred
        if diff_count > 0:
            with open(results_file_name, 'w', encoding='utf-8') as results_file:
                # Write the comparison results to the file
                results_file.write("Comparison Results:\n")
                results_file.write(f"{diff_count} difference(s) found.\n")
                results_file.write("Differences:\n")
                i = 1  # Initialize line counter
                for line in diff_lines:
                    results_file.write(f"Difference found on line {i}:\n")
                    if line.startswith('- '):
                        if i <= len(file1_lines):
                            file1_line = file1_lines[i - 1].strip()  # Remove leading/trailing whitespace
                            if file1_line == '\n':
                                results_file.write(f"Line #{i} from File 1 is a newline character.\n")
                            else:
                                results_file.write(f"Line #{i} from File 1: {file1_line}\n")
                    elif line.startswith('+ '):
                        if i <= len(file2_lines):
                            results_file.write(f"Line #{i} from File 2: {file2_lines[i - 1]}")
                    i += 1  # Increment line counter
            messagebox.showinfo("Comparison Results", f"{diff_count} difference(s) were found.\n\nResults saved to '{results_file_name}'.")
            # Open the results file after displaying the results pop-up
            open_file(results_file_name)
        else:
            with open(results_file_name, 'w', encoding='utf-8') as results_file:
                results_file.write("Comparison Results:\n")
                results_file.write("Your files match exactly.\n")
            messagebox.showinfo("Comparison Results", f"Your files match exactly. Results saved to '{results_file_name}'.")
            # Open the results file after displaying the results pop-up
            open_file(results_file_name)

        # Ask the user if they want to continue if 10 differences are found
        if diff_count >= 10:
            user_choice = messagebox.askyesno("Continue?", "10 differences have been found. Would you like to continue?")
            if not user_choice:
                open_file(results_file_name)

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

# Function to check if a file exists and is not empty
def is_valid_file(file_path):
    if not file_path:
        return False
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return bool(file.read())
    except FileNotFoundError:
        messagebox.showerror("Error", f"File '{file_path}' not found.")
        return False

# Create the main UI window
root = tk.Tk()
root.title("File Comparison Program")
root.geometry("1000x200")

# Create labels and entry fields for file paths
file1_label = tk.Label(root, text="File 1 Path:")
file1_label.grid(row=0, column=0)
file1_entry = tk.Entry(root, width=100)
file1_entry.grid(row=0, column=1)

file2_label = tk.Label(root, text="File 2 Path:")
file2_label.grid(row=1, column=0)
file2_entry = tk.Entry(root, width=100)
file2_entry.grid(row=1, column=1)

# Create a button to trigger the file comparison
compare_button = tk.Button(root, text="Compare Files", command=lambda: compare_text_files(file1_entry.get(), file2_entry.get()))
compare_button.grid(row=2, column=0, columnspan=2)

# Start the main UI loop
root.mainloop()
