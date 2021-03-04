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
"""

import string
import random
import sys
import pyperclip
import math


help = """ejecute los siguiente comandos para:
Encriptar con transposicion: python algo_encriptacion.py -transE
Desencriptar con transposicion: python algo_encriptacion.py -transD
"""


def trans_encriptar(llave, mensaje):
    texto_encriptado = [''] * llave

    for col in range(llave):
        position = col
        while position < len(mensaje):
            texto_encriptado[col] += mensaje[position]
            position += llave
    
    return ''.join(texto_encriptado)

def trans_desencriptar(llave, mensaje):
	numOfColumns = math.ceil(len(mensaje) / llave)
	numOfRows = llave
	numOfShadedBoxes = (numOfColumns * numOfRows) - len(mensaje)
	plaintext = [''] * numOfColumns
	col = 0
	row = 0
	
	for symbol in mensaje:
	   plaintext[col] += symbol
	   col += 1
	   if (col == numOfColumns) or (col == numOfColumns - 1 and row >= numOfRows - numOfShadedBoxes):
	   	col = 0
	   	row += 1 
	
	return ''.join(plaintext)

if __name__ == '__main__':
    availableOpt = ["-transE", "-transD"]
    if len(sys.argv) == 1 or sys.argv[1] not in availableOpt:
        print(help)
        exit(0)

    mensaje = input("mensaje a descifrar: ")

    
    if sys.argv[1] == availableOpt[0]:
        #Creamos llave de manera aleatoria
        llave_transposicion = random.randint(0,(len(mensaje)//2))
        #guardamos la llave en un archivo de texto
        text_file = open("llave_transposicion.txt", "w")
        text_file.write(str(llave_transposicion))
        text_file.close()

        texto_cifrado = trans_encriptar(llave_transposicion, mensaje)

        print("texto cifrado:")
        print(texto_cifrado + '|')
        pyperclip.copy(texto_cifrado)
    #Decifrar transposición
    elif sys.argv[1] == availableOpt[1]:
    	text_file = open("llave_transposicion.txt", "r")
    	myKey = text_file.read()
    	plaintext = trans_desencriptar(int(myKey), mensaje)
    	print(plaintext)
