import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import subprocess
import os
import csv

# --- Direktori & Path ---
BASE_DIR = ""
ARSIP_DIR = os.path.join(BASE_DIR, "..", "data", "arsip")
FILE_SEMENTARA = os.path.join("..", "data", "cache", "data_sementara.csv")
CSV_FIELDNAMES = ["Nama", "Gender", "Usia", "Tinggi Badan", "Berat Badan", "Status", "Keterangan"]

# --- Tema Warna Modern ---
BG_COLOR = '#fff1e6'
FRAME_BG_COLOR = '#ffffff'
FG_COLOR = '#333333'
BUTTON_PRIMARY_BG = '#007bff'
BUTTON_SUCCESS_BG = '#28a745'
BUTTON_DANGER_BG = '#dc3545'
BUTTON_FG_WHITE = '#ffffff'
POPUP_BG_COLOR = '#f8f9fa'
TREEVIEW_HEADER_BG = '#ffd3b0'

# Variabel global untuk menyimpan data angkatan yang aktif
data_angkatan_aktif = []

def ensure_arsip_dir_exists():
    """Memastikan direktori untuk menyimpan file arsip ada."""
    os.makedirs(ARSIP_DIR, exist_ok=True)

def get_list_angkatan():
    """Mendapatkan daftar file angkatan dari direktori arsip."""
    try:
        files = [f.replace('.csv', '') for f in os.listdir(ARSIP_DIR) if f.endswith('.csv')]
        return sorted(files)
    except FileNotFoundError:
        return []

def populate_angkatan_dropdown():
    """Mengisi dropdown dengan daftar angkatan yang tersedia."""
    list_angkatan = get_list_angkatan()
    combo_angkatan['values'] = list_angkatan
    if list_angkatan:
        combo_angkatan.current(0)
        view_selected_angkatan()

def tampilkan_data_di_treeview(data_list):
    """Fungsi terpisah untuk menampilkan list data ke Treeview."""
    for row in tree.get_children():
        tree.delete(row)

    row_number = 1
    for row in data_list:
        tag = 'oddrow' if row_number % 2 != 0 else 'evenrow'
        tree.insert("", "end", values=(
            row_number,
            row.get("Nama", ""), 
            row.get("Gender", ""), 
            row.get("Usia", ""), 
            row.get("Tinggi Badan", ""),
            row.get("Berat Badan", "")
        ), tags=(tag,))
        row_number += 1

