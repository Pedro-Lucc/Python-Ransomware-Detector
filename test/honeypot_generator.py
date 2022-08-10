# TODO PRINTAR A QUANTIDADE DE DIRETÓRIOS EXISTENTES NO SISTEMA, INPUT DE QUAL INTERVALO DE DIRETÓRIOS SERÁ COLOCADO UM HONEYPOT

import random
import string
import os
import hashlib
from timeit import default_timer as timer


# Gerar string aleatória
def randomString():
    # get random password pf length 8 with letters, digits, and symbols
    characters = string.ascii_letters + string.digits + string.punctuation
    random_string = ''.join(random.choice(characters) for i in range(50))
    return random_string


# Gerar uma hash para o arquivo honeypot
def generateHash(honeypot_file):
    file_data = honeypot_file.read()  # read file as bytes
    readable_hash = hashlib.md5(file_data).hexdigest()
    honeypot_file_hash_dict = {
        "absolute_path": honeypot_file.name,
        "hash": readable_hash
    }
    honeypot_files_hash_list.append(honeypot_file_hash_dict)


# Gerar as honeypots
def generateHoneypots(directory_list, honeypot_file_name):
    global honeypot_files_hash_list
    counter = 0
    for directory in directory_list:
        for current_path, _, _ in os.walk(directory):
            counter = counter + 1
            if counter % 1 == 0 or counter == 1 or 1 == 1:
                # Criar um honeypot a cada 10 diretórios
                with open(current_path + '/' + honeypot_file_name, 'w') as honeypot_file:
                    honeypot_file.write("THIS IS A PYTHON RANSOMWARE DETECTOR FILE! PLEASE! DO NOT MOVE, DELETE, RENAME OR MODIFY THIS FILE!\n")
                    honeypot_file.write(randomString())
                with open(current_path + '/' + honeypot_file_name, 'rb') as honeypot_file:
                    generateHash(honeypot_file)


# Deletar as honeypots
def deleteHoneypots(directory, honeypot_file_name):
    for current_path, _, files in os.walk(directory):
        os.remove(current_path + '/' + honeypot_file_name)


# Main
if __name__ == "__main__":
    start = timer()
    if not os.path.exists('./ransom-detector-hashes-list'):
        # DEbug para deletar
        delete = True
        # Lista de diretórios que terão honeypots criados
        directory_list = ["/home/"]
        # Lista com o hash de cada hobneypot criado
        honeypot_files_hash_list = []
        honeypot_file_name = ".r4n50mw4r3-d373c70r"

        if not delete:
            generateHoneypots(directory_list, honeypot_file_name)
        else:
            for directory in directory_list:
                deleteHoneypots(directory, honeypot_file_name)

        with open('./test/ransom-detector-hashes-list', 'w') as hashes_file:
            if not delete:
                index = 0
                for honeypot_dict in honeypot_files_hash_list:
                    hashes_file.write(f"[{index}] Directory: {honeypot_dict['absolute_path']} --- MD5 Hash: {honeypot_dict['hash']}\n")
                    index = index + 1
            else:
                os.remove('./test/ransom-detector-hashes-list')

    end = timer()
    time_taken = end - start
    print(f"Ação realizada com sucesso em {round(time_taken)} segundos.")
