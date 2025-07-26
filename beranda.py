import tkinter as tk
from tkinter import ttk, messagebox, PhotoImage
import subprocess
import os
import csv

# --- Tema Warna Modern ---
BG_COLOR = '#fff1e6'
FRAME_BG_COLOR = '#ffffff'
FG_COLOR = '#333333'
BUTTON_BG_1 = '#007bff'
BUTTON_BG_2 = '#28a745'
BUTTON_FG = '#ffffff'
POPUP_BG_COLOR = '#f8f9fa'
HEADING_BG_COLOR = '#e9ecef'
# --- Akhir Tema Warna ---


def open_seleksi_app():
    """Menutup menu utama dan membuka aplikasi seleksi."""
    root.destroy()
    script_path = os.path.join("seleksi.py")
    if os.path.exists(script_path):
        subprocess.run(["python", script_path])
    else:
        messagebox.showerror("Error", f"File tidak ditemukan: {script_path}")

def open_arsip_app():
    """Menutup menu utama dan membuka aplikasi arsip."""
    root.destroy()
    script_path = os.path.join("arsip.py")
    if os.path.exists(script_path):
        subprocess.run(["python", script_path])
    else:
        messagebox.showerror("Error", f"File tidak ditemukan: {script_path}")

def confirm_exit():
    if messagebox.askyesno("Konfirmasi", "Apakah Anda yakin ingin keluar?"):
        root.destroy()

# --- UI Setup untuk Jendela Beranda ---
root = tk.Tk()
root.title("Menu Utama - Aplikasi Seleksi TNI")
root.attributes("-fullscreen", True)
root.bind("<Escape>", lambda e: root.attributes("-fullscreen", False))
root.configure(bg=BG_COLOR)

try:
    icon_path = os.path.join("static/logo.ico")
    root.iconbitmap(icon_path)
except tk.TclError:
    print("Icon 'logo.ico' tidak ditemukan.")
    pass

# --- Tata Letak Terpusat ---
header_spacer = tk.Frame(root, bg=BG_COLOR)
header_spacer.pack(side="top", fill="both", expand=True)

main_frame = tk.Frame(root, bg=BG_COLOR, padx=80, pady=60)
main_frame.pack(side="top")

footer_spacer = tk.Frame(root, bg=BG_COLOR)
footer_spacer.pack(side="bottom", fill="both", expand=True)

# --- Widget ---
try:
    logo_path = os.path.join("static", "logo.gif")
    logo = PhotoImage(file=logo_path)
    label_logo = tk.Label(main_frame, image=logo, bg=BG_COLOR)
    label_logo.pack()
    label_logo.image = logo
except tk.TclError:
    label_logo = tk.Label(main_frame, text="logo TNI", font=("Arial", 24, "bold"), bg=BG_COLOR, fg=FG_COLOR)
    label_logo.pack()
tk.Label(
    main_frame,
    text="APLIKASI SELEKSI PRAJURIT BARU TNI",
    font=("Segoe UI", 32, "bold"),
    bg=BG_COLOR,
    fg="#FFD700"
).pack(pady=(0, 10))

tk.Label(
    main_frame,
    text="Tentara Nasional Indonesia",
    font=("Segoe UI", 26, "bold"),
    bg=BG_COLOR,
    fg=FG_COLOR
).pack(pady=(0, 20))

btn_seleksi = tk.Button(
    main_frame,
    text="Mulai Seleksi Peserta",
    font=("Segoe UI", 14, "bold"),
    bg=BUTTON_BG_1,
    fg=BUTTON_FG,
    width=25,
    pady=15,
    relief="flat",
    command=open_seleksi_app
)
btn_seleksi.pack(pady=10)

btn_arsip = tk.Button(
    main_frame,
    text="Arsip Peserta Diterima",
    font=("Segoe UI", 14, "bold"),
    bg='#17a2b8',  # Anda bisa definisikan sebagai BUTTON_BG_3
    fg=BUTTON_FG,
    width=25,
    pady=15,
    relief="flat",
    command=open_arsip_app
)
btn_arsip.pack(pady=10)

btn_keluar = tk.Button(
    root,
    text="❌ KELUAR",
    font=("Segoe UI", 12, "bold"),
    bg=BG_COLOR,  # Background transparan menggunakan warna yang sama dengan root
    fg="#ff4444",
    relief="flat",
    command=confirm_exit,
    width=10,
    height=1
)
btn_keluar.place(relx=0.95, rely=0.05, anchor="ne")



root.mainloop()
