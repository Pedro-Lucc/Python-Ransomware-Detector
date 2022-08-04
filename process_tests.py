# IMPORTS
from time import sleep
import psutil
import util


# FUNÇÕES
# Função para pegar todos os processos e seus dados
def getProcessesInfo():
    running_processes_list = []
    for process in psutil.process_iter():
        process_dict = {
            'name': str(process.name()),
            'pid': str(process.pid),
            'user': util.getProcessUser(process.environ()),
            'status': 1,
            'cpu_usafe': int(round(process.cpu_percent() / psutil.cpu_count())),
            'ram_usage': int(round(process.memory_percent('rss'))),
            'read_count': process.io_counters()[0],
            'write_count': process.io_counters()[1]
            }

        # Only for debug
        if process.pid == 4293:
            running_processes_list.append(process_dict)
            break

        # running_processes_list.append(process_dict)
    return running_processes_list
        

# Função para pegar as informações da CPU
def getCPUInfo():
    return [{
        'count': str(psutil.cpu_count()),
        'usage': int(round(psutil.cpu_percent()))
    }]


# Função para pegar as informações da RAM
def getRAMInfo():
    return [{
        'amount': str((psutil.virtual_memory().total)),
        'usage': int(round(psutil.virtual_memory().percent))
    }]


# Função para pegar as informações das partições no disco
def getDiskInfo():
    partitions_info = []
    for partition in psutil.disk_partitions():
        partition_dict = {
            'device': str(partition.device),
            'mountpoint': str(partition.mountpoint),
            'fstype': str(partition.fstype),
            'amount': int(psutil.disk_usage(partition.mountpoint).total),
            'usage': int(round(psutil.disk_usage(partition.mountpoint).percent))
            }
        partitions_info.append(partition_dict)
    
    return partitions_info
    
while True:
    print(getProcessesInfo())
    sleep(0.5)
    util.clearScreen()

# process IO counters