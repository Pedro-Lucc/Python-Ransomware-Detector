# A INICIALIZAÇÃO DO PROGRAMA VAI AQUI
import os
from software.honeypot_generator import HoneypotGenerator
from software.logger import logger

# CONSTANTES
PATH_TO_MAIN_FOLDER = os.getcwd()
PATH_TO_SOFTWARE_FOLDER = os.path.join(PATH_TO_MAIN_FOLDER, "software")
PATH_TO_CONFIG_FOLDER = os.path.join(PATH_TO_SOFTWARE_FOLDER, "config")
PATHS_TO_MONITOR_OR_GENERATE_HONEYPOT = ["/home/matheusheidemann/Documents/Github/Python-Ransomware-Detector/ransomware-samples/encrypt-test"]
HONEYPOT_FILE_NAME = ".r4n50mw4r3-d373c70r.txt"
JSON_FILE_NAME = "ransom-detector-hashes-list.json"
PATH_TO_JSON_FILE = os.path.join(PATH_TO_CONFIG_FOLDER, JSON_FILE_NAME)

logger.debug("Starting Ransomware Detector")
# SOFTWARE
honeypot_generator = HoneypotGenerator(
    directory_list=PATHS_TO_MONITOR_OR_GENERATE_HONEYPOT,
    honeypot_file_name=HONEYPOT_FILE_NAME,
    path_to_config_folder=PATH_TO_CONFIG_FOLDER,
    json_file_name=JSON_FILE_NAME,
    # honeypot_interval=2,
    disable_honeypot_interval=True,
    delete=True
)
honeypot_generator.run()
logger.debug("Quitting Ransomware Detector")
