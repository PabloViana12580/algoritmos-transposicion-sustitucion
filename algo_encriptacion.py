"""
Universidad del Valle de Guatemala
Seguridad en sistemas de computación
Catedrático: Melinton Navas
Pablo Viana - 16091

Implementación de tres algoritmos de cifrado: 

-> uno transposición
-> uno sustitución
-> uno mixto

03 de marzo 2021

Referencias: 

-> https://www.tutorialspoint.com/cryptography_with_python/cryptography_with_python_decryption_of_transposition_cipher.htm
-> https://www.tutorialspoint.com/cryptography_with_python/cryptography_with_python_encryption_of_transposition_cipher.htm
-> programa one-time-pad desarrollado con anterioridad
"""

import string
import random
import sys
import pyperclip
import math


help = """ejecute los siguiente comandos para:
Encriptar con transposicion: python algo_encriptacion.py -transE
Desencriptar con transposicion: python algo_encriptacion.py -transD
Encriptar con sustitución: python algo_encriptacion.py -sustE
Encriptar con sustitución: python algo_encriptacion.py -sustD
Encriptar mixto: python algo_encriptacion.py -mixE
Encriptar mixto: python algo_encriptacion.py -mixD
"""
# obtenemos los caracteres del abecedario en minuscula
abecedario = string.ascii_lowercase
sustitucion_abc = list(abecedario)

def trans_encriptar(llave, mensaje):
    texto_encriptado = [''] * llave
    #la llave marca el numero total de columnas de la tabla
    for col in range(llave):
    	#primera posición siempre es el número de columna
        position = col
        while position < len(mensaje):
        	#realizamos una tabla donde vamos escribiendo el mensaje de manera vertical, por así decirle
            texto_encriptado[col] += mensaje[position]
            #Movemos la position una "llave" hacia adelante
            position += llave
    
    return ''.join(texto_encriptado)

def trans_desencriptar(llave, mensaje):
	#Calculamos el numero de columnas en base a longitud del mensaje y llave
	numOfColumns = math.ceil(len(mensaje) / llave)
	numOfRows = llave
	#numero de celdas de la tabla que no se llenaron
	numOfShadedBoxes = (numOfColumns * numOfRows) - len(mensaje)
	plaintext = [''] * numOfColumns
	col = 0
	row = 0
	
	#Desencriptamos el mensaje reccoriendo la tabla
	for symbol in mensaje:
	   plaintext[col] += symbol
	   col += 1
	   if (col == numOfColumns) or (col == numOfColumns - 1 and row >= numOfRows - numOfShadedBoxes):
	   	col = 0
	   	row += 1 
	
	return ''.join(plaintext)

def sust_encriptar(mensaje, llave):
	texto_encriptado = ''
	for index, char in enumerate(mensaje):
		# buscamos el indice del primer caracter del mensaje en el abecedario
		char_index = abecedario.index(char)
		# Buscamos el indice del caracter encontrado en el arreglo llave[posicion indice en que va el ciclo]
		llave_index = sustitucion_abc.index(llave[index])
		# realizamos el cifrad
		encriptado = (char_index + llave_index) % len(sustitucion_abc)
		# armamos la palabra encriptad
		texto_encriptado += abecedario[encriptado]

	return texto_encriptado


def sust_desencriptar(mensaje, llave):
	# Revisa que los parametros sean strings validos para no computar un string vacio
	if mensaje == '' or llave == '':
		return ''

	# Tomamos el indice del primer caracter del mensaje en el abecedario
	char_index = abecedario.index(mensaje[0])
	# Tomamos el indice del primer caracter de la llave en el abecedario
	llave_index = sustitucion_abc.index(llave[0])

	# Realizamos el Desencriptado
	desencriptado = (char_index - llave_index) % len(sustitucion_abc)
	# Buscamos un solo caracter desencriptado en el abecedario
	character = abecedario[desencriptado]

	# Recursivamente, buscamos los demas caracteres en el abecedario
	return character + sust_desencriptar(mensaje[1:], llave[1:])

def llave_sustitucion(mensaje):
	#Creamos la llave aleatoria que servira como criterio de sustitución para el mensaje
    dict_llave = list(string.ascii_lowercase)
    random.shuffle(dict_llave)
    llave = dict_llave[:len(mensaje)]
    llave_txt = ''.join([str(elem) for elem in llave])
    #La escribimos en archivo de texto
    text_file = open("llave_sustitucion.txt", "w")
    text_file.write(llave_txt)
    text_file.close()
    #Encriptamos con sustitución
    return llave_txt

