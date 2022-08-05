from cryptography.fernet import Fernet

# Gerar uma chave de criptografia
def generateKey():
    key_value = Fernet.generate_key()
    with open('key.key', 'wb') as key_file:
        key_file.write(key_value)

# Carregar a chave de criptografia gerada
def loadKey():
    return open('key.key', 'rb').read()