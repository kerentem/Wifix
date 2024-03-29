import logging
import uuid
from typing import List, Dict

from flask_bcrypt import generate_password_hash
from utiles import make_db_server_response, HttpStatus, Const
import threading
import requests
from validation import validate_ip

from logger_client import logger

ROUTER_SERVER_URL = "http://192.168.0.100:9285"


class Manager:
    def __init__(self, db_handler):
        self.db_handler = db_handler

    def is_valid_token(self, data) -> bool:
        company_name: str = data["company_name"]
        token: str = data["token"]

        try:
            is_valid_token_response: bool = self.db_handler.is_valid_company_token(
                company_name=company_name, hashed_token=token
            )

            return is_valid_token_response

        except Exception as e:
            error_msg = str(e)
            error_response = make_db_server_response(HttpStatus.OK, "", {}, error_msg)
            return error_response

    def set_new_token(self, data):
        username: str = data["username"]
        password: str = data["password"]
        company_name: str = data["company_name"]
        premium_upload_speed: int = data["premium_upload_speed"]
        premium_download_speed: int = data["premium_download_speed"]
        regular_upload_speed: int = data["regular_upload_speed"]
        regular_download_speed: int = data["regular_download_speed"]

        def is_manager(username: str, password: str):
            return False if username != "wifix" or password != "12345" else True

        if not is_manager(username, password):
            raise Exception("You are not a service manager, please contact BarSe")

        token: str = str(uuid.uuid4())
        hashed_token: str = generate_password_hash(token)

        try:
            self.db_handler.set_company_token(
                company_name=company_name,
                hashed_token=hashed_token,
                premium_upload_speed=premium_upload_speed,
                premium_download_speed=premium_download_speed,
                regular_upload_speed=regular_upload_speed,
                regular_download_speed=regular_download_speed,
            )

            response = make_db_server_response(HttpStatus.OK, "", {"token": token})
            return response

        except Exception as e:
            error_msg = str(e)
            error_response = make_db_server_response(HttpStatus.OK, "", {}, error_msg)
            return error_response

    def update_wifi_speed(self, company: str, is_cron: bool = False):
        clients_ips: Dict[str, Dict[str, int]] = self._get_users_ip(company)
        company_speeds = self.get_company_speeds(company, self.db_handler)

        for ip in clients_ips.keys():
            validate_ip(ip)

        users_ips: List[str] = self.db_handler.get_premium_users(company)

        for client_ip in clients_ips.keys():
            if client_ip in users_ips:
                client_speeds = clients_ips.get("client_ip")
                if client_speeds:
                    if (
                        client_speeds["upload_speed"]
                        != company_speeds.premium_upload_speed
                        or clients_ips["client_ip"]["download_speed"]
                        != company_speeds.premium_download_speed
                    ):
                        self.change_user_speed(
                            ip=client_ip,
                            upload_speed=company_speeds.premium_upload_speed,
                            download_speed=company_speeds.premium_download_speed,
                            is_cron=is_cron,
                            company=company,
                        )
            else:
                self.change_user_speed(
                    ip=client_ip,
                    upload_speed=company_speeds.regular_upload_speed,
                    download_speed=company_speeds.regular_download_speed,
                    is_cron=is_cron,
                    company=company,
                )

        # url = ROUTER_SERVER_URL + "/change_speed"

    @staticmethod
    def change_user_speed(
        ip, upload_speed, download_speed, company: str, is_cron: bool = True
    ):
        def change_speed(url, json):
            try:
                response = requests.post(url, json=json, timeout=10)
                return response
            except Exception as e:
                logging.error(e)

        def limit_speed(routine_url):
            try:
                logger.info("Sending request to routine check")
                requests.get(routine_url)

            except Exception as e:
                logging.error(e)

        def fire_and_forget(url):
            threading.Thread(target=limit_speed, args=(routine_limit_URL,)).start()

        routine_limit_URL = ROUTER_SERVER_URL + "/routine_check"

        if is_cron:
            fire_and_forget(routine_limit_URL)
        else:
            url = ROUTER_SERVER_URL + "/change_speed"
            request = {
                "ip": ip,
                "upload_speed": upload_speed,
                "download_speed": download_speed,
            }

            return change_speed(url, json=request)

    @staticmethod
    def _get_users_ip(company: str) -> Dict[str, Dict[str, int]]:
        # http request to router
        clients_ips: Dict[str, Dict[str, int]] = {
            "192.168.0.100": {"upload_speed": 5, "download_speed": 10},
            "180.168.0.200": {"upload_speed": 5, "download_speed": 10},
        }

        return clients_ips

    @classmethod
    def get_company_speeds(cls, company: str, db_handler):
        response = db_handler.get_company_speeds(company)
        return response

    def get_companies(self) -> List[str]:
        response = self.db_handler.get_companies()
        return response
