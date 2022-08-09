#
#
#
#
# ARQUIVO APENAS PARA TESTES!!!!! NÃO ESTÁ SENDO UTILIZADO PARA NADA
#
#
#
#
from curses.ascii import isdigit
import os

pid_list = []
for filename in os.listdir("/proc/"):
    if filename.isdigit():
        pid_list.append(str(filename))

for pid in pid_list:
    with open(f'/proc/{pid}/status') as reader:
        proc_pid_status_output = reader.read()


# PEGAR TODOS OS USUÁRIOS DO SISTEMA E SEUS UIDS
# Variável que terá os nomes de todos os usuário (é pego do arquivo passwd)
usernames_username_list = []
# Variável que terá os IDs de cada usuário
usernames_uid_list = []

# Lendo o arquivo passwd para pegar todos os nomes de usuários e os UIDs respectivos
with open("/etc/passwd") as reader:
    # A variável abaixo irá fazer uma lista com cada linha do arquivo passwd
    etc_passwd_lines = reader.read().strip().split("\n")
    print(etc_passwd_lines)
for line in etc_passwd_lines:
    # Dividindo o output
    line_splitted = line.split(":", 3)
    # Pegando somente a primeira parte do output (que contém o nome do usuário)
    usernames_username_list.append(line_splitted[0])
    # Pegando somente a terceira parte do output (que contém o UID do usuário)
    usernames_uid_list.append(line_splitted[2])

# Pegar o nome do usuário atual
current_user_name = os.environ.get('USER')
print(current_user_name)
