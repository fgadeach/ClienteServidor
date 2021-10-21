import socket
import threading
import os
import hashlib
import logging
from datetime import datetime

def Cliente(servidor, direccion, nombreArchivo, cliente, tamanioArchivo):

    print(f'Inicia transferencia con el cliente {cliente}')
    numeroPaquetes = 0
    tiempoInicial = datetime.now()

    with open(nombreArchivo, "r") as f:
        while True:
            datos = f.read(1024)
            datos = datos.encode('utf-8')

            if not datos:
                servidor.sendto(datos, direccion)
                break

            server.sendto(datos, direccion)
            numeroPaquetes += 1

    tiempoFinal = datetime.now()

    print(f'Termina la transferencia con el cliente {cliente}')
    tiempoTotal = tiempoFinal-tiempoInicial

    datos, direccion = server.recvfrom(1024)
    datos = datos.decode("utf-8")
    objeto = datos.split("_")
    logging.info(f'el cliente {objeto[0]} recibe: {objeto[1]}')
    logging.info(f'El la transferencia con el {cliente} fue de: {tiempoTotal}')
    logging.info(f'numero de paquetes al {cliente}: {numeroPaquetes}')
    logging.info(f'Se envio un total de: {tamanioArchivo} bytes')


if __name__ == '__main__':

    dateTimeObj = datetime.now()

    logging.basicConfig(filename=f"Logs/{dateTimeObj.year}-{dateTimeObj.month}-{dateTimeObj.day}-{dateTimeObj.hour}-{dateTimeObj.minute}-{dateTimeObj.second}.log", level=logging.INFO)

    ip = '192.168.85.128'
    puerto = 6000

    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    server.bind((ip, puerto))
    print('Servidor inicializado')

    conexionesActivas = 0
    conexionesRequeridas = 0
    conexion = False

    while(not conexion):
        totalConexiones = input("El numero de conexiones debe de estar entre 1 y 25:")
        if(int(totalConexiones) >= 1 and int(totalConexiones) <= 25):
            conexion = True
            print(f'total conexiones: {totalConexiones}')
        else:
            print(f"{totalConexiones} numero invalido")

    conexionesRequeridas = int(totalConexiones)

    archivoTest = False
    nombreArchivo = ""
    tamanioArchivo = 0
    while (not archivoTest):
        archivo = input("Ingrese 1 para el archivo de 100MB o ingrese 2 para el archivo de 250MB:")
        
        if(int(archivo) == 2):
            nombreArchivo = "Archivos/250MB.txt"
            tamanioArchivo = os.path.getsize(nombreArchivo)
            archivoTest = True

        elif(int(archivo) == 1):
            nombreArchivo = "Archivos/100MB.txt"
            tamanioArchivo = os.path.getsize(nombreArchivo)
            archivoTest = True

        else:
            print("Archivo Invalido (Inputs debe ser 1 o 2)")
        print(f'Nombre del archivo: {nombreArchivo}')

    logging.info(f'Nombre del archivo enviado: {nombreArchivo}')
    logging.info(f'Tamanio del archivo: {tamanioArchivo} bytes')

    print(f'Numero de conexiones {totalConexiones} para empezar transferencia')

    hash = hashlib.md5()
    with open(nombreArchivo, 'rb') as f:
        while True:
            datos = f.read(1024)
            if not datos:
                break
            hash.update(datos)
    hashServidor = hash.hexdigest()

    ts = []

    while(conexionesActivas < conexionesRequeridas):
        datos, direccion = server.recvfrom(1024)
        datos = datos.decode("utf-8")
        print(datos)
        conexionesActivas += 1

        datos = f'{conexionesActivas}_{conexionesRequeridas}_{nombreArchivo}_{tamanioArchivo}_{hashServidor}'
        datos = datos.encode("utf-8")
        server.sendto(datos, direccion)

        datos = 'Conexion exitosa'
        datos = datos.encode("utf-8")
        server.sendto(datos, direccion)

        t = threading.Thread(target=Cliente,args=(server, direccion, nombreArchivo, conexionesActivas, tamanioArchivo))
        ts.append(t)

        logging.info(f'cliente {conexionesActivas}, direccion: {direccion}')

        print(f"Conexion con el cliente {conexionesActivas} exitosa")

        if(conexionesRequeridas - conexionesActivas == 0):
            print(f'inicia transferencia')
        else:
            print(f'Numero de conexiones {conexionesRequeridas-conexionesActivas} para empezar transferencia')

    i = 0
    while (i < conexionesActivas):
        ts[i].start()
        i += 1