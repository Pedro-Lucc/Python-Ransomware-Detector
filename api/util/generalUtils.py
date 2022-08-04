# IMPORTS
from os import name, system


# FUNÇÕES PARA AUXILIAR
# Função para limpar a tela
def clearScreen():
    # Windows NT
    if name == "nt":
        system("cls")
    # Mac/Linux
    else:
        system("clear")


# Função para converter bytes em números com unidades mais legíveis
def humanbytes(B, unit):
    B = float(B)
    KB = float(1024)
    MB = float(KB ** 2)
    GB = float(KB ** 3)
    TB = float(KB ** 4)
    if unit == "KB":
        return '{0} {1}'.format(B, 'Bytes' if 0 == B > 1 else 'Byte')
    elif unit == "KB":
        return '{0:.2f} KB'.format(B / KB)
    elif unit == "MB":
        return '{0:.2f} MB'.format(B / MB)
    elif unit == "GB":
        return '{0:.2f} GB'.format(B / GB)
    elif unit == "TB":
        return '{0:.2f} TB'.format(B / TB)


# teste = {
#     'sr0': sdiskio(
#         read_count=27,
#         write_count=0,
#         read_bytes=1073152,
#         write_bytes=0, read_time=608,
#         write_time=0, read_merged_count=0,
#         write_merged_count=0,
#         busy_time=612),

#     'sda': sdiskio(
#         read_count=128547,
#         write_count=80251,
#         read_bytes=2964126720,
#         write_bytes=2664091648,
#         read_time=355197,
#         write_time=56478,
#         read_merged_count=86994,
#         write_merged_count=395934,
#         busy_time=225004)}
