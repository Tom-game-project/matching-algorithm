import logging

logging.basicConfig(level=logging.DEBUG,format='%(asctime)s - %(levelname)s - %(message)s')

logging.debug(["hello","world"])
logging.debug(
    "hello world"
)