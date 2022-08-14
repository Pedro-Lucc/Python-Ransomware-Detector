# TODO MONITORAR O TAMANHO DOS ARQUIVOS, OS BYTES MODIFICADOS PARA CHECAR SE ESTÃO CRIPTOGRAFADOS, A QUANTIDADE DE MODIFICAÇÕES POR SEGUNDO (SE É SUSPEITA), A EXTENSÃO DO ARQUIVO, FAZER UM BACKUP DO ARQUIVO ANTES DELE SER MODIFICADO

import hashlib
import json
import os
import signal
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import logging


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

        def on_modified(self, event):
            if self.honeypot_file_name in event.src_path:
                try:
                    pids_in_honeypot = subprocess.check_output(["fuser", "-u", event.src_path], stderr=subprocess.DEVNULL).decode().strip().replace(" ", ",").split(",")
                    for dict in json_file_hashes:
                        if event.src_path == dict['absolute_path']:
                            with open(event.src_path, 'rb') as honeypot_file:
                                file_data = honeypot_file.read()
                                current_hash = hashlib.md5(file_data).hexdigest()
                                if current_hash != dict['hash']:
                                    logger.debug(f"Honeypot in {event.src_path} was modified!")
                                    try:
                                        file_monitor_pid = os.getpid()
                                        for pid in pids_in_honeypot:
                                            if str(pid) != str(file_monitor_pid):
                                                logger.debug(f"The Ransomware process PID is: {pid}")
                                                #os.kill(int(pid), signal.SIGKILL)
                                                logger.debug(f"Ransomware with process PID {pid} was killed!")
                                    except Exception as e:
                                        logger.error(f'{str(e.__class__.__name__)}')
                                        continue
                except Exception as e:
                    logger.error("The fuser command returned nothing.")
                    pass

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
    fm.run()
else:
    from software.logger import logger
