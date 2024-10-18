import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox
from pymarc import MARCReader

def open_file():
    global records
    file_path = filedialog.askopenfilename(filetypes=[("MARC files", "*.mrc"), ("All files", "*.*")])
    if file_path:
        with open(file_path, 'rb') as fh:
            reader = MARCReader(fh)
            records = [record for record in reader]
            display_records(records)
        enable_buttons()

def display_records(records):
    left_text.delete(1.0, tk.END)
    for record in records:
        left_text.insert(tk.END, str(record) + "\n\n")

def convert_to_aleph_seq():
    right_text.delete(1.0, tk.END)
    for i, record in enumerate(records, start=1):
        record_number = f"{i:09d}"
        for field in record.fields:
            if field.is_control_field():
                if field.tag in ["001", "002", "003", "004", "005", "006", "007", "008", "009"]:
                    line = f"{record_number} {field.tag}   L {field.data}"
                else:
                    line = f"{record_number} {field.tag} L {field.data}"
            else:
                indicators = f"{field.indicator1}{field.indicator2}"
                subfields = ' '.join(f"$$${code}{value}" for code, value in field.subfields_as_dict().items())
                if field.tag in ["001", "002", "003", "004", "005", "006", "007", "008", "009"]:
                    line = f"{record_number} {field.tag}   {indicators} L {subfields}"
                else:
                    line = f"{record_number} {field.tag}{indicators} L {subfields}"
            right_text.insert(tk.END, line + "\n")

def convert_to_aleph_seq_and_remove_brackets():
    convert_to_aleph_seq()
    remove_brackets()

def save_output():
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("SAV files", "*.sav"), ("Text files", "*.txt"), ("All files", "*.*")])
    if file_path:
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(right_text.get(1.0, tk.END))

def remove_brackets():
    output = right_text.get(1.0, tk.END)
    output = output.replace("['", " ").replace("']", " ").replace('["', " ").replace('"]', " ").replace("$$$", "$$")
    right_text.delete(1.0, tk.END)
    right_text.insert(tk.END, output)

def clear_frames():
    left_text.delete(1.0, tk.END)
    right_text.delete(1.0, tk.END)
    disable_buttons()

def show_help():
    help_text = (
        "This program is made in Python 3.10.11, using tkinter and pymarc.\n"
        "Created by Oren Maurer, with help from CoPilot. \n\n"
        "1. Open File: Choose a MARC file to display.\n"
        "2. Convert to Aleph SEQ: Convert and display the MARC records in Aleph SEQ format.\n"
        "3. Convert to ALEPH _ SEQ + []: Convert to Aleph SEQ format and remove [' and '] and correct subfield markers.\n"
        "4. Save Output As: Save the displayed output to a file.\n"
        "5. Remove []: Remove [' and '] from the output and correct subfield markers.\n"
        "6. Clear: Clear all displayed content.\n"
        "7. Exit: Exit the application."
    )
    messagebox.showinfo("Help", help_text)

def enable_buttons():
    convert_button.config(state=tk.NORMAL)
    convert_and_remove_button.config(state=tk.NORMAL)
    save_button.config(state=tk.NORMAL)
    remove_button.config(state=tk.NORMAL)
    clear_button.config(state=tk.NORMAL)
    # help_button.config(state=tk.NORMAL)

def disable_buttons():
    convert_button.config(state=tk.DISABLED)
    convert_and_remove_button.config(state=tk.DISABLED)
    save_button.config(state=tk.DISABLED)
    remove_button.config(state=tk.DISABLED)
    clear_button.config(state=tk.DISABLED)
    #  help_button.config(state=tk.DISABLED)  

# Create the main window
root = tk.Tk()
root.title("MARC File to Aleph Sequential converter")

# Create frames
left_frame = tk.Frame(root)
left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
right_frame = tk.Frame(root)
right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

# Create text widgets
left_text = scrolledtext.ScrolledText(left_frame, wrap=tk.WORD)
left_text.pack(fill=tk.BOTH, expand=True)
right_text = scrolledtext.ScrolledText(right_frame, wrap=tk.WORD)
right_text.pack(fill=tk.BOTH, expand=True)

# Create buttons
open_button = tk.Button(root, text="Open File", command=open_file)
open_button.pack(side=tk.TOP, fill=tk.X)
convert_button = tk.Button(root, text="Convert to Aleph SEQ", command=convert_to_aleph_seq, font=("Helvetica", 12, "bold"), state=tk.DISABLED)
convert_button.pack(side=tk.TOP, fill=tk.X)
convert_and_remove_button = tk.Button(root, text="Convert to ALEPH _ SEQ + []", command=convert_to_aleph_seq_and_remove_brackets, font=("Helvetica", 12, "bold"), state=tk.DISABLED)
convert_and_remove_button.pack(side=tk.TOP, fill=tk.X)
save_button = tk.Button(root, text="Save Output As", command=save_output, state=tk.DISABLED)
save_button.pack(side=tk.TOP, fill=tk.X)
remove_button = tk.Button(root, text="Remove []", command=remove_brackets, state=tk.DISABLED)
remove_button.pack(side=tk.TOP, fill=tk.X)
clear_button = tk.Button(root, text="Clear", command=clear_frames, state=tk.DISABLED)
clear_button.pack(side=tk.TOP, fill=tk.X)
help_button = tk.Button(root, text="Help", command=show_help)
help_button.pack(side=tk.TOP, fill=tk.X)
exit_button = tk.Button(root, text="Exit", command=root.quit)
exit_button.pack(side=tk.TOP, fill=tk.X)

# Start the main loop
root.mainloop()
