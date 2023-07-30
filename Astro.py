import tkinter as tk
from tkinter import ttk
import requests
from PIL import Image, ImageTk
from datetime import date

# APOD API URL
APOD_API_URL = "https://api.nasa.gov/planetary/apod"

def fetch_apod_data(api_key, date):
    params = {
        "api_key": api_key,
        "date": date,
    }
    response = requests.get(APOD_API_URL, params=params)
    data = response.json()
    return data

def show_apod_image():
    api_key = api_key_entry.get()
    selected_date = date_picker.get()
    data = fetch_apod_data(api_key, selected_date)

    if "url" in data:
        image_url = data["url"]
        image_response = requests.get(image_url, stream=True)
        image_response.raise_for_status()

        with open("apod_image.jpg", "wb") as f:
            for chunk in image_response.iter_content(chunk_size=8192):
                f.write(chunk)

        image = Image.open("apod_image.jpg")
        image.thumbnail((400, 400))
        photo = ImageTk.PhotoImage(image)
        image_label.config(image=photo)
        image_label.photo = photo

        title_label.config(text=data["title"])
        explanation_text.config(state=tk.NORMAL)
        explanation_text.delete("1.0", tk.END)
        explanation_text.insert(tk.END, data["explanation"])
        explanation_text.config(state=tk.DISABLED)

        login_window.withdraw()  # Hide the login window after proceeding to next page
        app.deiconify()  # Show the main APOD Viewer window
    else:
        error_label.config(text="Error: APOD not available for the selected date.")

def on_closing():
    app.destroy()

# Create the main application window
app = tk.Tk()
app.title("APOD Viewer")
app.geometry("600x600")
app.protocol("WM_DELETE_WINDOW", on_closing)

# Create a login window
login_window = tk.Toplevel(app)
login_window.title("Login")
login_window.geometry("300x150")

# Set background image for the login window
background_image = Image.open(r"E:\NK programs\Python\python save\Astro\login.png")
background_photo = ImageTk.PhotoImage(background_image)
background_label = tk.Label(login_window, image=background_photo)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

api_key_label = ttk.Label(login_window, text="Enter NASA API Key:")
api_key_label.pack(pady=5)
api_key_entry = ttk.Entry(login_window, show="*")
api_key_entry.pack(pady=5)

date_label = ttk.Label(login_window, text="Enter Date (YYYY-MM-DD):")
date_label.pack(pady=5)
date_picker = ttk.Entry(login_window)
date_picker.pack(pady=5)

login_button = ttk.Button(login_window, text="Login", command=show_apod_image)
login_button.pack(pady=10)

error_label = ttk.Label(login_window, foreground="red")
error_label.pack(pady=5)

# Image Display
image_label = ttk.Label(app)
image_label.pack(pady=10)

# Title Display
title_label = ttk.Label(app, font=("Helvetica", 16, "bold"))
title_label.pack(pady=5)

# Explanation Display
explanation_text = tk.Text(app, wrap=tk.WORD, font=("Helvetica", 12))
explanation_text.pack(pady=10)
explanation_text.config(state=tk.DISABLED)

# Hide the main APOD Viewer window initially
app.withdraw()

app.mainloop()
