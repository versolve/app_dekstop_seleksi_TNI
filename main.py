import subprocess
import os
import sys

def run_app():
    # Menentukan path
    src_path = os.path.join(os.path.dirname(__file__), 'src')

    if not os.path.isdir(src_path):
        print(f"Error: Folder 'src' tidak ditemukan di '{os.path.dirname(__file__)}'.")
        print("Pastikan main.py berada di direktori root proyek Anda, sejajar dengan folder 'src'.")
        sys.exit(1)

    # Script pertama
    initial_script = 'login.py'
    script_path = os.path.join(src_path, initial_script)

    if not os.path.exists(script_path):
        print(f"Error: File '{initial_script}' tidak ditemukan di dalam folder 'src'.")
        sys.exit(1)

    print(f"Memulai aplikasi dari '{initial_script}'...")
    
    try:
        subprocess.run([sys.executable, initial_script], check=True, cwd=src_path)

    except subprocess.CalledProcessError as e:
        print(f"Aplikasi berhenti dengan error: {e}")
    except FileNotFoundError:
        print(f"Error: Perintah 'python' tidak ditemukan. Pastikan Python terinstall dan ada di PATH sistem Anda.")
    except Exception as e:
        print(f"Terjadi kesalahan yang tidak terduga: {e}")

    print("Aplikasi telah ditutup.")

if __name__ == "__main__":
    run_app()