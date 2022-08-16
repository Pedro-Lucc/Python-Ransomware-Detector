# IMPORTS
import os
import subprocess
from software.honeypot_generator import HoneypotGenerator
from software.file_monitor import FileMonitor
from software.logger import logger

otp = subprocess.check_output(["locate", "audit/auditd.conf"]).decode()


# CONSTANTS
# SOFTWARE
PATH_TO_MAIN_FOLDER = os.getcwd()
PATH_TO_SOFTWARE_FOLDER = os.path.join(PATH_TO_MAIN_FOLDER, "software")
PATH_TO_CONFIG_FOLDER = os.path.join(PATH_TO_SOFTWARE_FOLDER, "config")

# AUDIT
AUDIT_CUSTOM_RULES_FILE_NAME = "ransomware-detector.rules"
AUDIT_CUSTOM_RULES_KEY = "ransomware-detector-key"
PATH_TO_AUDIT_CONFIG = subprocess.check_output(["locate", "audit/auditd.conf"]).decode()
PATH_TO_AUDIT = os.path.join(PATH_TO_AUDIT_CONFIG.rsplit('/', 1)[0])
PATH_TO_AUDIT_CUSTOM_RULE_FILE = os.path.join(PATH_TO_AUDIT, "rules.d", AUDIT_CUSTOM_RULES_FILE_NAME)

# VARIABLES
paths_to_monitor_or_generate_honeypot = ["/home/matheusheidemann/Documents/Github/Python-Ransomware-Detector/ransomware-samples/encrypt-test"]
honeypot_file_name = ".r4n50mw4r3-d373c70r.txt"
json_file_name = "ransom-detector-hashes-list.json"


# MAIN
logger.debug("Starting Ransomware Detector")

# HONEYPOT GENERATOR
honeypot_generator = HoneypotGenerator(
    directory_list=paths_to_monitor_or_generate_honeypot,
    honeypot_file_name=honeypot_file_name,
    path_to_config_folder=PATH_TO_CONFIG_FOLDER,
    json_file_name=json_file_name,
    # honeypot_interval=2,
    disable_honeypot_interval=True,
    delete=False
)
honeypot_generator.run()

# FILE MONITOR
if not honeypot_generator.delete:
    file_monitor = FileMonitor(
        directory_list=paths_to_monitor_or_generate_honeypot,
        honeypot_file_name=honeypot_file_name,
        path_to_config_folder=PATH_TO_CONFIG_FOLDER,
        json_file_name=json_file_name
    )
    file_monitor.run()
else:
    quit()

# FINISH
logger.debug("Quitting Ransomware Detector")
