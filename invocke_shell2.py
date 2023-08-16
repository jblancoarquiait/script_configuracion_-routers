import csv
import paramiko
import time
from getpass import getpass


# Datos de conexión SSH
ip = '10.200.11.107'  # Dirección IP del enrutador
port = 22            # Puerto SSH por defecto
username = 'jblanco' #  Usuario
password = 'M4r14n4.S4nch3z'
#password = getpass("Ingrese su contraseña:  ")

def configure_router(ip, username, password, commands):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(ip, username=username, password=password, look_for_keys=False)

    channel = client.invoke_shell()
    time.sleep(2)  # Espera para que la shell esté lista

    for command in commands:
        channel.send(command + "\n")
        time.sleep(1)

    output = ""
    while channel.recv_ready():
        output += channel.recv(1024).decode("utf-8")

    client.close()
    return output

def main():
    with open("datos_routers.csv", "r") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            ip_address_t = row["ip_address_t"]
            username_t = row["username_t"]
            password_t = row["password_t"]
            commands = [
                f"ssh -l {username_t} {ip_address_t}",# Ejemplo de comando de configuración
                f"{password_t}",
                f"sh int desc", 
                f"sh arp",
                f"sh mac-",
                f"exit"
                ] 
            commands2 = [
                f"ssh -l {username_t} {ip_address_t}",# Ejemplo de comando de configuración
                f"{password_t}",
                f"ping 172.30.1.56 so lo 10 re 50 si 1500",
                f"exit"
                ]
            
            
            result = configure_router(ip, username, password, commands)
            print(f"Resultado para {ip}:\n{result}")

if __name__ == "__main__":
    main()
