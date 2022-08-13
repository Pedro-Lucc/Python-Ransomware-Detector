# TODO MONITORAR O TAMANHO DOS ARQUIVOS, OS BYTES MODIFICADOS PARA CHECAR SE ESTÃO CRIPTOGRAFADOS, A QUANTIDADE DE MODIFICAÇÕES POR SEGUNDO (SE É SUSPEITA), A EXTENSÃO DO ARQUIVO, FAZER UM BACKUP DO ARQUIVO ANTES DELE SER MODIFICADO

import hashlib
import json
import os
import signal
import subprocess
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


# Classe FileSystemModifications, que herda a classe FileSystemEventHandler do watchdog
# event.src_path é basicamente o caminho que o handler retorna
class FileSystemModifications(FileSystemEventHandler):

    def on_modified(self, event):
        if honeypot_file_name in event.src_path:
            try:
                pids_in_honeypot = subprocess.check_output(["fuser", "-u", event.src_path]).decode().strip().replace(" ", ",").split(",")
                for dict in hashes_json:
                    if event.src_path == dict['absolute_path']:
                        with open(event.src_path, 'rb') as honeypot_file:
                            file_data = honeypot_file.read()  # read file as bytes
                            current_hash = hashlib.md5(file_data).hexdigest()
                            if current_hash != dict['hash']:
                                print(f"Honeypot in {event.src_path} was modified!")
                                try:
                                    file_monitor_pid = os.getpid()
                                    print(pids_in_honeypot)
                                    for pid in pids_in_honeypot:
                                        if str(pid) != str(file_monitor_pid):
                                            print("\nThe Ransomware process PID is: " + pid + "\n")
                                            #os.kill(int(pid), signal.SIGKILL)
                                except Exception as e:
                                    print(f'[-] ERROR --- {str(e.__class__.__name__)}')
                                    continue
            except Exception as e:
                print(e)


if __name__ == "__main__":
    # Os caminhos que serão monitorados pelo WatchDog Observer
    paths_to_monitor = ["/home/matheusheidemann/Documents/Github/Python-Ransomware-Detector/ransomware-samples/encrypt-test"]
    # Lista que conterá todos os Observers ativos
    observers = []

    # honeypot name
    honeypot_file_name = ".r4n50mw4r3-d373c70r.txt"

    # Criando uma variável para iniciar cada classe
    observer = Observer()
    event_handler = FileSystemModifications()

    # Criar um observer que receberá o handler "FileSystemModifications" e o caminho atual do loop
    for path in paths_to_monitor:
        # Criação do observer
        observer.schedule(event_handler, path, recursive=True)
        # Colocando o observer criado na lista dos observers
        observers.append(observer)

    # Iniciar o observer
    observer.start()

    # PRINT JSON
    with open('/home/matheusheidemann/Documents/Github/Python-Ransomware-Detector/test/ransom-detector-hashes-list.json') as a:
        hashes_json = json.load(a)

    # Rodar o monitoramento dos observers definidos
    try:
        while True:
            # Será feito um scan a cada 1 segundos
            continue
    # Caso o usuário interrompa o funcionamento, todos os observer serão finalizados
    except KeyboardInterrupt:
        for observer in observers:
            observer.unschedule_all()
            observer.stop()
            observer.join()
