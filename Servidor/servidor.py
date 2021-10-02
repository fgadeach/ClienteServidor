import socket
import threading
import os
import logging
from datetime import datetime
import hashlib

IP = socket.gethostbyname(socket.gethostname())
PUERTO = 8888
DIRECCION = (IP, PUERTO)
TAMANIO = 1024
FORMATO = "utf-8"


def manejarCliente(conn, addr, NOM_ARCHIVO, TAM_ARCHIVO, ID, NUM_CONEXIONES, hashServidor, ip, puerto):
    logging.info(f'Se conecto el cliente {ID} desde {ip}:{puerto}')

    print("[+] Nueva conexion {addr}: conectado")

    data = f"{NOM_ARCHIVO}_{TAM_ARCHIVO}_{ID}_{NUM_CONEXIONES}_{hashServidor}_{ip}_{puerto}"
    conn.send(data.encode(FORMATO))
    mensaje = conn.recv(TAMANIO).decode(FORMATO)
    print("[-] El cliente responde: " + mensaje)

    numPaquetesEnviados = 0
    tiempoTranferenciaI = datetime.now()
    with open(NOM_ARCHIVO, "r") as f:
        while True:
            data = f.read(TAMANIO)

            if not data:
                break

            conn.send(data.encode(FORMATO))
            mensaje = conn.recv(TAMANIO).decode(FORMATO)
            numPaquetesEnviados += 1
    tiempoTranferenciaF = datetime.now()

    tiempoTranferencia = tiempoTranferenciaF-tiempoTranferenciaI
    logging.info(
        f'El tiempo de transferencia del cliente {ID} fue de: {tiempoTranferencia}')

    logging.info(
        f'El numero de paquetes enviado al cliente {ID} fue: {numPaquetesEnviados}')
    logging.info(
        f'El numero de bytes enviado al cliente {ID} fue: {numPaquetesEnviados*TAMANIO}')
    conn.close()


def main():
    dateTimeObj = datetime.now()
    logging.basicConfig(
        filename=f"Logs/{dateTimeObj.year}-{dateTimeObj.month}-{dateTimeObj.day}-{dateTimeObj.hour}-{dateTimeObj.minute}-{dateTimeObj.second}.log", level=logging.INFO)

    numValidoConexiones = False
    while(not numValidoConexiones):
        numConexiones = input("Numero de conexiones (1-25):")
        if(int(numConexiones) >= 1 and int(numConexiones) <= 25):
            numValidoConexiones = True
        else:
            print(f"{numConexiones} no es un numero valido de conexiones")

    NUM_CONEXIONES = int(numConexiones)

    archivoValido = False
    while(not archivoValido):
        archivo = input("Escoja entre el archivo 1(100MB) o 2(250MB):")
        if(int(archivo) == 2):
            NOM_ARCHIVO = "ArchivosEnvio/250MB.txt"
            TAM_ARCHIVO = os.path.getsize(NOM_ARCHIVO)
            archivoValido = True
        elif(int(archivo) == 1):
            NOM_ARCHIVO = "ArchivosEnvio/100MB.txt"
            TAM_ARCHIVO = os.path.getsize(NOM_ARCHIVO)
            archivoValido = True
        else:
            print("El archivo escogido no es valido")

    ## HASHING ##
    BUF_SIZE = 1024

    md5 = hashlib.md5()

    with open(NOM_ARCHIVO, 'rb') as f:
        while True:
            data = f.read(BUF_SIZE)
            if not data:
                break
            md5.update(data)

    hashServidor = md5.hexdigest()

    ## HASHING ##

    logging.info(f'El nombre del archivo envidado : {NOM_ARCHIVO}')
    logging.info(f'El tamanio del archivo enviado es : {TAM_ARCHIVO}')

    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.bind(DIRECCION)
    servidor.listen()
    print("[+] Servidor escuchando ....")

    threads = []

    NUM_CLIENTES = 0
    while (NUM_CLIENTES < NUM_CONEXIONES):
        conn, addr = servidor.accept()
        NUM_CLIENTES += 1
        print(f"[+] Cliente conectado desde {addr[0]}:{addr[1]}")
        thread = threading.Thread(target=manejarCliente, args=(
            conn, addr, NOM_ARCHIVO, TAM_ARCHIVO, NUM_CLIENTES, NUM_CONEXIONES, hashServidor, addr[0], {addr[1]}))
        threads.append(thread)
        print(f"[+] Threads activos: {threading.active_count()-1}")
        print(f"[+] Clientes conectados: {NUM_CLIENTES}")

    i = 0
    while(i < NUM_CLIENTES):
        threads[i].start()
        i += 1

    servidor.close()


if __name__ == "__main__":
    main()
