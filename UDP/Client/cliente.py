import socket
import os
import hashlib
from datetime import datetime
import logging

if __name__ == '__main__':
    dateTimeObj = datetime.now()
    logging.basicConfig(
        filename=f"Client/Logs/{dateTimeObj.year}-{dateTimeObj.month}-{dateTimeObj.day}-{dateTimeObj.hour}-{dateTimeObj.minute}-{dateTimeObj.second}.log", level=logging.INFO)

    cliente = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    ip = '192.168.85.128'
    puerto = 6000
    direccion = (ip, puerto)

    datos = 'Conexión exitosa'
    datos = datos.encode('utf8')

    cliente.sendto(datos, direccion)

    datos, direccion = cliente.recvfrom(1024)
    datos = datos.decode('utf8')
    objeto = datos.split("_")

    numeroClientes = objeto[0]
    numeroConexiones = objeto[1]
    nombreArchivo = objeto[2].split("/")[1]
    tamanioArchivo = objeto[3]
    hashS = objeto[4]

    datos, direccion = cliente.recvfrom(1024)
    datos = datos.decode('utf8')
    print(datos)

    print(f'Numero del cliente {numeroClientes} numero de conexiones {numeroConexiones}')

    print(f'nombre del archivo "{nombreArchivo}" tamaño del archivo {tamanioArchivo}')

    print(f'hash servidor: {hashS}')

    logging.info(f'Numero del cliente: {numeroClientes}')

    logging.info(f'Numero de conexiones: {numeroConexiones}')

    logging.info(f'Nombre del archivo: {nombreArchivo}')

    logging.info(f'Tamaño del archivo: {tamanioArchivo}')

    paquetesRecibidos = 0
    tiempoInicial = datetime.now()
    with open(f"Client/Recibidos/{numeroClientes}–Prueba-{numeroConexiones}.txt", "w") as f:
        while True:
            datos, direccion = cliente.recvfrom(1024)
            if(paquetesRecibidos == 0):
                tiempoInicial = datetime.now()
                print('Empieza la transferencia')
            if not datos:
                break

            datos = datos.decode('utf8')
            f.write(datos)
            paquetesRecibidos += 1

    tiempoFinal = datetime.now()
    print('Termina la transferencia')
    tiempoTranferencia = tiempoFinal-tiempoInicial

    tamanioArchivoRecibido = os.path.getsize(f"Client/Recibidos/{numeroClientes}–Prueba-{numeroConexiones}.txt")

    hash = hashlib.md5()
    with open(f"Client/Recibidos/{numeroClientes}–Prueba-{numeroConexiones}.txt", 'rb') as f:
        while True:
            datos = f.read(1024)
            if not datos:
                break
            hash.update(datos)

    hashC = hash.hexdigest()

    if hashC == hashS:
        archivoCorrecto = True 
    else:
        archivoCorrecto = False

    print(f'valor del hash del cliente: {hashC}')

    datos = f'{numeroClientes}_{archivoCorrecto}'
    datos = datos.encode('utf8')
    cliente.sendto(datos, direccion)
    cliente.close()

    logging.info(f'El archivo se recibe correctamente: {archivoCorrecto}')

    logging.info(f'tiempo de transferencia: {tiempoTranferencia}')

    logging.info(f'Numero de paquetes: {paquetesRecibidos}')

    logging.info(f'Numero de bytes: {tamanioArchivoRecibido}')