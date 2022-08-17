# TODO
# PRINTAR A QUANTIDADE DE DIRETÓRIOS EXISTENTES NO SISTEMA (COM BASE NOS DIRETÓRIOS PASSADOS) X
# INPUT DE QUAL INTERVALO DE DIRETÓRIOS SERÁ COLOCADO UM HONEYPOT X
# CRIAR NOVOS HONEYPOTS PARA NOVOS DIRETÓRIOS
# ATUALIZAR JSON E AS REGRAS QUANDO ARQUIVOS HONEYPOT SÃO MOVIDOS OU DELETADOS
# OPÇÃO DE GERAR ARQUIVOS OCULTOS OU NÃO PARA MAIOR SEGURANÇA

import json
import random
import string
import os
import hashlib
import time
from audit import Audit


class HoneypotGenerator:
    """Classe do Gerador de Honeypots"""

    def __init__(self, directory_list, honeypot_file_name, path_to_config_folder, json_file_name, path_to_audit_custom_rule_file, audit_custom_rules_key, honeypot_interval=2, disable_honeypot_interval=False, delete=False):
        self.directory_list = directory_list
        self.honeypot_file_name = honeypot_file_name
        self.path_to_config_folder = path_to_config_folder
        self.json_file_name = json_file_name
        self.path_to_audit_custom_rule_file = path_to_audit_custom_rule_file
        self.audit_custom_rules_key = audit_custom_rules_key
        self.honeypot_interval = honeypot_interval
        self.disable_honeypot_interval = disable_honeypot_interval
        self.delete = delete

        if honeypot_interval <= 1:
            logger.error("Honeypot interval should be 2 or greater!")
            quit()

    def __randomString(self):
        """Função para gerar uma string única e aleatória que ficará dentro de cada honeypot"""
        characters = string.ascii_letters + string.digits + string.punctuation
        random_string = ''.join(random.choice(characters) for i in range(50))
        return random_string

    def __generateHash(self, honeypot_file):
        """Função para gerar uma hash para o arquivo de honeypot criado"""
        file_data = honeypot_file.read()
        readable_hash = hashlib.md5(file_data).hexdigest()

        honeypot_file_hash_dict = {
            "absolute_path": honeypot_file.name,
            "hash": readable_hash
        }
        honeypot_files_hash_list.append(honeypot_file_hash_dict)

    def __generateHoneypots(self):
        """Função para gerar os honeypots"""
        global honeypot_files_hash_list
        honeypot_files_hash_list = []
        counter = 0

        for directory in self.directory_list:
            directory_count = 0
            for root in os.walk(directory):
                directory_count += 1

            logger.debug(f"Creating honeypots in: {directory}")
            logger.debug(f"There are {directory_count} subdirectories inside {directory}")
            logger.debug(f"The honeypot creation interval is set to: {self.honeypot_interval if not self.disable_honeypot_interval else 'disabled'}")
            logger.debug(f"It will be created {round(directory_count / self.honeypot_interval) if not self.disable_honeypot_interval else directory_count} honeypots")
            audit.createCustomRuleFile()
            for current_path, _, _ in os.walk(directory):
                counter += 1
                if counter % self.honeypot_interval == 0 or counter == 1 or self.disable_honeypot_interval:
                    try:
                        if os.access(current_path, os.W_OK):
                            # Criar o honeypot
                            with open(os.path.join(current_path, self.honeypot_file_name), 'w') as honeypot_file:
                                honeypot_file.write("THIS IS A PYTHON RANSOMWARE DETECTOR FILE! PLEASE! DO NOT MOVE, DELETE, RENAME OR MODIFY THIS FILE!\n")
                                honeypot_file.write(f"Unique string for this file: {self.__randomString()}")

                            # Gerar a hash para o honeypot criado
                            with open(os.path.join(current_path, self.honeypot_file_name), 'rb') as honeypot_file:
                                self.__generateHash(honeypot_file)

                            # Criar a regra no audit
                            audit.createAuditRule(os.path.join(current_path, self.honeypot_file_name))

                    except Exception as e:
                        logger.error(e)
                        continue
        audit.loadRules()

        # Gerar o JSON para os honeypot files criados e suas respectivas hashes
        self.__generateJson(honeypot_files_hash_list)

    def __generateJson(self, honeypot_files_hash_list):
        """Função para gerar o JSON com as entradas de cada honeypot"""
        json_object = json.dumps(honeypot_files_hash_list, indent=4)

        # Se a pasta config não existir, criar uma
        if not os.path.exists(self.path_to_config_folder):
            os.makedirs(self.path_to_config_folder)

        # Criar um novo .json com o objeto json criado
        with open(os.path.join(self.path_to_config_folder, self.json_file_name), 'w') as hashes_file:
            hashes_file.write(json_object)

    def __deleteHoneypots(self):
        """Função para deletar todos os honeypots"""
        for directory in self.directory_list:
            deleted_count = 0
            logger.debug(f"Deleting honeypots in: {directory}")
            for current_path, _, _ in os.walk(directory):
                try:
                    if os.access(current_path, os.W_OK):
                        os.remove(os.path.join(current_path, self.honeypot_file_name))
                        deleted_count += 1
                except Exception as e:
                    logger.error(f'Found an error in {current_path}: {str(e.__class__.__name__)}')
                    continue
            logger.debug(f"Deleted a total of {deleted_count} honeypots in {directory}")

    # Deletar o JSON das hashes
        self.__deleteJson()

    def __deleteJson(self):
        """Função deletar o JSON com as entradas de cada honeypot"""
        # Se a pasta config não existir, criar uma
        if os.path.exists(self.path_to_config_folder):
            try:
                os.remove(os.path.join(self.path_to_config_folder, self.json_file_name))
            except FileNotFoundError:
                logger.error(f'Could not find {self.json_file_name} in {self.path_to_config_folder}')
                quit()

    # Atualizar o json caso haja alguma mudança
    def updateJson(self):
        """Função para atualizar o JSON, modificando as entradas de cada honeypot afetado"""
        print("atualizar o json")

    def run(self):
        """Função para criar ou deletar os honeypots"""
        start = time.perf_counter()
        # CRIAR HONEYPOTS
        if not self.delete:
            self.__generateHoneypots()

        # DELETAR HONEYPOTS
        elif self.delete:
            self.__deleteHoneypots()
        end = time.perf_counter()
        logger.debug(f"{'Created' if not self.delete else 'Deleted'} honeypots in {round(end - start, 3)}")


if __name__ == "__main__":
    from logger import logger
    audit = Audit(
        path_to_audit="/etc/audit",
        path_to_audit_custom_rule_file="/etc/audit/rules.d/ransomware-detector.rules",
        path_to_audit_config="/etc/audit/auditd.conf",
        audit_custom_rules_key="ransomware-detector-key"
    )
    hg = HoneypotGenerator(
        directory_list=["/home/matheusheidemann/Documents/Github/Python-Ransomware-Detector/ransomware-samples/encrypt-test"],
        honeypot_file_name=".r4n50mw4r3-d373c70r.txt",
        path_to_config_folder="/home/matheusheidemann/Documents/Github/Python-Ransomware-Detector/software/config",
        json_file_name="ransom-detector-hashes-list.json",
        path_to_audit_custom_rule_file="/etc/audit/rules.d/ransomware-detector.rules",
        audit_custom_rules_key="ransomware-detector-key",
        # honeypot_interval=5,
        disable_honeypot_interval=False,
        delete=True
    )
    hg.run()

else:
    from software.logger import logger
