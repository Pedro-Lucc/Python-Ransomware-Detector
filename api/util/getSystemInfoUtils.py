# Função para não crashar o programa caso de erro ao pegar o parâmetro user
from __future__ import print_function


def getProcessUser(process_env):
    try:
        return str(process_env['USER'])
    except:
        return None

def getReadWriteSpeed(disk_io_config, operation):
    disk_name = str(disk_io_config['current_disk_name']).split('/')[-1]
    if operation == "rc":
        return disk_io_config['all_disks_io'][disk_name][0]
    elif operation == "wc":
        return disk_io_config['all_disks_io'][disk_name][1]
    elif operation == "rbc":
        return disk_io_config['all_disks_io'][disk_name][2]
    elif operation == "wbc":
        return disk_io_config['all_disks_io'][disk_name][3]
    #psutil.disk_io_counters(perdisk=True, nowrap=False)['sda1'][0]
