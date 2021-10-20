import socket
import logging
from datetime import datetime
import hashlib

tamanio = 1024
formato = "utf-8"
puerto = 6000
ip = '192.168.85.128'
direccion = (ip, puerto)

def main():
    dateTimeObj = datetime.now()
    logging.basicConfig(filename=f'ClienteServidor/UDP/Log/{dateTimeObj.year}-{dateTimeObj.month}-{dateTimeObj.day}-{dateTimeObj.hour}-{dateTimeObj.minute}-{dateTimeObj.second}.log', filemode='w', level=logging.DEBUG)

    cliente = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    cliente.connect(direccion)

    data = cliente.recv(tamanio).decode('utf-8')
    item = data.split("_")
    nombreArch = item[0]
    tamanioArchivo = int(item[1])
    ID = item[2]
    connectionNumber = item[3]
    ip = item[4]
    puerto = item[5]

    logging.info(
        f"Se recibio el archivo : {nombreArch} con tamaño de {tamanioArchivo}")

    logging.info(
        f"El cliente {ID}  se encuentra con la direccion: {ip} : {puerto}")

    print("\n Datos del archivo recibido")
    cliente.send("Datos del archivo recibido".encode(formato))

    numPaquetes = 0
    tiempoTranferenciaI = datetime.now()
    with open(f"ArchivosRecibidos/{ID}-Prueba-{connectionNumber}", "w") as f:
        while True:
            data = cliente.recv(tamanio).decode(formato)

            if not data:
                break

            f.write(data)
            cliente.send("Archivo recibido".encode(formato))
            numPaquetes += 1
    tiempoTranferenciaF = datetime.now()

    tiempoTranferencia = tiempoTranferenciaF-tiempoTranferenciaI
  
    BUF_SIZE = 1024

    with open(f"Cliente/ArchivosRecibidos/{ID}-Prueba-{connectionNumber}", 'rb') as f:
        while True:
            data = f.read(BUF_SIZE)
            if not data:
                break

    logging.info(f'Tiempo de transferencia : {tiempoTranferencia}')
    logging.info(
        f'Numero de paquetes recibidos fue: {numPaquetes}')
    logging.info(
        f"Numero de bytes recibidos fue: {numPaquetes*tamanio}")

    cliente.close()

if __name__ == "__main__":
    main()
