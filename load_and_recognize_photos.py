import logging
import grequests
import vk_api_auth
import time
from people_sqlite import PeopleSqlite

# noinspection PyUnresolvedReferences
logging.config.fileConfig('log.ini')
log = logging.getLogger('recognizer')

log.info("starting")
