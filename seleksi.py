import tkinter as tk
from tkinter import messagebox, PhotoImage, ttk, filedialog, simpledialog
import subprocess
import os
import csv

# --- Tema Warna Modern ---
BG_COLOR = '#fff1e6'
FRAME_BG_COLOR = '#fff1e6' 
LABEL_FRAME_BG = '#fff1e6' 
FG_COLOR = '#333333'
BUTTON_PRIMARY_BG = '#007bff'
BUTTON_SUCCESS_BG = '#28a745'
BUTTON_WARNING_BG = '#ffc107'
BUTTON_DANGER_BG = '#dc3545'
BUTTON_INFO_BG = '#17a2b8'
BUTTON_SECONDARY_BG = '#6c757d'
BUTTON_FG_WHITE = '#ffffff'
BUTTON_FG_DARK = '#212529'
TREEVIEW_HEADER_BG = '#ffd3b0'

# List untuk menyimpan data peserta
data_peserta = []

def hitung_berat_ideal(gender, tinggi):
    """Menghitung berat badan ideal berdasarkan gender dan tinggi badan."""
    if tinggi <= 100:
        return 0
    if gender == "Laki-laki":
        ideal = (tinggi - 100) - ((tinggi - 100) * 0.10)
    elif gender == "Perempuan":
        ideal = (tinggi - 100) - ((tinggi - 100) * 0.15)
    else:
        ideal = 0
    return ideal

def hitung_status_dan_keterangan(data_input):
    """Menghitung status dan keterangan berdasarkan data input (dictionary)."""
    try:
        gender = data_input.get("Gender")
        usia = int(data_input.get("Usia", 0))
        tinggi = int(data_input.get("Tinggi Badan", 0))
        berat = float(data_input.get("Berat Badan", 0.0))

        berat_ideal = hitung_berat_ideal(gender, tinggi)
        lolos_usia = 18 <= usia <= 22
        lolos_tinggi = (gender == "Laki-laki" and tinggi >= 160) or \
                       (gender == "Perempuan" and tinggi >= 157)
        # Toleransi perbandingan float dibuat lebih realistis
        lolos_berat = abs(berat - berat_ideal) <= 2 

        status = "Lolos" if lolos_usia and lolos_tinggi and lolos_berat else "Tidak Lolos"
        
        keterangan = []
        if not lolos_tinggi:
            keterangan.append("Tinggi tidak memenuhi syarat")
        if not lolos_usia:
            if usia < 18: keterangan.append("Usia kurang dari 18 tahun")
            if usia > 22: keterangan.append("Usia lebih dari 22 tahun")
        if not lolos_berat:
            keterangan.append(f"Berat tidak ideal (ideal: {berat_ideal:.1f} kg)")

        keterangan_jadi = " dan ".join(keterangan) if keterangan else "Memenuhi Syarat"

        # Mengembalikan dictionary lengkap dengan status dan keterangan
        return {
            "Nama": data_input.get("Nama"),
            "Gender": gender,
            "Usia": str(usia),
            "Tinggi Badan": str(tinggi),
            "Berat Badan": str(berat),
            "Status": status,
            "Keterangan": keterangan_jadi
        }
    except (ValueError, TypeError):
        # Jika ada data yang tidak valid di CSV (misal: usia bukan angka)
        return {
            "Nama": data_input.get("Nama", "N/A"),
            "Gender": data_input.get("Gender", "N/A"),
            "Usia": data_input.get("Usia", "N/A"),
            "Tinggi Badan": data_input.get("Tinggi Badan", "N/A"),
            "Berat Badan": data_input.get("Berat Badan", "N/A"),
            "Status": "Error",
            "Keterangan": "Data tidak valid"
        }

