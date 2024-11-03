import subprocess
import platform
import os
import time
from colorama import init, Fore

# Inicializa colorama
init()

def ping_ip(ip_address):
    param = '-n' if platform.system().lower() == 'windows' else '-c'
    command = ['ping', param, '1', ip_address]

    try:
        output = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return output.returncode == 0  # True si está activa, False si está muerta
    except Exception as e:
        print(f"Error al intentar hacer ping a {ip_address}: {e}")
        return False

def list_txt_files(directory):
    """Lista todos los archivos .txt en el directorio dado."""
    return [f for f in os.listdir(directory) if f.endswith('.txt')]

def select_file(directory):
    """Permite al usuario seleccionar un archivo .txt del directorio."""
    txt_files = list_txt_files(directory)
    
    if not txt_files:
        print("No hay archivos .txt en la misma carpeta que el script.")
        return None

    print("Archivos de texto disponibles:")
    for i, file in enumerate(txt_files):
        print(f"{i + 1}: {file}")

    while True:
        try:
            choice = int(input("Selecciona el número del archivo que deseas procesar: ")) - 1
            if 0 <= choice < len(txt_files):
                return os.path.join(directory, txt_files[choice])
            else:
                print("Selección no válida. Intenta de nuevo.")
        except ValueError:
            print("Por favor, introduce un número válido.")

def process_ips(file_path):
    """Lee el archivo y hace ping a cada IP en la lista."""
    try:
        with open(file_path, 'r') as file:
            ip_list = file.readlines()
            ip_list = [ip.strip() for ip in ip_list]  # Eliminar espacios en blanco y saltos de línea
            
            for ip in ip_list:
                print(f"Probando {ip}...", end="", flush=True)
                if ping_ip(ip):
                    print(f"{Fore.GREEN} Viva!{Fore.RESET}")
                else:
                    print(f"{Fore.RED} Muerta.{Fore.RESET}")
                time.sleep(1)  # Espera 1 segundo antes de probar la siguiente IP
    except Exception as e:
        print(f"Error al leer el archivo: {e}")

if __name__ == "__main__":
    # Obtener la ruta del directorio donde se encuentra el script
    script_directory = os.path.dirname(os.path.abspath(__file__))
    
    # Seleccionar el archivo
    file_path = select_file(script_directory)
    
    if file_path:
        process_ips(file_path)