def view_selected_angkatan(event=None):
    """Memuat data dari angkatan yang dipilih dan menampilkannya."""
    global data_angkatan_aktif
    data_angkatan_aktif.clear() # Kosongkan data lama

    # Hapus teks di kolom pencarian saat ganti angkatan
    entry_cari.delete(0, tk.END)

    selected_angkatan = combo_angkatan.get()
    if not selected_angkatan:
        tampilkan_data_di_treeview([])
        return

    file_path = os.path.join(ARSIP_DIR, f"{selected_angkatan}.csv")
    
    try:
        with open(file_path, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            data_angkatan_aktif = list(reader) # Muat semua data ke memori
        
        tampilkan_data_di_treeview(data_angkatan_aktif)

    except FileNotFoundError:
        messagebox.showerror("Error", f"File arsip untuk '{selected_angkatan}' tidak ditemukan.", parent=root)
        tampilkan_data_di_treeview([])
    except Exception as e:
        messagebox.showerror("Error", f"Gagal membaca file arsip: {e}", parent=root)
        tampilkan_data_di_treeview([])

# --- FUNGSI PENCARIAN BARU ---
def lakukan_pencarian(event=None):
    """Menyaring data di tabel berdasarkan input dari kolom pencarian."""
    query = entry_cari.get().lower()
    
    if not query:
        # Jika kolom pencarian kosong, tampilkan semua data
        tampilkan_data_di_treeview(data_angkatan_aktif)
        return

    hasil_pencarian = []
    for row in data_angkatan_aktif:
        # Cek apakah query ada di salah satu kolom yang diinginkan
        nama = str(row.get("Nama", "")).lower()
        usia = str(row.get("Usia", "")).lower()
        tinggi = str(row.get("Tinggi Badan", "")).lower()
        berat = str(row.get("Berat Badan", "")).lower()

        if query in nama or query in usia or query in tinggi or query in berat:
            hasil_pencarian.append(row)
    
    tampilkan_data_di_treeview(hasil_pencarian)

def hapus_angkatan_terpilih():
    # ... (Fungsi ini tidak perlu diubah, biarkan seperti semula)
    selected_angkatan = combo_angkatan.get()
    if not selected_angkatan:
        messagebox.showwarning("Peringatan", "Pilih angkatan yang ingin dihapus.", parent=root)
        return
    if not messagebox.askyesno("Konfirmasi Hapus", f"Apakah Anda yakin ingin menghapus arsip untuk angkatan '{selected_angkatan}' secara permanen?"):
        return
    file_path = os.path.join(ARSIP_DIR, f"{selected_angkatan}.csv")
    try:
        os.remove(file_path)
        messagebox.showinfo("Berhasil", f"Arsip untuk '{selected_angkatan}' telah dihapus.", parent=root)
        for row in tree.get_children():
            tree.delete(row)
        combo_angkatan.set('')
        populate_angkatan_dropdown()
    except FileNotFoundError:
        messagebox.showerror("Error", "File arsip tidak ditemukan untuk dihapus (mungkin sudah dihapus sebelumnya).", parent=root)
        populate_angkatan_dropdown()
    except Exception as e:
        messagebox.showerror("Error", f"Gagal menghapus file: {e}", parent=root)

def kembali_ke_beranda():
    # ... (Fungsi ini tidak perlu diubah, biarkan seperti semula)
    root.destroy()
    script_path = os.path.join(BASE_DIR, "beranda.py")
    if os.path.exists(script_path):
        subprocess.run(["python", script_path])
    else:
        messagebox.showerror("Error", f"File tidak ditemukan: {script_path}")


# --- UI Setup ---
root = tk.Tk()
root.title("Arsip Peserta Diterima - Aplikasi Seleksi TNI")
root.attributes("-fullscreen", True)
root.bind("<Escape>", lambda e: root.attributes("-fullscreen", False))
root.configure(bg=BG_COLOR)

try:
    icon_path = os.path.join("..", "assets", "logo.ico")
    root.iconbitmap(icon_path)
except tk.TclError:
    print("Icon 'logo.ico' tidak ditemukan.")

# --- Frame Utama & Kontrol ---
main_frame = tk.Frame(root, bg=BG_COLOR, padx=20, pady=20)
main_frame.pack(expand=True, fill="both")

# Frame Kontrol Atas
control_frame = tk.Frame(main_frame, bg=BG_COLOR, pady=10)
control_frame.pack(fill="x")

tk.Label(control_frame, text="Pilih Angkatan:", font=("Segoe UI", 14), bg=BG_COLOR, fg=FG_COLOR).pack(side="left", padx=(0, 10))
combo_angkatan = ttk.Combobox(control_frame, font=("Segoe UI", 12), width=30, state='readonly')
combo_angkatan.pack(side="left", padx=(0, 20), ipady=4)
combo_angkatan.bind("<<ComboboxSelected>>", view_selected_angkatan)

# --- UI PENCARIAN ---
tk.Label(control_frame, text="Cari:", font=("Segoe UI", 14), bg=BG_COLOR, fg=FG_COLOR).pack(side="left", padx=(0, 10))
entry_cari = tk.Entry(control_frame, font=("Segoe UI", 12), width=40)
entry_cari.pack(side="left", fill="x", expand=True, ipady=4)
entry_cari.bind("<KeyRelease>", lakukan_pencarian) # Pencarian live setiap kali mengetik


# --- Frame Tabel ---
tree_frame = tk.Frame(main_frame)
tree_frame.pack(expand=True, fill="both", pady=10)
style = ttk.Style()
style.map('Treeview', background=[('selected', '#0056b3')], foreground=[('selected', 'white')])
style.configure("Treeview.Heading", font=("Segoe UI", 12, "bold"), background=TREEVIEW_HEADER_BG)
style.configure("Treeview", rowheight=28, font=("Segoe UI", 11))
style.layout("Treeview", [('Treeview.treearea', {'sticky': 'nswe'})]) 
cols = ("No.", "Nama", "Gender", "Usia", "Tinggi Badan", "Berat Badan")
tree = ttk.Treeview(tree_frame, columns=cols, show="headings")
tree.tag_configure('oddrow', background='#E8E8E8')
tree.tag_configure('evenrow', background='#FFFFFF')
tree.heading("No.", text="No.")
tree.column("No.", width=40, minwidth=40, anchor='center')
tree.heading("Nama", text="Nama")
tree.column("Nama", width=250, minwidth=150)
tree.heading("Gender", text="Gender")
tree.column("Gender", width=100, minwidth=100, anchor='center')
tree.heading("Usia", text="Usia")
tree.column("Usia", width=60, minwidth=60, anchor='center')
tree.heading("Tinggi Badan", text="Tinggi Badan (cm)")
tree.column("Tinggi Badan", width=140, minwidth=120, anchor='center')
tree.heading("Berat Badan", text="Berat Badan (kg)")
tree.column("Berat Badan", width=140, minwidth=120, anchor='center')
tree.pack(side="left", expand=True, fill="both")
scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
tree.configure(yscrollcommand=scrollbar.set)
scrollbar.pack(side="right", fill="y")


# --- Frame Tombol Bawah ---
bottom_frame = tk.Frame(main_frame, bg=BG_COLOR, pady=10)
bottom_frame.pack(fill="x")
btn_hapus = tk.Button(bottom_frame, text="Hapus Angkatan Terpilih", font=("Segoe UI", 12, "bold"), bg=BUTTON_DANGER_BG, fg=BUTTON_FG_WHITE, relief="flat", command=hapus_angkatan_terpilih, width=25, pady=8)
btn_hapus.pack(side="left")
btn_kembali = tk.Button(bottom_frame, text="Kembali ke Menu Utama", font=("Segoe UI", 12, "bold"), bg=BUTTON_PRIMARY_BG, fg=BUTTON_FG_WHITE, relief="flat", command=kembali_ke_beranda, width=25, pady=8)
btn_kembali.pack(side="right")


# --- Inisialisasi ---
ensure_arsip_dir_exists()
populate_angkatan_dropdown()
root.mainloop()