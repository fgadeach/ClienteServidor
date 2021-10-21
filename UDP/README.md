# Lab_3_Redes Grupo 11 Seccion 2

## Instalacion Servidor

1. Instalar Python3.0 en la maquina en caso de que no este ya instalado
2. Clonar repositorio en la maquina servidor
3. Ubicarse en la carpeta Servidor/Archivos

```bash
cd Servidor/Archivos
```

4. Correr los siguientes comandos (Unicamente funcionan en Linux o Mac):

```bash
dd if=/dev/zero of=100MB.txt count=10000 bs=10000
dd if=/dev/zero of=250MB.txt count=15812 bs=15812
```

5. Volver a la carpeta Servidor

```bash
cd ..
```

6. Correr la aplicacion con el siguiente comando:

```bash
python3 servidor.py
```

7. Indicar el numero de clientes que se deben conectar (numero entre 1 y 25)
8. Indicar el archvo que se desea recibir ("1" Para recibir el archivo de 100MB y "2" Para recibir el archivo de 250MB)

## Instalacion Cliente

1. Instalar Python3.0 en la maquina en caso de que no este ya instalado
2. Clonar repositorio en la maquina servidor
3. Ubicarse en la carpeta Cliente envio

```bash
cd Cliente
```

4. Campiar la constante IP en cliente.py a la IP del servidor
5. Abrir el numero de terminales segun el numero ingresado en el punto 7 del servidor (Puede ser en VSCode)
6. Correr el siguiente comando en todas las terminales:

```bash
python3 cliente.py
```
