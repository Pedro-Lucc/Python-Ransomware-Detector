# A INICIALIZAÇÃO DO PROGRAMA VAI AQUI
import os
from software.honeypot_generator import HoneypotGenerator
from software.logger import logger

# VARIABLES
PATH_TO_MAIN_FOLDER = os.getcwd()
PATH_TO_SOFTWARE_FOLDER = os.path.join(PATH_TO_MAIN_FOLDER, "software")
PATH_TO_CONFIG_FOLDER = os.path.join(PATH_TO_SOFTWARE_FOLDER, "config")
paths_to_monitor_or_generate_honeypot = ["/home/matheusheidemann/Documents/Github/Python-Ransomware-Detector/ransomware-samples/encrypt-test"]
honeypot_file_name = ".r4n50mw4r3-d373c70r.txt"
json_file_name = "ransom-detector-hashes-list.json"
PATH_TO_JSON_FILE = os.path.join(PATH_TO_CONFIG_FOLDER, json_file_name)

logger.debug("Starting Ransomware Detector")
# SOFTWARE
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
logger.debug("Quitting Ransomware Detector")
