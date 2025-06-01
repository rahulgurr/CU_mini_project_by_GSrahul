import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import subprocess
import os

# Set paths for outputs
OUTPUT_IMAGE_PATH = "output_plates/output.jpg"
OUTPUT_TEXT_PATH = "output_texts/output.txt"

# Initialize GUI
app = tk.Tk()
app.title("Automated Vehicle Plate Recognition System")
app.geometry("1000x700")

# UI Elements
img_label = tk.Label(app)
img_label.pack(pady=10)

text_label = tk.Label(app, text="Detected Plate: ", font=("Arial", 16))
text_label.pack(pady=10)

# Helper: Show output image
def display_output():
    if os.path.exists(OUTPUT_IMAGE_PATH):
        img = Image.open(OUTPUT_IMAGE_PATH)
        img = img.resize((800, 500))
        img_tk = ImageTk.PhotoImage(img)
        img_label.config(image=img_tk)
        img_label.image = img_tk
    else:
        messagebox.showerror("Error", "Output image not found.")

    if os.path.exists(OUTPUT_TEXT_PATH):
        with open(OUTPUT_TEXT_PATH, "r", encoding="utf-8") as f:
            text = f.read().strip()
            text_label.config(text=f"Detected Plate: {text}")
    else:
        text_label.config(text="Detected Plate: [Not Found]")

# Static Detection Button
def run_static_detection():
    file_path = filedialog.askopenfilename(title="Select Image", filetypes=[("Images", "*.jpg *.png *.jpeg")])
    if not file_path:
        return

    try:
        subprocess.run(["python", "main.py", file_path], check=True)
        display_output()
    except subprocess.CalledProcessError:
        messagebox.showerror("Error", "Failed to run static detection.")

# Live Detection Button
def run_live_detection():
    try:
        subprocess.run(["python", "yololive.py"], check=True)
        display_output()
    except subprocess.CalledProcessError:
        messagebox.showerror("Error", "Failed to start live detection.")

# Buttons
tk.Button(app, text="📁 Static Image Detection (Haar Cascade)", font=("Arial", 14), command=run_static_detection).pack(pady=10)
tk.Button(app, text="🎥 Live Detection (YOLO)", font=("Arial", 14), command=run_live_detection).pack(pady=10)

# Run the App
app.mainloop()
