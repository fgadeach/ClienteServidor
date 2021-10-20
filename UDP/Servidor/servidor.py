import socket
import threading
import os
import logging
from datetime import datetime
import hashlib

tamanio = 1024
formato = "utf-8"
puerto = 6000
ip = '192.168.152.128'
direccion = (ip, puerto)

def manejarCliente(conn, addr, nombreArch, tamanioArchivo, ID, connectionNumber, hashServidor, ip, puerto):
    logging.info(f'Se genero la conexion {ID} desde {ip}:{puerto}')

    print(" Conexion del cliente {addr}: ready")

    data = f"{nombreArch}_{tamanioArchivo}_{ID}_{connectionNumber}_{hashServidor}_{ip}_{puerto}"
    conn.send(data.encode(formato))
    mensaje = conn.recv(tamanio).decode(formato)
    print("Respuesta del cliente: " + mensaje)

    numPaquetesEnviados = 0
    tiempoTranferenciaI = datetime.now()
    with open(nombreArch, "r") as f:
        while True:
            data = f.read(tamanio)

            if not data:
                break

            conn.send(data.encode(formato))
            mensaje = conn.recv(tamanio).decode(formato)
            numPaquetesEnviados += 1
    tiempoTranferenciaF = datetime.now()

    tiempoTranferencia = tiempoTranferenciaF-tiempoTranferenciaI
    logging.info(
        f'Tiempo de transferencia de cliente {ID} fue: {tiempoTranferencia}')

    logging.info(
        f'Numero de paquetes enviados al cliente {ID} fueron: {numPaquetesEnviados}')
    logging.info(
        f'Numero de bytes enviados al cliente {ID} fueron: {numPaquetesEnviados*tamanio}')
    conn.close()

def main():
    dateTimeObj = datetime.now()
    logging.basicConfig(
        filename=f"Logs/{dateTimeObj.year}-{dateTimeObj.month}-{dateTimeObj.day}-{dateTimeObj.hour}-{dateTimeObj.minute}-{dateTimeObj.second}.log", level=logging.INFO)

    numValidoConexiones = False
    while(not numValidoConexiones):
        numConexiones = input("Ingrese numero de conexiones:")
        if(int(numConexiones) >= 1 and int(numConexiones) <= 25):
            numValidoConexiones = True
        else:
            print(f"{numConexiones} El numero de conexiones debe de estar entre 1 y 25")

    connectionNumber = int(numConexiones)

    archivoValido = False
    while(not archivoValido):
        archivo = input("Ingrese 1 para el archivo de 100MB o ingrese 2 para el archivo de 250MB:")
        if(int(archivo) == 2):
            nombreArch = "ArchivosEnvio/250MB.txt"
            tamanioArchivo = os.path.getsize(nombreArch)
            archivoValido = True
        elif(int(archivo) == 1):
            nombreArch = "ArchivosEnvio/100MB.txt"
            tamanioArchivo = os.path.getsize(nombreArch)
            archivoValido = True
        else:
            print("Archivo Invalido (Inputs debe ser 1 o 2)")

    ## HASHING ##
    BUF_SIZE = 1024

    logging.info(f'Nombre del archivo enviado : {nombreArch}')
    logging.info(f'Tamanio del archivo  : {tamanioArchivo}')

    servidor = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    servidor.bind(direccion)
    servidor.listen()
    print("Servidor en standby ....")

    threads = []

    clientsNumber = 0

    
    while (clientsNumber < connectionNumber):
        conn, addr = servidor.accept()
        clientsNumber += 1
        print(f"Conexion del cliente desde {addr[0]}:{addr[1]}")
        thread = threading.Thread(target=manejarCliente, args=(
            conn, addr, nombreArch, tamanioArchivo, clientsNumber, connectionNumber, addr[0], {addr[1]}))
        threads.append(thread)
        print(f" Hilos de ejecucion en este momento: {threading.active_count()-1}")
        print(f"Conexion de clientes: {clientsNumber}")

    i = 0
    while(i < clientsNumber):
        threads[i].start()
        i += 1

    servidor.close()


if __name__ == "__main__":
    main()
