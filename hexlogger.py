import logging

logging.basicConfig(format="%(asctime)s.%(msecs)d %(levelname)s [%(name)s %(module)s:%(lineno)s] %(message)s", datefmt="%Y-%m-%d %H:%M:%S", level=logging.INFO)
logger = logging.getLogger("rest-json-logger")