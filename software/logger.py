import logging

#logging.basicConfig(level=logging.DEBUG, format='[%(name)s] [%(levelname)s] %(filename)s %(lineno)d ---- %(message)s')
logging.basicConfig(level=logging.DEBUG, format='[%(name)s] [%(levelname)s] ---- %(message)s')
logger = logging.getLogger("ransomware-detector-logger")