def simpanData(event=None):
    """Menyimpan data pendaftar baru dan melakukan validasi."""
    nama = entry_nama.get()
    gender = gender_var.get()
    usia = entry_usia.get()
    tinggiBadan = entry_tinggiBadan.get()
    beratBadan = entry_beratBadan.get()

    if not all([nama, gender, usia, tinggiBadan, beratBadan]):
        messagebox.showwarning("Peringatan", "Semua field harus diisi!")
        return

    try:
        usia_int = int(usia)
        tinggiBadan_int = int(tinggiBadan)
        beratBadan_float = float(beratBadan)
    except ValueError:
        messagebox.showerror("Eror", "Usia, Tinggi, dan Berat Badan harus berupa angka!")
        return

    berat_ideal = hitung_berat_ideal(gender, tinggiBadan_int)
    lolos_usia = 18 <= usia_int <= 22
    lolos_tinggi = (gender == "Laki-laki" and tinggiBadan_int >= 160) or \
                   (gender == "Perempuan" and tinggiBadan_int >= 157)
    lolos_berat = abs(beratBadan_float - berat_ideal) < 0.1 # Toleransi kecil untuk perbandingan float

    status = "Lolos" if lolos_usia and lolos_tinggi and lolos_berat else "Tidak Lolos"

    keterangan = []
    if not lolos_tinggi:
        keterangan.append("Tinggi tidak memenuhi syarat")
    if not lolos_usia:
        if usia_int < 18: keterangan.append("Usia kurang dari 18 tahun")
        if usia_int > 22: keterangan.append("Usia lebih dari 22 tahun")
    if not lolos_berat:
        keterangan.append(f"Berat tidak ideal (ideal: {berat_ideal:.2f} kg)")

    keteranganJadi = " dan ".join(keterangan) if keterangan else "Memenuhi Syarat"

    data_peserta.append({
        "Nama": nama, "Gender": gender, "Usia": usia, "Tinggi Badan": tinggiBadan,
        "Berat Badan": beratBadan, "Status": status, "Keterangan": keteranganJadi
    })

    messagebox.showinfo("Berhasil", f"Data untuk '{nama}' berhasil disimpan.")
    
    for entry in [entry_nama, entry_usia, entry_tinggiBadan, entry_beratBadan]:
        entry.delete(0, tk.END)
    gender_var.set("")
    tampilkanData()

def tampilkanData():
    """Menampilkan semua data peserta ke dalam tabel."""
    for row in tabel.get_children():
        tabel.delete(row)
    for data in data_peserta:
        tabel.insert("", tk.END, values=(
            data["Nama"], data["Gender"], data["Usia"], data["Tinggi Badan"],
            data.get("Berat Badan", ""), data["Status"], data["Keterangan"]
        ))

def editData(event=None):
    """Membuka jendela baru untuk mengedit data yang dipilih."""
    if not tabel.selection():
        messagebox.showwarning("Peringatan", "Pilih data yang ingin di edit")
        return
    
    pilih = tabel.selection()[0]
    index = tabel.index(pilih)
    data_lama = data_peserta[index]

    frm_edit = tk.Toplevel(frmutama)
    frm_edit.title("Edit Data")
    frm_edit.configure(bg=BG_COLOR)
    frm_edit.geometry("350x280")
    frm_edit.transient(frmutama) # Agar jendela edit selalu di atas jendela utama
    frm_edit.grab_set() # Fokus hanya pada jendela edit

    fields = ["Nama", "Gender", "Usia", "Tinggi Badan", "Berat Badan"]
    entries = {}
    
    def simpan_edit(event=None):
        try:
            nama_baru = entries["Nama"].get()
            gender_baru = entries["Gender"].get()
            usia_baru = int(entries["Usia"].get())
            tinggi_baru = int(entries["Tinggi Badan"].get())
            berat_baru = float(entries["Berat Badan"].get())

            berat_ideal = hitung_berat_ideal(gender_baru, tinggi_baru)
            lolos_usia = 18 <= usia_baru <= 22
            lolos_tinggi = (gender_baru == "Laki-laki" and tinggi_baru >= 160) or \
                           (gender_baru == "Perempuan" and tinggi_baru >= 157)
            lolos_berat = abs(berat_baru - berat_ideal) < 0.1

            status_baru = "Lolos" if lolos_usia and lolos_tinggi and lolos_berat else "Tidak Lolos"
            keterangan_baru = []
            if not lolos_tinggi: keterangan_baru.append("Tinggi tidak memenuhi syarat")
            if not lolos_usia:
                if usia_baru < 18: keterangan_baru.append("Usia kurang dari 18 tahun")
                if usia_baru > 22: keterangan_baru.append("Usia lebih dari 22 tahun")
            if not lolos_berat: keterangan_baru.append(f"Berat tidak ideal (ideal: {berat_ideal:.2f} kg)")

            data_peserta[index] = {
                "Nama": nama_baru, "Gender": gender_baru, "Usia": str(usia_baru),
                "Tinggi Badan": str(tinggi_baru), "Berat Badan": str(berat_baru),
                "Status": status_baru, "Keterangan": " dan ".join(keterangan_baru) if keterangan_baru else "Memenuhi Syarat"
            }
            tampilkanData()
            frm_edit.destroy()
        except ValueError:
            messagebox.showerror("Error", "Usia, Tinggi, dan Berat harus berupa angka", parent=frm_edit)
        except Exception as e:
            messagebox.showerror("Error", f"Terjadi kesalahan: {e}", parent=frm_edit)

    for i, field in enumerate(fields):
        tk.Label(frm_edit, text=field, font=("Arial", 10), bg=BG_COLOR).grid(row=i, column=0, padx=10, pady=5, sticky='e')
        if field == "Gender":
            gender_var_edit = tk.StringVar(value=data_lama[field])
            entry_widget = ttk.Combobox(frm_edit, textvariable=gender_var_edit, values=["Laki-laki", "Perempuan"], state='readonly')
            entries[field] = gender_var_edit
        else:
            entry_widget = tk.Entry(frm_edit)
            entry_widget.insert(0, data_lama.get(field, ""))
            entries[field] = entry_widget
        entry_widget.grid(row=i, column=1, padx=10, pady=5, sticky='w')
        # Bind tombol Enter ke semua input di form edit
        entry_widget.bind("<Return>", simpan_edit)
        
    tk.Button(frm_edit, text="Simpan Perubahan", font=("Arial", 11, "bold"), bg=BUTTON_SUCCESS_BG, fg=BUTTON_FG_WHITE, relief="flat", command=simpan_edit).grid(row=len(fields), column=0, columnspan=2, pady=15)
    
