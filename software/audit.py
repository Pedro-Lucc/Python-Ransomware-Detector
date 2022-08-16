# TODO
# Checar se o audit está instalado e ligado
# Ligar e configurar o audit
# As regras do AUDIT devem ser criadas/modificadas toda vez que:
# - Forem criados novos honeypots pela primeira vez
# - Um diretório for movido para outro lugar, atualizando o JSON e as regras consequentemente
# - Um diretório for deletado, atualizando o JSON e as regras consequentemente
# As regras do AUDIT devem ir para o arquivo de regras separado
# As regras devem conter a keyword "ransomware-detector-key"
# É necessário configurar o arquivo de log para que possa salvar os PIDs se um ransomware agir
# É necessário ter um caminho definido para o arquivo que conterá as regras personalizadas

from datetime import datetime
import os
import subprocess
import hashlib
import re
import time


def createAuditRule(path_to_custom_rule_file, path_to_honeypot_file, audit_custom_rules_key):
    with open(path_to_custom_rule_file, "a") as custom_rule_file:
        custom_rule_file.write(f'-w "{path_to_honeypot_file}" -p wa -k {audit_custom_rules_key}\n')


def createCustomRuleFile(path_to_custom_rule_file):
    with open(path_to_custom_rule_file, "w") as custom_rule_file:
        custom_rule_file.write("-D\n")


def loadRules(path_to_custom_rule_file):
    with open(path_to_custom_rule_file) as custom_rule_file:
        for rule in custom_rule_file:
            os.system("auditctl " + rule)


def checkForDuplicateRules(path_to_custom_rule_file):
    temp_file_path = os.path.join(path_to_custom_rule_file, "custom")

    completed_lines_hash = set()

    temp_file = open(temp_file_path, "w")

    for line in open(path_to_custom_rule_file, "r"):
        hashValue = hashlib.md5(line.rstrip().encode('utf-8')).hexdigest()
        if hashValue not in completed_lines_hash:
            temp_file.write(line)
            completed_lines_hash.add(hashValue)
    temp_file.close()

# pegar o caminho
# pegar o type
# pegar o ID
# pegar o tempo


def getAuditRuleReport(fm_honeypot_file_path, action):
    last_honeypot_file_event = subprocess.check_output(["ausearch", "-k", "ransomware-detector-key"], stderr=subprocess.DEVNULL).decode().rstrip().split("----")[-1:]
    try:
        ppid, pid = re.findall(ppid_pid_pattern, last_honeypot_file_event[0])
        if action == "pid":
            return pid
        elif action == "ppid":
            return ppid
        elif action == "ppid-pid":
            return ppid, pid
    except Exception as e:
        print(e)

    # fm_event_time_as_unix = time.mktime(fm_event_time.timetuple())
    # for honeypot_file_event in honeypot_file_event_list:
    #     event_times = re.search(time_pattern, honeypot_file_event).group()
    #     for event_time in event_times:
    #         print()


ppid_pid_pattern = "(?<=pid=)(.*?)(?=\ )"
time_and_id_pattern = "(?<=msg=audit\()(.*)(?=\):)"
time_pattern = "(?<=msg=audit\()(.*)(?=:\d)"
type_pattern = "(?<=type=)(.*?)(?= )"
path_pattern = '(?<=name=")(.*?)(?=" )'
if __name__ == "__main__":
    # createCustomRuleFile("/etc/audit/rules.d/ransomware-detector.rules")
    loadRules("/etc/audit/rules.d/ransomware-detector.rules")

# [0].split(":")[1] - get only ID
