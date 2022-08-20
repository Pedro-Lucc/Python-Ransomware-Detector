# TODO
# MONITORAR O TAMANHO DOS ARQUIVOS (SE VÁRIOS ARQUIVOS ESTÃO FICANDO MAIORES EM UM CURTO PERÍODO DE TEMPO)
# CHECAR OS BYTES MODIFICADOS PARA CHECAR SE ESTÃO CRIPTOGRAFADOS
# MONITORAR A QUANTIDADE DE MODIFICAÇÕES POR SEGUNDO NO TAMANHO DOS ARQUIVOS OU NOS HONEYPOTS
# MONITORAR SE ALGUM ARQUIVO MODIFICADO POSSUI UMA EXTENSÃO SUSPEITA/DESCONHECIDA
# ALGUMA FORMA DE REALIZAR BACKUP DOS ARQUIVOS/SISTEMA/REGISTRO ETC
# CRIAR NOVOS HONEYPOTS PARA NOVOS DIRETÓRIOS
# ATUALIZAR JSON QUANDO ARQUIVOS HONEYPOT SÃO MOVIDOS

import hashlib
import json
import os
import re
from signal import SIGKILL
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import logging
from software.audit import Audit
from software.logger import logger
import time


# Classe FileSystemModifications, que herda a classe FileSystemEventHandler do watchdog
# event.src_path é basicamente o caminho que o handler retorna
class FileMonitor:
    def __init__(self, directory_list, honeypot_file_name, path_to_config_folder, json_file_name, honeypot_names_file, audit_obj):
        self.directory_list = directory_list
        self.honeypot_file_name = honeypot_file_name
        self.path_to_config_folder = path_to_config_folder
        self.json_file_name = json_file_name
        self.honeypot_names_file = honeypot_names_file
        self.audit_obj = audit_obj

    class EventHandler(FileSystemEventHandler):
        def __init__(self, data):
            self.directory_list = data[0]
            self.honeypot_file_name = data[1]
            self.path_to_config_folder = data[2]
            self.json_file_name = data[3],
            self.audit_obj = data[4]

        # Monitorar modificações nos honeypots
        def on_modified(self, event):
            if re.findall("([^\/]+$)", event.src_path)[0] in honeypot_names_data:
                start = time.perf_counter()
                try:
                    for dict in json_file_hashes:
                        if event.src_path == dict['absolute_path']:
                            with open(event.src_path, 'rb') as honeypot_file:
                                file_data = honeypot_file.read()
                                current_hash = hashlib.md5(file_data).hexdigest()
                                if current_hash != dict['hash']:
                                    logger.warning(f"Honeypot in {event.src_path} was modified!")
                                    ransomware_pid = self.audit_obj.getAuditRuleReport("pid")
                                    logger.critical(f"Proabable Ransomware process with PID: {ransomware_pid}")
                                    if ransomware_pid != None:
                                        os.kill(int(ransomware_pid), SIGKILL)
                                        end = time.perf_counter()
                                        logger.critical(f"Proabable Ransomware process with PID {ransomware_pid} was killed in {round(end - start, 3)}s!")

                except Exception as e:
                    logger.error(e)
                    if "start" in globals():
                        end = time.perf_counter()
                    pass

        # Monitorar caso algum diretório seja mudado de lugar, para atualizar o JSON dos honeypots
        def on_moved(self, event):
            logger.debug("Moved " + event.src_path)

        # Monitorar se algum diretório for deletado, para remover as entradas dos mesmos no JSON dos honeypots
        def on_deleted(self, event):
            logger.debug("Deleted " + event.src_path)

    def run(self):
        """Função para executar o file monitor"""
        global observers
        observers = []
        observer = Observer()
        event_handler = self.EventHandler([self.directory_list, self.honeypot_file_name, self.path_to_config_folder, self.json_file_name, self.audit_obj])

        for directory in self.directory_list:
            # Criação do observer
            observer.schedule(event_handler, directory, recursive=True)
            # Colocando o observer criado na lista dos observers
            observers.append(observer)

        observer.start()

        global json_file_hashes
        global honeypot_names_data
        honeypot_names_data = []
        json_file_path = os.path.join(self.path_to_config_folder, self.json_file_name)
        # input()
        honeypot_names_path = os.path.join(self.path_to_config_folder, self.honeypot_names_file)
        if os.path.exists(self.path_to_config_folder):
            try:
                with open(json_file_path) as json_file:
                    json_file_hashes = json.load(json_file)
            except FileNotFoundError:
                logger.error(f'Could not find {self.json_file_name} in {self.path_to_config_folder}')
                quit()
            try:
                with open(honeypot_names_path, "r") as names_file:
                    for line in names_file:
                        honeypot_names_data.append(line.rstrip())
            except FileNotFoundError:
                logger.error(f'Could not find {names_file} in {self.path_to_config_folder}')
                quit()

        else:
            logger.error(f'Could not find {self.json_file_name} in {self.path_to_config_folder}')
            quit()

        logger.debug('File Monitor has started...')
        try:
            while True:
                continue
        except KeyboardInterrupt:
            for observer in observers:
                observer.unschedule_all()
                observer.stop()
                observer.join()


# MAIN
if __name__ == "__main__":
    pass
else:
    from software.logger import logger
    logging.getLogger("watchdog.observers.inotify_buffer").disabled = True
