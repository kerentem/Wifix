import threading
import time
from typing import List

from endpoints.manager_endpoints.endpoints import Manager
from logger_client import logger


def _create_update_speed_thread(manager: Manager):
    while True:
        companies: List[str] = manager.get_companies()
        for company in companies:
            logger.info(f"Cron - updating wifi speeds for company: {company}")
            manager.update_wifi_speed(company)

        time.sleep(300)


def init_update_speed_thread(manager: Manager):
    http_thread = threading.Thread(target=_create_update_speed_thread, args=(manager,))
    http_thread.start()
