# Proceso de solución de los requerimientos de la practica grupo 5 Seccion1

## Instalación del servidor en la máquina virtual.

1. Se clona el repositorio en la maquina servidor https://github.com/fgadeach/ClienteServidor
2. Hacer cd en la carpeta Servidor/Envio
3. Se crean los archivos a enviar con los comandos en ubuntu de la siguiente forma:

dd if=/dev/zero of=100MB.txt count=10000 bs=10000
dd if=/dev/zero of=250MB.txt count=15812 bs=15812

4. Se corre el archivo .py en la ruta del servidor de la siguiente forma:

python3 servidor.py
7. Se indica el numero de clientes a conectar.
8. Se indica con 1 o 2 el archivo que se debe enviar.

## Instalacion del Cliente en la otra máquina en la que se va a generar la conexión

1. Se clona el repositorio en la maquina servidor https://github.com/fgadeach/ClienteServidor
2. Se corre el número de threads necesario basado en el numero de conexiones escogidas.
3. Se corre el archivo .py en la ruta del servidor de la siguiente forma::

python3 cliente.py

