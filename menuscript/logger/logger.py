# menuscript/logger/logger.py

import logging
from resources import paths as paths
import pathlib

global _log
_log = logging.getLogger("log")

def init():
    _log.setLevel(logging.INFO)
        
    for handler in logging.root.handlers:
        logging.root.removeHandler(handler)

    fh = logging.FileHandler(pathlib.Path(paths.user_data_path).joinpath("app.log"))
    ch = logging.StreamHandler()

    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    ch.setFormatter(formatter)
    fh.setFormatter(formatter)

    logging.Logger.addHandler(_log, ch)
    logging.Logger.addHandler(_log, fh)