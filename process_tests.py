# IMPORTS
from telnetlib import STATUS
from time import sleep
import psutil
import util


# FUNÇÕES
# Função para printar os processos
while True:
    for process in psutil.process_iter():
        if "Web Content" in str(process.name) and process.pid == 45425:
            print(f"Process: {process.name()}")
            print(f"PID: {process.pid}")
            print(f"Status: {process.status()}")
            print(f"User: {process.environ()['USER']}")
            print(f"CPU usage: {round(process.cpu_percent() / psutil.cpu_count())}%")
            print(f"RAM usage: {round(process.memory_percent('rss'))}%")
    sleep(1)
    util.clearScreen()