import tkinter as tk
from tkinter import messagebox
import subprocess
import os

# --- Tema Warna ---
BG_COLOR = '#fff1e6'
FG_COLOR = '#333333'
ENTRY_BG_COLOR = '#fdfdfd'
BUTTON_BG_COLOR = '#007bff'
BUTTON_FG_COLOR = '#ffffff'

# Data Panitia
users = [
    {"username": "admin", "password": "admin123"},
]

def check_login():
    username = entry_username.get()
    password = entry_password.get()

    for user in users:
        if user["username"] == username and user["password"] == password:
            messagebox.showinfo("Login Berhasil", f"Selamat datang, {username}!")
            root.destroy()

            script_path = os.path.join("beranda.py")

            if os.path.exists(script_path):
                subprocess.run(["python", script_path])
            else:
                messagebox.showerror("Error", f"File tidak ditemukan: {script_path}")
            return

    messagebox.showerror("Login Gagal", "Username atau Password salah.")
    
def confirm_exit():
    if messagebox.askyesno("Konfirmasi", "Apakah Anda yakin ingin keluar?"):
        root.destroy()

# --- Pengaturan UI ---
# Mengatur jendela utama
root = tk.Tk()
root.title("Login Aplikasi Seleksi")
root.attributes("-fullscreen", True)
root.bind("<Escape>", lambda e: root.attributes("-fullscreen", False))
root.configure(bg=BG_COLOR)

try:
    # Menentukan path ke ikon
    icon_path = os.path.join("..", "assets", "logo.ico")
    root.iconbitmap(icon_path)
except tk.TclError:
    print("Icon 'logo.ico' tidak ditemukan.")
    pass

# --- UI ---
header_spacer = tk.Frame(root, bg=BG_COLOR)
header_spacer.pack(side="top", fill="both", expand=True)

main_frame = tk.Frame(root, bg=BG_COLOR, padx=60, pady=50)
main_frame.pack(side="top")

footer_spacer = tk.Frame(root, bg=BG_COLOR)
footer_spacer.pack(side="bottom", fill="both", expand=True)

# Label Judul
tk.Label(
    main_frame,
    text="Selamat Datang",
    font=("Segoe UI", 24, "bold"),
    bg=BG_COLOR, 
    fg=FG_COLOR
).pack(pady=(0, 10))

tk.Label(
    main_frame,
    text="Silakan login untuk melanjutkan",
    font=("Segoe UI", 12),
    bg=BG_COLOR, 
    fg=FG_COLOR
).pack(pady=(0, 30))

# Field Username
tk.Label(
    main_frame,
    text="Username",
    font=("Segoe UI", 12),
    bg=BG_COLOR, 
    fg=FG_COLOR
).pack(anchor='w')

entry_username = tk.Entry(
    main_frame,
    font=("Segoe UI", 12),
    width=35, 
    bg=ENTRY_BG_COLOR,
    bd=1,
    relief="solid"
)
entry_username.pack(pady=(5, 15), ipady=4)
entry_username.focus_set() 

# Field Password
tk.Label(
    main_frame,
    text="Password",
    font=("Segoe UI", 12),
    bg=BG_COLOR, 
    fg=FG_COLOR
).pack(anchor='w')

entry_password = tk.Entry(
    main_frame,
    font=("Segoe UI", 12),
    width=35,
    show="*",
    bg=ENTRY_BG_COLOR,
    bd=1,
    relief="solid"
)
entry_password.pack(pady=(5, 25), ipady=4)

# Tombol Login
login_button = tk.Button(
    main_frame,
    text="Login",
    font=("Segoe UI", 12, "bold"),
    bg=BUTTON_BG_COLOR,
    fg=BUTTON_FG_COLOR,
    command=check_login,
    width=15,
    pady=8,
    relief="flat"
)
login_button.pack()

btn_keluar = tk.Button(
    root,
    text="❌ KELUAR",
    font=("Segoe UI", 12, "bold"),
    bg=BG_COLOR,
    fg="#ff4444",
    relief="flat",
    command=confirm_exit,
    width=10,
    height=1
)
btn_keluar.place(relx=0.95, rely=0.05, anchor="ne")

root.bind("<Return>", lambda event: check_login())

root.mainloop()
