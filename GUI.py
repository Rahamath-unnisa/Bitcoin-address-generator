import tkinter as tk
from tkinter import messagebox
import requests
from bitAddress import address_generator
from PIL import Image, ImageTk

# 📋 Function to copy text to clipboard and show confirmation message
def copy_to_clipboard(text):
    root.clipboard_clear()
    root.clipboard_append(text)
    root.update()
    messagebox.showinfo("Copied", "Copied to clipboard!")

# 🔐 Function to generate or fetch Bitcoin address
def generate():
    name = entry_name.get().strip().lower()
    password = entry_password.get().strip()

    if not name or not password:
        messagebox.showwarning("Input Required", "Please enter both username and password.")
        return

    try:
        # 🔎 Check if user already exists
        response = requests.get(f"http://127.0.0.1:8000/get_keys/{name}")

        if response.status_code == 200:
            # User exists — ask for password verification
            verify_response = requests.post("http://127.0.0.1:8000/verify_user/", json={
                "username": name,
                "password": password
            })

            if verify_response.status_code == 200:
                # Password is correct — display stored keys
                keys = verify_response.json()
                lbl_private_val.config(text=keys["private_key"])
                lbl_public_val.config(text=keys["public_key"])
                lbl_address_val.config(text=keys["address"])
                messagebox.showinfo("Success", "Logged in and showing your saved keys.")
            else:
                messagebox.showerror("Error", "Username exists but password is incorrect. Cannot show keys.")
            return

        elif response.status_code == 404:
            # User not found — generate and store new keys
            keys = address_generator(name)

            save_response = requests.post(
                "http://127.0.0.1:8000/store_keys/",
                json={
                    "username": name,
                    "password": password,
                    "private_key": keys["private_key"],
                    "public_key": keys["public_key"],
                    "address": keys["address"]
                }
            )

            if save_response.status_code == 200:
                messagebox.showinfo("Success", "New keys generated and saved.")
                lbl_private_val.config(text=keys["private_key"])
                lbl_public_val.config(text=keys["public_key"])
                lbl_address_val.config(text=keys["address"])
            else:
                messagebox.showerror("Error", f"Error saving keys: {save_response.text}")

        else:
            messagebox.showerror("Error", f"Unexpected error: {response.status_code}")

    except Exception as e:
        messagebox.showerror("Error", f"Request failed: {e}")

# 🖼️ GUI Setup
root = tk.Tk()
root.title("Bitcoin Address Generator")
root.geometry("800x600")
root.resizable(False, False)

# 🖼️ Set Background Image
bg_image = Image.open("assets\\bgimg.jpg")
bg_image = bg_image.resize((800, 600))
bg_photo = ImageTk.PhotoImage(bg_image)
bg_label = tk.Label(root, image=bg_photo)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

# 🧾 App Title
tk.Label(root, text="Bitcoin Address Generator", font=("Arial", 20, "bold"), fg="orange", bg="#ffffff").pack(pady=(10, 0))

# 🔆 App Logo
image = Image.open("assets\\bitcoin_logo").convert("RGBA")
background = Image.new("RGB", image.size, (255, 255, 255))
background.paste(image, mask=image.split()[3])
logo_photo = ImageTk.PhotoImage(background.resize((100, 100)))
tk.Label(root, image=logo_photo, bg="#ffffff").pack(pady=(10, 0))

# ✏️ Username Input
tk.Label(root, text="Enter Username:", font=("Arial", 12, "bold"), bg="#ffffff").pack(pady=(10, 0))
entry_name = tk.Entry(root, font=("Arial", 12), width=30)
entry_name.pack(pady=5)

# 🔐 Password Input
tk.Label(root, text="Enter Password:", font=("Arial", 12, "bold"), bg="#ffffff").pack(pady=(10, 0))
entry_password = tk.Entry(root, font=("Arial", 12), width=30, show="*")
entry_password.pack(pady=5)

# ✅ Generate Button
tk.Button(root, text="Generate Address", command=generate,
          font=("Arial", 12, "bold"), bg="orange", fg="black").pack(pady=10)

# 📦 Output Frame
output_frame = tk.Frame(root, width=700, height=250)
output_frame.pack(pady=10)
output_frame.pack_propagate(False)

# 🖼️ Output Frame Background
output_bg_image = Image.open("assets\\bgimg.jpg")
output_bg_image = output_bg_image.resize((700, 250))
output_bg_photo = ImageTk.PhotoImage(output_bg_image)
output_bg_label = tk.Label(output_frame, image=output_bg_photo)
output_bg_label.place(x=0, y=0, relwidth=1, relheight=1)

wrap_len = 680  # Text wrap length for output

# 🔁 Helper function to create output rows (Private Key, Public Key, Address)
def create_output_row(label_text):
    frame = tk.Frame(output_frame)
    frame.pack(anchor="w", padx=10, pady=(5, 0), fill="x")

    tk.Label(frame, text=label_text, font=("Arial", 10, "bold"), anchor="w").pack(side="left")

    label = tk.Label(frame, text="", wraplength=wrap_len, justify="left", font=("Courier", 10))
    label.pack(side="left", padx=(5, 10), expand=True, fill="x")

    def make_copy():
        copy_to_clipboard(label.cget("text"))

    tk.Button(frame, text="Copy", font=("Arial", 8), command=make_copy, bg="orange", fg="black").pack(side="right")

    return label

# Output Labels
lbl_private_val = create_output_row("Private Key:")
lbl_public_val = create_output_row("Public Key:")
lbl_address_val = create_output_row("Address:")

# 🧹 Clear Fields Function
def clear_fields():
    entry_name.delete(0, tk.END)
    entry_password.delete(0, tk.END)
    lbl_private_val.config(text="")
    lbl_public_val.config(text="")
    lbl_address_val.config(text="")

# 🆗 OK / Clear Button
btn_clear = tk.Button(root, text="Thanks", command=clear_fields,
                      font=("Arial", 12, "bold"), bg="orange", fg="white")
btn_clear.pack(pady=10)
btn_clear.lift()  # Bring it to front of all widgets

# 🧵 Run the GUI loop
root.mainloop()
