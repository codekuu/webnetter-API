import logging

logger = logging.getLogger("webnetter")
hdlr = logging.FileHandler("webnetter.log")
formatter = logging.Formatter("%(asctime)s:%(levelname)s:%(message)s")
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.INFO)
