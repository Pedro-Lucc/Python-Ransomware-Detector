import random
import string
import os
import hashlib


def randomString():
    # get random password pf length 8 with letters, digits, and symbols
    characters = string.ascii_letters + string.digits + string.punctuation
    random_string = ''.join(random.choice(characters) for i in range(50))
    print("Random password is:", random_string)
    return random_string


def generateHash(honeypot_file):
    file_data = honeypot_file.read()  # read file as bytes
    readable_hash = hashlib.md5(file_data).hexdigest()
    honeypot_file_hash_dict = {
        "absolute_path": honeypot_file.name,
        "hash": readable_hash
    }
    honeypot_files_hash_list.append(honeypot_file_hash_dict)
    print(honeypot_files_hash_list)


def generateHoneypots(directory, honeypot_file_name):
    global honeypot_files_hash_list
    if 1 == 2:
        for current_path, _, files_in_current_path in os.walk(directory):
            with open(current_path + '/' + honeypot_file_name, 'w') as file:
                file.write("THIS IS A PYTHON RANSOMWARE DETECTOR FILE! PLEASE! DO NOT MOVE, DELETE, RENAME OR MODIFY THIS FILE!\n")
                honeypot_file.write(randomString())
            with open(directory + '/' + '.ransomware-detector', 'rb') as honeypot_file:
                generateHash(honeypot_file)
    else:
        with open(directory + '/' + honeypot_file_name, 'w') as honeypot_file:
            honeypot_file.write("THIS IS A PYTHON RANSOMWARE DETECTOR FILE! PLEASE! DO NOT MOVE, DELETE, RENAME OR MODIFY THIS FILE!\n")
            honeypot_file.write(randomString())
        with open(directory + '/' + '.ransomware-detector', 'rb') as honeypot_file:
            generateHash(honeypot_file)


def deleteHoneypots(directory, honeypot_file_name):
    for current_path, _, files_in_current_path in os.walk(directory):
        os.remove(directory + '/' + honeypot_file_name)


if __name__ == "__main__":
    # Lista de diretórios que terão honeypots criados
    directory_list = ["/home/matheusheidemann/Documents/Python Files/Python-Ransomware-Detector/ransomware-samples/encrypt-test"]
    honeypot_files_hash_list = []
    honeypot_file_name = ".r4n50mw4r3-d373c70r"
    generateHoneypots(directory_list, honeypot_file_name)