def hapusData(event=None):
    """Menghapus data yang dipilih dari tabel."""
    if not tabel.selection():
        messagebox.showwarning("Peringatan", "Pilih data yang ingin dihapus")
        return
    pilih = tabel.selection()[0]
    nama_peserta = tabel.item(pilih)['values'][0]
    konfirmasi = messagebox.askyesno("Konfirmasi", f"Yakin ingin menghapus data '{nama_peserta}'?")
    if konfirmasi:
        index = tabel.index(pilih)
        del data_peserta[index]
        tampilkanData()

def hapusSemuaData():
    """Menghapus semua data dari tabel dan list."""
    if not data_peserta:
        messagebox.showinfo("Info", "Tidak ada data untuk dihapus")
        return
    konfirmasi = messagebox.askyesno("Konfirmasi Hapus Semua", "Yakin ingin menghapus SEMUA data? Aksi ini tidak dapat dibatalkan.")
    if konfirmasi:
        data_peserta.clear()
        tampilkanData()

def show_context_menu(event):
    """Menampilkan menu klik kanan pada tabel."""
    # Pilih baris di bawah kursor
    iid = tabel.identify_row(event.y)
    if iid:
        # Pindahkan seleksi ke baris yang diklik kanan
        tabel.selection_set(iid)
        # Tampilkan menu popup
        context_menu.tk_popup(event.x_root, event.y_root)

CSV_FIELDNAMES = ["Nama", "Gender", "Usia", "Tinggi Badan", "Berat Badan", "Status", "Keterangan"]

def export_data():
    """Mengekspor data peserta ke dalam file CSV."""
    if not data_peserta:
        messagebox.showinfo("Info", "Tidak ada data untuk diekspor.")
        return
    file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")], title="Simpan Data ke CSV")
    if not file_path: return
    try:
        with open(file_path, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=CSV_FIELDNAMES)
            writer.writeheader()
            writer.writerows(data_peserta)
        messagebox.showinfo("Export Berhasil", f"Data berhasil diekspor ke\n{file_path}")
    except Exception as e:
        messagebox.showerror("Error", f"Gagal mengekspor data: {e}")

def import_data():
    """Mengimpor data peserta dari file CSV dan MENGHITUNG ULANG status/keterangan."""
    if data_peserta and not messagebox.askyesno("Konfirmasi", "Data yang ada akan dihapus dan diganti dengan data baru. Lanjutkan impor?"):
        return

    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")], title="Import Data dari CSV")
    if not file_path: return
    
    try:
        with open(file_path, mode='r', newline='', encoding='utf-8-sig') as file:
            reader = csv.DictReader(file)
            
            # Kosongkan data lama, siapkan list untuk data baru yang sudah diproses
            data_peserta.clear()
            
            # Loop melalui setiap baris dari CSV, hitung status, lalu tambahkan
            for row_mentah in reader:
                # Proses setiap baris untuk menghitung status dan keterangan
                data_terproses = hitung_status_dan_keterangan(row_mentah)
                data_peserta.append(data_terproses)

        tampilkanData()
        messagebox.showinfo("Import Berhasil", f"Data berhasil diimpor dan diproses dari\n{file_path}")
    except FileNotFoundError:
        messagebox.showerror("Error", "File tidak ditemukan.")
    except Exception as e:
        messagebox.showerror("Error", f"Gagal mengimpor data: {e}")

