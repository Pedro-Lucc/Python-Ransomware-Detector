# IMPORTS
from time import sleep
import psutil
import util.generalUtils as generalUtils
import util.getSystemInfoUtils as getSystemInfoUtils

debug = True

# FUNÇÕES
# Função para pegar todos os processos e seus dados
def getProcessesInfo():
    running_processes_list = []
    for process in psutil.process_iter():
        process_dict = {
            'name': str(process.name()),
            'executable_path': str(process.exe()),
            'pid': str(process.pid),
            'user': getSystemInfoUtils.getProcessUser(process.environ()),
            'status': 1,
            'cpu_usage': int(round(process.cpu_percent() / psutil.cpu_count())),
            'running_on_cpu': str(process.cpu_num()),
            'ram_usage': int(round(process.memory_percent('rss'))),
            'read_count': process.io_counters()[0],
            'write_count': process.io_counters()[1],
            # Talvez usar o children()
            # connections para ver onde o processo está conectado, porta etc
        }

        # Only for debug
        if debug:
            if process.pid == 39737:
                running_processes_list.append(process_dict)
                break
        else:
            running_processes_list.append(process_dict)
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
        # Dicionário para guardar os dados de uso da partição e nome da partição
        disk_io_config = {
            'all_disks_io': psutil.disk_io_counters(perdisk=True, nowrap=False),
            'current_disk_name': partition.device}

        # Dicionário para guardar informações das partições
        partition_dict = {
            'device': str(partition.device),
            'mountpoint': str(partition.mountpoint),
            'fstype': str(partition.fstype),
            'amount': int(psutil.disk_usage(partition.mountpoint).total),
            'usage': int(round(psutil.disk_usage(partition.mountpoint).percent)),
            'read_count': getSystemInfoUtils.getReadWriteSpeed(
                disk_io_config, "rc"),
            'write_count': getSystemInfoUtils.getReadWriteSpeed(
                disk_io_config, "wc"),
            'read_bytes_count': getSystemInfoUtils.getReadWriteSpeed(
                disk_io_config, "rbc"),
            'write_bytes_count': getSystemInfoUtils.getReadWriteSpeed(
                disk_io_config, "wbc")
        }
        partitions_info.append(partition_dict)
    return partitions_info


while True:
    print("RANSOMWARE DETECTOR 0.0.1")
    print("Status: Running")
    print("Mode: Debug\n")
    print(f"> Single Process: {getProcessesInfo()}")
    print(f"> CPU Info: {getCPUInfo()}")
    print(f"> RAM Info: {getRAMInfo()}")
    print(f"> DISK Info: {getDiskInfo()}")
    sleep(0.5)
    generalUtils.clearScreen()

# process IO counters
