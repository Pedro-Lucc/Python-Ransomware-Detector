# TODO
# MONITORAR O TAMANHO DOS ARQUIVOS (SE VÁRIOS ARQUIVOS ESTÃO FICANDO MAIORES EM UM CURTO PERÍODO DE TEMPO)
# CHECAR OS BYTES MODIFICADOS PARA CHECAR SE ESTÃO CRIPTOGRAFADOS
# MONITORAR A QUANTIDADE DE MODIFICAÇÕES POR SEGUNDO NO TAMANHO DOS ARQUIVOS OU NOS HONEYPOTS
# MONITORAR SE ALGUM ARQUIVO MODIFICADO POSSUI UMA EXTENSÃO SUSPEITA/DESCONHECIDA
# ALGUMA FORMA DE REALIZAR BACKUP DOS ARQUIVOS/SISTEMA/REGISTRO ETC
# CRIAR NOVOS HONEYPOTS PARA NOVOS DIRETÓRIOS
# ATUALIZAR JSON QUANDO ARQUIVOS HONEYPOT SÃO MOVIDOS

from datetime import datetime
import hashlib
import json
import os
from signal import SIGKILL
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import logging
from audit import Audit


# Classe FileSystemModifications, que herda a classe FileSystemEventHandler do watchdog
# event.src_path é basicamente o caminho que o handler retorna
class FileMonitor:
    def __init__(self, directory_list, honeypot_file_name, path_to_config_folder, json_file_name):
        self.directory_list = directory_list
        self.honeypot_file_name = honeypot_file_name
        self.path_to_config_folder = path_to_config_folder
        self.json_file_name = json_file_name

    class EventHandler(FileSystemEventHandler):
        def __init__(self, data):
            self.directory_list = data[0]
            self.honeypot_file_name = data[1]
            self.path_to_config_folder = data[2]
            self.json_file_name = data[3]

        # Monitorar modificações nos honeypots
        def on_modified(self, event):
            if self.honeypot_file_name in event.src_path:
                try:
                    for dict in json_file_hashes:
                        if event.src_path == dict['absolute_path']:
                            with open(event.src_path, 'rb') as honeypot_file:
                                file_data = honeypot_file.read()
                                current_hash = hashlib.md5(file_data).hexdigest()
                                if current_hash != dict['hash']:
                                    logger.warning(f"Honeypot in {event.src_path} was modified!")
                                    ransomware_pid = audit.getAuditRuleReport("pid")
                                    logger.warning(f"Proabable Ransomware process with PID: {ransomware_pid}")
                                    # Software conseguindo para o Ransomware após em média 70.85Mb de arquivos .txt serem criptografados
                                    if ransomware_pid != None:
                                        os.kill(int(ransomware_pid), SIGKILL)
                                        logger.warning(f"Proabable Ransomware process with PID {ransomware_pid} was killed!")

                except Exception as e:
                    logger.error(e)
                    pass

        # Monitorar caso algum diretório seja mudado de lugar, para atualizar o JSON dos honeypots
        def on_moved(self, event):
            logger.debug("Moved " + event.src_path)

        # Monitorar se algum diretório for deletado, para remover as entradas dos mesmos no JSON dos honeypots
        def on_deleted(self, event):
            logger.debug("Deleted " + event.src_path)

    def run(self):
        global observers
        observers = []
        observer = Observer()
        event_handler = self.EventHandler([self.directory_list, self.honeypot_file_name, self.path_to_config_folder, self.json_file_name])

        for directory in self.directory_list:
            # Criação do observer
            observer.schedule(event_handler, directory, recursive=True)
            # Colocando o observer criado na lista dos observers
            observers.append(observer)

        observer.start()

        global json_file_hashes
        json_file_path = os.path.join(self.path_to_config_folder, self.json_file_name)
        if os.path.exists(self.path_to_config_folder):
            try:
                with open(os.path.join(json_file_path)) as json_file:
                    json_file_hashes = json.load(json_file)
            except FileNotFoundError:
                logger.error(f'Could not find {self.json_file_name} in {self.path_to_config_folder}')
                quit()

        try:
            while True:
                continue
        except KeyboardInterrupt:
            for observer in observers:
                observer.unschedule_all()
                observer.stop()
                observer.join()


if __name__ == "__main__":
    from logger import logger
    logging.getLogger("watchdog.observers.inotify_buffer").disabled = True
    fm = FileMonitor(
        directory_list=["/home/matheusheidemann/Documents/Github/Python-Ransomware-Detector/ransomware-samples/encrypt-test"],
        honeypot_file_name=".r4n50mw4r3-d373c70r.txt",
        path_to_config_folder="/home/matheusheidemann/Documents/Github/Python-Ransomware-Detector/software/config",
        json_file_name="ransom-detector-hashes-list.json"
    )
    audit = Audit(
        path_to_audit="/etc/audit",
        path_to_audit_custom_rule_file="/etc/audit/rules.d/ransomware-detector.rules",
        path_to_audit_config="/etc/audit/auditd.conf",
        audit_custom_rules_key="ransomware-detector-key"
    )
    fm.run()
else:
    from software.logger import logger
