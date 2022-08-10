# TODO MONITORAR O TAMANHO DOS ARQUIVOS, OS BYTES MODIFICADOS PARA CHECAR SE ESTÃO CRIPTOGRAFADOS, A QUANTIDADE DE MODIFICAÇÕES POR SEGUNDO (SE É SUSPEITA), A EXTENSÃO DO ARQUIVO, FAZER UM BACKUP DO ARQUIVO ANTES DELE SER MODIFICADO

import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


# Classe FileSystemModifications, que herda a classe FileSystemEventHandler do watchdog
# event.src_path é basicamente o caminho que o handler retorna
class FileSystemModifications(FileSystemEventHandler):
    def on_create(self, event):
        print("Created: " + event.src_path)
        print("\n" + str(event))

    def on_deleted(self, event):
        print("Deleted: " + event.src_path)
        print("\n" + str(event))

    def on_modified(self, event):
        print("Modified: " + event.src_path)
        print("\n" + str(event))

    def on_moved(self, event):
        print("Moved or Renamed: " + event.src_path)
        print("\n" + str(event))


if __name__ == "__main__":
    # Os caminhos que serão monitorados pelo WatchDog Observer
    paths_to_monitor = ["/home/matheusheidemann/Documents/Python Files/Python-Ransomware-Detector/ransomware-samples/encrypt-test/"]
    # Lista que conterá todos os Observers ativos
    observers = []

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

    # Rodar o monitoramento dos observers definidos
    try:
        while True:
            # Será feito um scan a cada 1 segundos
            time.sleep(1)
    # Caso o usuário interrompa o funcionamento, todos os observer serão finalizados
    except KeyboardInterrupt:
        for observer in observers:
            observer.unschedule_all()
            observer.stop()
            observer.join()
