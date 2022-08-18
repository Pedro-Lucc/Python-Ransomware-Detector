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

import os
import subprocess
import re
from time import sleep


class Audit:
    def __init__(self, path_to_audit, path_to_audit_custom_rule_file, path_to_audit_config, audit_custom_rules_key):
        self.path_to_audit = path_to_audit
        self.path_to_custom_rule_file = path_to_audit_custom_rule_file
        self.path_to_audit_config = path_to_audit_config
        self.audit_custom_rules_key = audit_custom_rules_key

    def setStatus(self, action):
        """Função para ligar ou desligar o serviço de auditoria"""
        output = subprocess.run(['service', 'auditd', 'status'],  capture_output=True, text=True)
        tries = 0
        if not "could not be found" in str(output):
            if action == "on":
                while True and tries < 5:
                    if re.findall("(?<=Active: )(.*?)(?=\ )", str(output))[0] == "active":
                        logger.debug("Auditd Service is currently active")
                        break
                    else:
                        logger.debug("Auditd Service is currently inactive")
                        logger.debug("Turning Auditd service on...")
                        subprocess.run(['service', 'auditd', 'start'])
                        sleep(3)
                        output = subprocess.run(['service', 'auditd', 'status'],  capture_output=True, text=True)
                        tries += 1
            elif action == "off":
                if re.findall("(?<=Active: )(.*?)(?=\ )", str(output))[0] == "inactive":
                    logger.error("Can't turn Auditd Service off. The service is already inactive")
                else:
                    logger.debug("Turning Auditd service off...")
                    subprocess.run(['service', 'auditd', 'stop'])
        else:
            logger.debug("Could not find Auditd service. Do you have Auditd installed?")

    def createCustomRuleFile(self):
        """Função para criar o arquivo que terá as regras para cada honeypot"""
        if os.path.exists(self.path_to_custom_rule_file):
            os.remove(self.path_to_custom_rule_file)

        with open(self.path_to_custom_rule_file, "w") as custom_rule_file:
            custom_rule_file.write("-D\n")

    def deleteCustomRuleFileAndRules(self):
        """Função para criar o arquivo que terá as regras para cada honeypot"""
        if os.path.exists(self.path_to_custom_rule_file):
            os.remove(self.path_to_custom_rule_file)
        else:
            logger.error("There is not custom rule file in the directory.")
            subprocess.run(["auditctl", "-D"], capture_output=False)

    def createAuditRule(self, path_to_honeypot_file):
        """"""
        with open(self.path_to_custom_rule_file, "a") as custom_rule_file:
            custom_rule_file.write(f'-w "{path_to_honeypot_file}" -p wa -k {self.audit_custom_rules_key}\n')

    def loadRules(self):
        """Função para carregar as regras personalizadas criadas"""
        with open(self.path_to_custom_rule_file) as custom_rule_file:
            for rule in custom_rule_file:
                os.system("auditctl " + rule)
                #subprocess.run(['auditctl', rule], shell=True, capture_output=False)

    def getAuditRuleReport(self, action):
        """Função para pegar os reports associados a key do Ransomware e retornar alguma informação"""
        last_honeypot_file_event = subprocess.check_output(["ausearch", "-k", "ransomware-detector-key"], stderr=subprocess.DEVNULL).decode().rstrip().split("----")[-1:]
        ppid_pid_pattern = "(?<=pid=)(.*?)(?=\ )"
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


# MAIN
if __name__ == "__main__":
    from logger import logger
    # VAR
    ppid_pid_pattern = "(?<=pid=)(.*?)(?=\ )"
    time_and_id_pattern = "(?<=msg=audit\()(.*)(?=\):)"
    time_pattern = "(?<=msg=audit\()(.*)(?=:\d)"
    type_pattern = "(?<=type=)(.*?)(?= )"
    path_pattern = '(?<=name=")(.*?)(?=" )'
    service_active_pattern = "(?<=Active: )(.*?)(?=\ )"
    AUDIT_CUSTOM_RULES_FILE_NAME = "ransomware-detector.rules"
    AUDIT_CUSTOM_RULES_KEY = "ransomware-detector-key"
    PATH_TO_AUDIT_CONFIG = subprocess.check_output(["locate", "audit/auditd.conf"]).decode()
    PATH_TO_AUDIT = os.path.join(PATH_TO_AUDIT_CONFIG.rsplit('/', 1)[0])
    PATH_TO_AUDIT_CUSTOM_RULE_FILE = os.path.join(PATH_TO_AUDIT, "rules.d", AUDIT_CUSTOM_RULES_FILE_NAME)

    # SOFTWARE
    # createCustomRuleFile("/etc/audit/rules.d/ransomware-detector.rules")
    audit = Audit(
        path_to_audit=PATH_TO_AUDIT,
        path_to_audit_custom_rule_file=PATH_TO_AUDIT_CUSTOM_RULE_FILE,
        path_to_audit_config=PATH_TO_AUDIT_CONFIG,
        audit_custom_rules_key=AUDIT_CUSTOM_RULES_KEY
    )
    audit.setStatus("on")
else:
    from software.logger import logger

# [0].split(":")[1] - get only ID
