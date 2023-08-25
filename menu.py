import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import webbrowser
import os
import subprocess

import pandas as pd
from sklearn.preprocessing import MinMaxScaler

def main():
    global app
    app = tk.Tk()
    app.title("Visual Knowledge Discovery Tools")

    global data_dict
    global info_label
    data_dict = {}
    
    # Center the window on the screen
    window_width = 450
    window_height = 400
    screen_width = app.winfo_screenwidth()
    screen_height = app.winfo_screenheight()
    x_coordinate = int((screen_width/2) - (window_width/2))
    y_coordinate = int((screen_height/2) - (window_height/2))
    app.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")

    # Styling
    style = ttk.Style()
    style.configure('TButton', background='#3498db', foreground='black', borderwidth=0, font=('Arial', 12))
    style.map('TButton', background=[('active', '#2980b9')], foreground=[('active', 'black')])
    style.configure('TLabel', font=('Arial', 14, 'bold'), foreground='black')

    # Display program collection's name
    program_label = ttk.Label(app, text="Visual Knowledge Discovery Tools")
    program_label.pack(pady=20)

    # Buttons
    load_csv_button = ttk.Button(app, text="Load and Process CSV", command=load_and_process_csv)
    load_csv_button.pack(pady=5, fill='x', padx=50)

    circular_button = ttk.Button(app, text="Run Circular Plotter", command=launch_circular_plotter)
    circular_button.pack(pady=5, fill='x', padx=50)

    envelope_button = ttk.Button(app, text="Run Envelope Plotter", command=launch_envelope_plotter)
    envelope_button.pack(pady=5, fill='x', padx=50)

    plotly_demo_button = ttk.Button(app, text="Run Plotly Demo", command=launch_plotly_demo)
    plotly_demo_button.pack(pady=5, fill='x', padx=50)

    github_button = ttk.Button(app, text="Visit GitHub Page", command=launch_github)
    github_button.pack(pady=5, fill='x', padx=50)

    info_label = ttk.Label(app, text="", font=("Arial", 11))
    info_label.pack(pady=10)

    app.mainloop()

# Function to open file picker and load CSV dataset
def load_and_process_csv():
    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if not file_path:
        return

    # Load the dataset into a Pandas DataFrame
    df = pd.read_csv(file_path)
    df_copy = df.copy()
    # Extract the 'class' column and the features into separate DataFrames
    labels = df.pop('class')
    features = df

    # Normalize the features DataFrame
    scaler = MinMaxScaler()
    features_normalized = pd.DataFrame(scaler.fit_transform(features), columns=features.columns)

    # Save the data in a named dictionary
    dataset_name = os.path.basename(file_path).split(".")[0]
    # Save the data in a named dictionary
    global data_dict
    data_dict = {
        "dataset_name": dataset_name,
        "file_path": file_path,
        "original_dataframe": df_copy,
        "features": features,
        "labels": labels,
        "features_normalized": features_normalized
    }
    display_dataset_info()

def display_dataset_info():
    global data_dict, info_label
    dataset_name = data_dict.get("dataset_name", "N/A")
    file_path = data_dict.get("file_path", "N/A")
    label_names = data_dict.get("labels", [])
    
    unique_label_names = ", ".join(set(label_names))
    num_unique_labels = len(set(label_names))

    
    info_text = f"CSV Name: {dataset_name}\nPath: {file_path}\nClass Count: {num_unique_labels}\nClass Names: {unique_label_names}"
    
    info_label.config(text=info_text)

def launch_circular_plotter():
    app.withdraw()  # Hide the main menu
    subprocess.run(["python", "circular_plotter.py"])
    app.deiconify()  # Show the main menu again

def launch_envelope_plotter():
    app.withdraw()  # Hide the main menu
    subprocess.run(["python", "envelope_plotter.py"])
    app.deiconify()  # Show the main menu again

def launch_plotly_demo():
    app.withdraw()  # Hide the main menu
    subprocess.run(["python", "plotly_demo.py"])
    app.deiconify()  # Show the main menu again

def launch_github():
    webbrowser.open("https://github.com/CWU-VKD-LAB")

def get_dataset_count_and_location():
    datasets_directory = "datasets"
    if os.path.exists(datasets_directory):
        dataset_count = len(os.listdir(datasets_directory))
        dataset_path = os.path.abspath(datasets_directory)
        return dataset_count, dataset_path
    return 0, "Not Found"

if __name__ == "__main__":
    main()
