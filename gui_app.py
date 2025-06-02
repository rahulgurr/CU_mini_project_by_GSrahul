import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import subprocess
import threading
import os
import sys

# Set paths
OUTPUT_FOLDER = "output_plates"
OUTPUT_TEXT = "output_texts/output.txt"

# Global process for live detection
live_process = None

# Ensure output folder exists
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

#resource path 




# Initialize GUI
app = tk.Tk()
app.title("Automated Vehicle Number Plate Recognition System")
app.geometry("1000x700")
#university details
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

 
app.configure(bg="#f0f0f0")
app.resizable(False, False)
info_label = tk.Label(
    app,
    text="Developed by Gurrapu Sai Rahul | UID: O24MSD160167 | Chandigarh University",
    font=("Arial", 12, "italic"),
    fg="gray"
)
info_label.pack(pady=(5, 0))

# UI Elements
img_label = tk.Label(app)
img_label.pack(pady=10)

text_label = tk.Label(app, text="Detected Plate: ", font=("Arial", 16))
text_label.pack(pady=10)

status_label = tk.Label(app, text="", font=("Arial", 14), fg="green")
status_label.pack(pady=10)

# Display latest output image and text
def display_output():
    if os.path.exists(OUTPUT_TEXT):
        with open(OUTPUT_TEXT, "r", encoding="utf-8") as f:
            plate = f.read().strip()
            text_label.config(text=f"Detected Plate: {plate}")
    else:
        text_label.config(text="Detected Plate: Completed")

    # Instead of showing image, just show a popup
    messagebox.showinfo("Process Completed", "Number plate detection completed.\nCheck 'output_plates' folder.")

# Static detection from folder
def run_static_detection():
    folder_path = filedialog.askdirectory(title="Select Folder of Images")
    if not folder_path:
        return

    def static_thread():
        try:
            status_label.config(text="🔍 Detecting plates...", fg="blue")
            subprocess.run(["python", "main.py", folder_path], check=True)
            status_label.config(text="✅ Detection Completed!", fg="green")
            display_output()
            os.startfile(OUTPUT_FOLDER)
        except subprocess.CalledProcessError:
            status_label.config(text="❌ Detection Failed", fg="red")
            messagebox.showerror("Error", "Static detection failed.")

    threading.Thread(target=static_thread).start()

# Open output folder
def open_output_folder():
    if os.path.exists(OUTPUT_FOLDER):
        os.startfile(OUTPUT_FOLDER)
    else:
        messagebox.showerror("Error", "Output folder not found.")

# Start Live Detection (YOLO)
def run_live_detection():
    global live_process

    def live_thread():
        global live_process
        try:
            status_label.config(text="🎥 YOLO Live Detection Running...", fg="blue")
            live_process = subprocess.Popen(["python", "yolo_live2.py"])
            live_process.wait()
            status_label.config(text="✅ Live Detection Completed", fg="green")
        except Exception as e:
            status_label.config(text="❌ Live Detection Failed", fg="red")
            messagebox.showerror("Error", str(e))

    threading.Thread(target=live_thread).start()

# Stop Live Detection
def stop_live_detection():
    global live_process
    if live_process and live_process.poll() is None:
        try:
            live_process.terminate()
            status_label.config(text="🛑 Live Detection Stopped", fg="orange")
        except Exception as e:
            messagebox.showerror("Error", f"Could not stop live detection:\n{e}")
    else:
        status_label.config(text="ℹ️ No live detection running", fg="gray")

# Buttons
tk.Button(app, text="📁 Detect Plates from Folder", font=("Arial", 14), command=run_static_detection).pack(pady=10)
tk.Button(app, text="🎥 Start Live Detection (YOLO)", font=("Arial", 14), command=run_live_detection).pack(pady=5)
tk.Button(app, text="🛑 Stop Live Detection", font=("Arial", 14), command=stop_live_detection).pack(pady=5)
tk.Button(app, text="📂 Open Output Folder", font=("Arial", 14), command=open_output_folder).pack(pady=10)

# Launch the app
app.mainloop()