FILE_SEMENTARA = "cache/data_sementara.csv"

def simpan_sementara():
    """Menyimpan sesi data saat ini ke file sementara."""
    os.makedirs(os.path.dirname(FILE_SEMENTARA), exist_ok=True)
    with open(FILE_SEMENTARA, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=CSV_FIELDNAMES)
        writer.writeheader()
        writer.writerows(data_peserta)

def muat_sementara():
    """Memuat sesi data terakhir dari file sementara saat aplikasi dimulai."""
    if not os.path.exists(FILE_SEMENTARA): return
    try:
        with open(FILE_SEMENTARA, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            data_peserta.clear()
            for row in reader: data_peserta.append(row)
            tampilkanData()
    except Exception as e:
        print(f"Error saat memuat data sementara: {e}")

def beranda():
    """Menyimpan data dan kembali ke menu utama."""
    simpan_sementara()
    frmutama.destroy()
    script_path = os.path.join("beranda.py")
    try:
        subprocess.run(["python", script_path], check=True)
    except FileNotFoundError: messagebox.showerror("Error", f"File tidak ditemukan: {script_path}")
    except Exception as e: messagebox.showerror("Error", f"Gagal menjalankan skrip: {e}")

def on_close():
    """Menyimpan data sebelum menutup aplikasi."""
    simpan_sementara()
    frmutama.destroy()

def arsipkan():
    """Filter peserta lolos dan simpan ke dalam file arsip CSV."""
    # 1. Filter peserta yang statusnya "Lolos"
    peserta_lolos = [p for p in data_peserta if p.get("Status") == "Lolos"]

    # 2. Cek apakah ada peserta yang lolos
    if not peserta_lolos:
        messagebox.showinfo("Info", "Tidak ada peserta yang berstatus 'Lolos' untuk diarsipkan.", parent=frmutama)
        return

    # 3. Minta nama file arsip dari pengguna
    nama_angkatan = simpledialog.askstring("Arsipkan Peserta Lolos", "Masukkan nama untuk angkatan yang akan diarsipkan:", parent=frmutama)
    if not nama_angkatan:
        return # Pengguna membatalkan dialog

    # 4. Siapkan path untuk menyimpan file
    arsip_dir = os.path.join("arsip")
    os.makedirs(arsip_dir, exist_ok=True) # Buat folder jika belum ada
    arsip_file_path = os.path.join(arsip_dir, f"{nama_angkatan}.csv")

    # 5. Konfirmasi jika file arsip sudah ada
    if os.path.exists(arsip_file_path):
        if not messagebox.askyesno("Konfirmasi Timpa", f"File arsip '{nama_angkatan}' sudah ada.\nApakah Anda ingin menimpanya?"):
            return # Pengguna memilih 'No'

    # 6. Tulis data ke file CSV
    try:
        with open(arsip_file_path, mode='w', newline='', encoding='utf-8') as file:
            # Asumsikan CSV_FIELDNAMES adalah variabel global atau sudah terdefinisi
            writer = csv.DictWriter(file, fieldnames=CSV_FIELDNAMES)
            writer.writeheader()
            writer.writerows(peserta_lolos)
        
        # 7. Tampilkan pesan sukses (tanpa menyebutkan reset)
        messagebox.showinfo("Berhasil", 
                            f"{len(peserta_lolos)} peserta lolos telah berhasil diarsipkan ke '{nama_angkatan}'.", 
                            parent=frmutama)

    except Exception as e:
        messagebox.showerror("Error", f"Gagal menyimpan file arsip: {e}", parent=frmutama)

# --- Tampilan Utama ---
frmutama = tk.Tk()
frmutama.attributes("-fullscreen", True)
frmutama.bind("<Escape>", lambda e: frmutama.attributes("-fullscreen", False))
try: frmutama.iconbitmap("static/logo.ico")
except tk.TclError: pass
frmutama.title("Aplikasi Seleksi Calon Prajurit TNI")
frmutama.configure(bg=BG_COLOR)

# --- Bagian Atas: Tombol Navigasi dan Header ---
frame_atas = tk.Frame(frmutama, bg=BG_COLOR)
frame_atas.pack(fill="x", padx=10, pady=(10, 5))

tk.Button(frame_atas, text="☰ Menu Utama", font=("Segoe UI", 11, "bold"), bg=BUTTON_PRIMARY_BG, fg=BUTTON_FG_WHITE, width=14, relief="flat", command=beranda).pack(side="left", anchor="w")
tk.Button(frame_atas, text="❌ Keluar", font=("Segoe UI", 11, "bold"), bg=BUTTON_DANGER_BG, fg=BUTTON_FG_WHITE, width=12, relief="flat", command=on_close).pack(side="right", anchor="e")

frame_judul_container = tk.Frame(frame_atas, bg=BG_COLOR)
frame_judul_container.pack(side="top", fill="x", expand=True)

try:
    header_path = os.path.join("static", "header.gif")
    header = PhotoImage(file=header_path)
    label_header = tk.Label(frame_judul_container, image=header, bg=BG_COLOR)
    label_header.pack()
    label_header.image = header
except tk.TclError:
    label_header = tk.Label(frame_judul_container, text="Seleksi Calon Prajurit TNI", font=("Arial", 24, "bold"), bg=BG_COLOR, fg=FG_COLOR)
    label_header.pack()

# --- Frame untuk Formulir Pendaftaran ---
frame_form = tk.Frame(frmutama, bg=BG_COLOR)
frame_form.pack(padx=10, pady=10, fill="x")

form_kiri = tk.LabelFrame(frame_form, text="Formulir Pendaftaran", font=("Arial", 12, "bold"), bg=LABEL_FRAME_BG, fg=FG_COLOR, padx=10, pady=10, relief="groove")
form_kiri.pack(side="left", fill="x", expand=True)

tk.Label(form_kiri, text="Nama", font=("Arial", 12), bg=LABEL_FRAME_BG, fg=FG_COLOR).grid(row=0, column=0, padx=10, pady=5, sticky='w')
entry_nama = tk.Entry(form_kiri, width=30, font=("Arial", 12))
entry_nama.grid(row=0, column=1, padx=10, pady=5)
tk.Label(form_kiri, text="Gender", font=("Arial", 12), bg=LABEL_FRAME_BG, fg=FG_COLOR).grid(row=1, column=0, padx=10, pady=5, sticky='w')
gender_var = tk.StringVar()
combo_gender = ttk.Combobox(form_kiri, textvariable=gender_var, values=["Laki-laki", "Perempuan"], width=28, font=("Arial", 12), state='readonly')
combo_gender.grid(row=1, column=1, padx=10, pady=5)
tk.Label(form_kiri, text="Usia", font=("Arial", 12), bg=LABEL_FRAME_BG, fg=FG_COLOR).grid(row=2, column=0, padx=10, pady=5, sticky='w')
entry_usia = tk.Entry(form_kiri, width=30, font=("Arial", 12))
entry_usia.grid(row=2, column=1, padx=10, pady=5)
tk.Label(form_kiri, text="Tinggi Badan (cm)", font=("Arial", 12), bg=LABEL_FRAME_BG, fg=FG_COLOR).grid(row=3, column=0, padx=10, pady=5, sticky='w')
entry_tinggiBadan = tk.Entry(form_kiri, width=30, font=("Arial", 12))
entry_tinggiBadan.grid(row=3, column=1, padx=10, pady=5)
tk.Label(form_kiri, text="Berat Badan (kg)", font=("Arial", 12), bg=LABEL_FRAME_BG, fg=FG_COLOR).grid(row=4, column=0, padx=10, pady=5, sticky='w')
entry_beratBadan = tk.Entry(form_kiri, width=30, font=("Arial", 12))
entry_beratBadan.grid(row=4, column=1, padx=10, pady=5)

# Bind tombol Enter ke semua input di form utama
for widget in [entry_nama, entry_usia, entry_tinggiBadan, entry_beratBadan, combo_gender]:
    widget.bind("<Return>", simpanData)

frame_tombol_kanan = tk.Frame(frame_form, bg=BG_COLOR, padx=20)
frame_tombol_kanan.pack(side="left", anchor="n", pady=20)
tk.Button(frame_tombol_kanan, text="Simpan", font=("Arial", 12), bg=BUTTON_INFO_BG, fg=BUTTON_FG_WHITE, width=12, relief="flat", command=simpanData).pack(pady=5)
tk.Button(frame_tombol_kanan, text="Edit", font=("Arial", 12), bg=BUTTON_WARNING_BG, fg=BUTTON_FG_DARK, width=12, relief="flat", command=editData).pack(pady=5)
tk.Button(frame_tombol_kanan, text="Hapus Semua", font=("Arial", 12), bg=BUTTON_DANGER_BG, fg=BUTTON_FG_WHITE, width=12, relief="flat", command=hapusSemuaData).pack(pady=5)

# --- Frame untuk Tabel Data ---
label_data = tk.Label(frmutama, text="Data Pendaftar", font=("Arial", 13, "bold"), bg=BG_COLOR, fg=FG_COLOR)
label_data.pack(pady=(10, 0))
frame_tabel_bawah = tk.Frame(frmutama, bg=BG_COLOR)
frame_tabel_bawah.pack(fill="both", expand=True, padx=10, pady=5)
frame_tabel = tk.Frame(frame_tabel_bawah)
frame_tabel.pack(fill="both", expand=True, side="left")

scrollbar_y = ttk.Scrollbar(frame_tabel, orient="vertical")
scrollbar_y.pack(side="right", fill="y")
style = ttk.Style()
style.theme_use("clam")
style.configure("Treeview.Heading", font=("Segoe UI", 11, "bold"), background=TREEVIEW_HEADER_BG)
style.configure("Treeview", rowheight=25) 

columns = ("Nama", "Gender", "Usia", "Tinggi Badan", "Berat Badan", "Status", "Keterangan")
tabel = ttk.Treeview(frame_tabel, columns=columns, show="headings", height=8, yscrollcommand=scrollbar_y.set)
scrollbar_y.config(command=tabel.yview)

for col in columns:
    tabel.heading(col, text=col)
    tabel.column(col, anchor='center')
tabel.column("Nama", width=180, anchor='center')
tabel.column("Gender", width=100, anchor='center')
tabel.column("Usia", width=50, anchor='center')
tabel.column("Tinggi Badan", width=80, anchor='center')
tabel.column("Berat Badan", width=80, anchor='center')
tabel.column("Status", width=80, anchor='center')
tabel.column("Keterangan", width=300, anchor='w')
tabel.pack(fill="both", expand=True)

# --- Menu Klik Kanan ---
context_menu = tk.Menu(tabel, tearoff=0)
context_menu.add_command(label="✏️ Edit Data", command=editData)
context_menu.add_command(label="🗑️ Hapus Data", command=hapusData)
context_menu.add_separator()
context_menu.add_command(label="Hapus Semua Data", command=hapusSemuaData)

# Bind event klik kanan dan tombol Delete
tabel.bind("<Button-3>", show_context_menu)
tabel.bind("<Delete>", hapusData)

# --- Panel Bawah: Kriteria dan Tombol CSV ---
panel_bawah = tk.Frame(frmutama, bg=BG_COLOR)
panel_bawah.pack(fill="x", padx=10, pady=10)

ketentuan_text = """Kriteria Kelulusan: Usia: 18–22 tahun | Laki-laki: tinggi ≥ 160 cm & berat ideal | Perempuan: tinggi ≥ 157 cm & berat ideal"""
label_ketentuan = tk.Label(panel_bawah, text=ketentuan_text, font=("Arial", 10), justify="left", bg=BG_COLOR, fg="#006400")
label_ketentuan.pack(side="left", anchor="w")

frame_buton_kanan_bawah = tk.Frame(panel_bawah, bg=BG_COLOR)
frame_buton_kanan_bawah.pack(side="right", anchor="e")
tk.Button(frame_buton_kanan_bawah, text="Import CSV", font=("Arial", 12), bg=BUTTON_SECONDARY_BG, fg=BUTTON_FG_WHITE, width=12, relief="flat", command=import_data).pack(side="left", padx=5)
tk.Button(frame_buton_kanan_bawah, text="Export CSV", font=("Arial", 12), bg=BUTTON_SUCCESS_BG, fg=BUTTON_FG_WHITE, width=12, relief="flat", command=export_data).pack(side="left", padx=5)

tk.Button(frame_buton_kanan_bawah, text="Arsipkan peserta Lolos", font=("Arial", 12, "bold"), bg=BUTTON_PRIMARY_BG, fg=BUTTON_FG_WHITE, width=20, relief="flat", command=arsipkan).pack(side="left", padx=5)

muat_sementara()
frmutama.protocol("WM_DELETE_WINDOW", on_close)
frmutama.mainloop()
