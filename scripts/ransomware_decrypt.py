import os
from cryptography.fernet import Fernet

# ─────────────────────────────────────────────
# CONFIGURACION
# ─────────────────────────────────────────────
TARGET_FOLDER = r"C:\SimLab\Documentos"
KEY_FILE      = r"C:\SimLab\decrypt_key.key"
EXT_LOCKED    = ".locked"
RANSOM_NOTE   = "README_RECOVER.txt"

def main():
    print("[*] Ransomware Decryptor - Fase de recuperacion del incidente")

    if not os.path.exists(KEY_FILE):
        print(f"[!] No se encontro la clave en {KEY_FILE}. Imposible descifrar.")
        return

    with open(KEY_FILE, "rb") as kf:
        key = kf.read()
    fernet = Fernet(key)
    print(f"[+] Clave cargada desde: {KEY_FILE}")

    files_restored = 0

    for root, dirs, files in os.walk(TARGET_FOLDER):
        for filename in files:
            if filename == RANSOM_NOTE:
                os.remove(os.path.join(root, filename))
                print(f"  [NOTA ELIMINADA] {os.path.join(root, filename)}")
                continue

            if not filename.endswith(EXT_LOCKED):
                continue

            locked_path   = os.path.join(root, filename)
            original_path = locked_path[:-len(EXT_LOCKED)]

            try:
                with open(locked_path, "rb") as f:
                    encrypted_data = f.read()
                decrypted_data = fernet.decrypt(encrypted_data)
                with open(original_path, "wb") as f:
                    f.write(decrypted_data)
                os.remove(locked_path)
                files_restored += 1
                print(f"  [RESTAURADO] {os.path.basename(locked_path)}  -->  {os.path.basename(original_path)}")
            except Exception as e:
                print(f"  [ERROR] {locked_path}: {e}")

    print(f"\n[+] Recuperacion completa. Archivos restaurados: {files_restored}")

if __name__ == "__main__":
    main()
