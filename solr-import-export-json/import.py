import logging.config
import os

logger = logging.getLogger()


def solr_import():
    logger.info("Importing")


if __name__ == '__main__':
    ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    CONFIG_PATH = os.path.join(ROOT_DIR, 'logging.conf')
    logging.config.fileConfig(CONFIG_PATH)
    solr_import()