def llave_transposicion(mensaje):
	#Creamos llave de manera aleatoria
	llave_transposicion = random.randint(0,(len(mensaje)//2))
	#guardamos la llave en un archivo de texto
	text_file = open("llave_transposicion.txt", "w")
	text_file.write(str(llave_transposicion))
	text_file.close()

	return llave_transposicion


if __name__ == '__main__':
    availableOpt = ["-transE", "-transD", "-sustE", "-sustD", "-mixE", "-mixD"]
    if len(sys.argv) == 1 or sys.argv[1] not in availableOpt:
        print(help)
        exit(0)

    revi = True
    while(revi):
    	mensaje = input("mensaje a descifrar: ")
    	if (len(mensaje)>26):
    		print("mensaje demasiado largo")
    	else:
    		revi = False

   	#encriptar transposicion
    if sys.argv[1] == availableOpt[0]:
        #Creamos llave de manera aleatoria
        llave_transposicion = llave_transposicion(mensaje)
        #Ecriptamos el texto con transposición
        texto_cifrado = trans_encriptar(llave_transposicion, mensaje)
        #Imprimimos en pantalla
        print("texto cifrado:")
        print(texto_cifrado + '|')
        #Copiamos mensaje encriptado al portapapeles
        pyperclip.copy(texto_cifrado)

    #descifrar transposición
    elif sys.argv[1] == availableOpt[1]:
    	#Abrimos archivo con la llave de transposición aleatoria
    	text_file = open("llave_transposicion.txt", "r")
    	myKey = text_file.read()
    	#Desencriptamos el mensaje
    	plaintext = trans_desencriptar(int(myKey), mensaje)
    	#Imprimos en pantalla y copiamos al portapapeles
    	pyperclip.copy(plaintext)
    	print(plaintext)

    #Encriptar sustitución
    elif sys.argv[1] == availableOpt[2]:
    	#creamos llave a utilizar
    	llave = llave_sustitucion(mensaje)
    	#encriptamos con sustitución
    	text_crip = sust_encriptar(mensaje.replace(" ",""), llave)
    	#Imprimimos resultado en pantalla y copiamos al portapapeles
    	pyperclip.copy(text_crip)
    	print(text_crip)

    #descifrar sustitucion
    elif sys.argv[1] == availableOpt[3]:
    	#Abrimos llave única y aleatoria de sustitución
    	text_file = open("llave_sustitucion.txt", "r")
    	llave = text_file.read()
    	#Deciframos 
    	text_crip = sust_desencriptar(mensaje, llave)
    	#Imprimimos resultado en pantalla y copiamos al portapapeles
    	pyperclip.copy(text_crip)
    	print(text_crip)

    #Encriptar mixto
    elif sys.argv[1] == availableOpt[4]:
    	
    	#------Encriptamos con sustitución-----
    	print("encriptando por sustitución")
    	#creamos llave a utilizar
    	llave = llave_sustitucion(mensaje)
    	#encriptamos con sustitución
    	text_crip = sust_encriptar(mensaje.replace(" ",""), llave)
    	#------Encriptamos con transposición------
    	print("encriptando por transposicion")
    	#Creamos llave de manera aleatoria
    	llave_transposicion = llave_transposicion(text_crip)
    	#Ecriptamos el texto con transposición
    	texto_cifrado = trans_encriptar(llave_transposicion, text_crip)
    	#Imprimimos resultado en pantalla y copiamos al portapapeles
    	pyperclip.copy(texto_cifrado)
    	print(texto_cifrado)

    #descifrar mixto
    elif sys.argv[1] == availableOpt[5]:
    	
    	#------Deciframos con transposición------
    	print("decifrando por transposición")
    	#Abrimos archivo con la llave de transposición aleatoria
    	text_file = open("llave_transposicion.txt", "r")
    	myKey = text_file.read()
    	#Desencriptamos el mensaje
    	plaintext = trans_desencriptar(int(myKey), mensaje)
    	#Imprimos en pantalla y copiamos al portapapeles
    	#------Deciframos con sustitución------
    	print("decifrando por sustitución")
    	#Abrimos llave única y aleatoria de sustitución
    	text_file = open("llave_sustitucion.txt", "r")
    	llave = text_file.read()
    	#Deciframos 
    	text_crip = sust_desencriptar(plaintext, llave)
    	pyperclip.copy(text_crip)
    	print(text_crip)

