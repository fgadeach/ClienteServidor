import socket
import logging
from datetime import datetime
import hashlib

tamanio = 1024
formato = "utf-8"
puerto = 8888
ip = '192.168.80.128'
direccion = (ip, puerto)

def main():
    dateTimeObj = datetime.now()
    logging.basicConfig(filename=f'Logs/{dateTimeObj.year}-{dateTimeObj.month}-{dateTimeObj.day}-{dateTimeObj.hour}-{dateTimeObj.minute}-{dateTimeObj.second}.log', filemode='w', level=logging.DEBUG)

    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cliente.connect(direccion)

    data = cliente.recv(tamanio).decode('utf-8')
    item = data.split("_")
    nombreArch = item[0]
    tamanioArchivo = int(item[1])
    ID = item[2]
    connectionNumber = item[3]
    hashServidor = item[4]
    ip = item[5]
    puerto = item[6]

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

    md5 = hashlib.md5()

    with open(f"ArchivosRecibidos/{ID}-Prueba-{connectionNumber}", 'rb') as f:
        while True:
            data = f.read(BUF_SIZE)
            if not data:
                break
            md5.update(data)

    hashCliente = md5.hexdigest()
   
    if(hashCliente == hashServidor):
        print(
            "La llave privada concuerda con las dos partes")
        cliente.send('PROTOCOLO CORRECTO'.encode(formato))
        logging.info('Se entrego el archivo exitosamente')
    else:
        print("Se comparo los hashing del servidor y del cliente y el archivo NO llego correctamente")
        cliente.send('ERROR EN EL ENVIO'.encode(formato))
        logging.info('No se pudo concluir la entrega del archivo')

    logging.info(f'Tiempo de transferencia : {tiempoTranferencia}')
    logging.info(
        f'Numero de paquetes recibidos fue: {numPaquetes}')
    logging.info(
        f"Numero de bytes recibidos fue: {numPaquetes*tamanio}")

    cliente.close()

if __name__ == "__main__":
    main()
