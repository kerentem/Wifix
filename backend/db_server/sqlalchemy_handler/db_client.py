from typing import Optional, Dict, List

from logger_client import logger

from flask_bcrypt import check_password_hash
from sqlalchemy import func, QueuePool, create_engine, text, Row, update
from sqlalchemy.exc import NoResultFound, IntegrityError
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql._typing import _TP

from sqlalchemy_handler.db_models import (
    Base,
    User,
    Admin,
    WifiSession,
    CreditCard,
    Payment,
    Company,
    UserCompany,
)
import datetime


class DBHandler:
    def __init__(
        self,
        rds_username: str,
        rds_password: str,
        rds_endpoint: str,
        database: str,
        rds_port: int,
    ):

        url = f"mysql+pymysql://{rds_username}:{rds_password}@{rds_endpoint}:{rds_port}/{database}"

        self.engine = create_engine(
            url, poolclass=QueuePool, pool_size=10, max_overflow=20
        )

        self.Session = sessionmaker(bind=self.engine)

    def get_session(self):
        return self.Session()

    def create_all(self):
        logger.info("Creating tables (if not exist)")
        Base.metadata.create_all(self.engine)

    def drop_all(self):
        logger.info("Dropping tables")
        Base.metadata.drop_all(self.engine)

    def create_events(self):
        logger.info("Creating wifi_session_cleanup event")
        with self.engine.connect() as conn:
            try:
                query = text(
                    "CREATE EVENT IF NOT EXISTS wifi_session_cleanup "
                    "ON SCHEDULE "
                    "EVERY 1 MINUTE "
                    "DO "
                    "DELETE FROM wifi_sessions "
                    "WHERE end_time < UNIX_TIMESTAMP(NOW())"
                )
                conn.execute(query)
            except Exception as error:
                raise Exception(
                    f"Error while creating MySQL event,\n" f"Error: {error}"
                )

    def is_email_registered(self, email: str, is_admin: bool) -> bool:
        session = self.get_session()
        user = None

        if is_admin:
            user = session.query(Admin).filter_by(email=email).first()
        else:
            user = session.query(User).filter_by(email=email).first()

        return user is not None

    def register(
        self,
        full_name: str,
        email: str,
        hashed_password: str,
        ip: Optional[str] = None,
        company_name: Optional[str] = None,
        is_admin: bool = False,
    ):
        session = self.get_session()

        if is_admin:
            user = Admin(
                full_name=full_name, email=email, hashed_password=hashed_password
            )
        else:
            user = User(
                full_name=full_name, email=email, hashed_password=hashed_password, ip=ip
            )

        session.add(user)
        try:
            session.commit()

            if not is_admin:
                user_company = UserCompany(email=email, company_name=company_name)
                session.add(user_company)
                session.commit()

        except Exception as error:
            session.rollback()

            if vars(error).get("orig"):
                raise Exception(vars(error).get("orig"))
            else:
                raise error

    def is_user_registered(
        self,
        email: str,
        password: str,
        company_name: Optional[str] = None,
        is_admin: bool = False,
    ) -> bool:
        session = self.get_session()
        is_valid_company = True

        if is_admin:
            user = session.query(Admin).filter_by(email=email).first()
        else:
            user = session.query(User).filter_by(email=email).first()
            is_valid_company = (
                session.query(UserCompany).filter_by(company_name=company_name).first()
            )

        if not user or not is_valid_company:
            return False

        return check_password_hash(user.hashed_password, password)

    def set_user_ip(self, email: str, user_ip: str):
        session = self.get_session()
        user = session.query(User).filter_by(email=email).first()

        if user and user.ip != user_ip:
            logger.info(
                f"Updating ip for user: {email}, old_ip: {user.ip}, new_ip: {user_ip}"
            )
            user.ip = user_ip
            session.commit()

    def add_credit_card(
        self, card_number, expiration_month, expiration_year, hashed_cvv, email
    ):
        session = self.get_session()
        user = session.query(User).filter_by(email=email).first()
        if not user:
            raise InvalidUsernameException(f"Hi {email},\nPlease register first.")
        credit_card = CreditCard(
            email=email,
            card_number=card_number,
            expiration_month=expiration_month,
            expiration_year=expiration_year,
            hashed_cvv=hashed_cvv,
        )
        session.add(credit_card)
        try:
            session.commit()

        except Exception as error:
            session.rollback()

            if vars(error).get("orig"):
                raise Exception(vars(error).get("orig"))
            else:
                raise error

    def get_wifi_session_expired(
        self, email: str, company_name: str
    ) -> Optional[Row[_TP]]:
        session = self.get_session()
        result = (
            session.query(WifiSession)
            .filter_by(email=email, company_name=company_name)
            .first()
        )
        return result

    def is_wifi_session_expired(self, email: str, company_name: str) -> bool:
        is_expired: bool = self.get_wifi_session_expired(email, company_name) is None
        return is_expired

    def start_wifi_session(
        self,
        email: str,
        start_time: float,
        end_time: float,
        data_usage: int,
        company_name: str,
    ):
        session = self.get_session()

        try:
            wifi_session = WifiSession(
                email=email,
                start_time=start_time,
                end_time=end_time,
                data_usage=data_usage,
                company_name=company_name,
            )
            session.add(wifi_session)
            session.commit()

        except NoResultFound:
            session.rollback()
            logger.error(f"Error starting WiFi session. User {email} does not exist.")
            raise InvalidUsernameException(f"Hi {email},\nPlease register first.")

        except Exception as error:
            session.rollback()
            logger.error(f"Error starting WiFi session. Error: {error}")

            if vars(error).get("orig"):
                raise Exception(vars(error).get("orig"))
            else:
                raise error

    def remove_wifi_session(
        self, email: str, start_time: int, end_time: int, company_name: str
    ):
        session = self.get_session()
        try:
            session.query(WifiSession).filter_by(
                email=email,
                start_time=start_time,
                end_time=end_time,
                company_name=company_name,
            ).delete()
            session.commit()

        except NoResultFound:
            session.rollback()
            logger.error(f"Error removing WiFi session. User {email} does not exist.")
            raise InvalidUsernameException(f"Hi {email},\nPlease register first.")

        except Exception as error:
            session.rollback()
            logger.error(f"Error removing WiFi session. Error: {error}")

            if vars(error).get("orig"):
                raise Exception(vars(error).get("orig"))
            else:
                raise error

    def insert_payment(self, email: str, price: int):
        created_at = datetime.datetime.now().timestamp()
        session = self.Session()
        try:
            payment = Payment(email=email, price=price, created_at=created_at)
            session.add(payment)
            session.commit()
        except Exception as error:
            session.rollback()
            logger.error(f"Error while adding payment with MySQL, error: {error}")
            raise InvalidUsernameException(f"Hi {email},\nPlease register first.")
        finally:
            session.close()

    def get_current_balance(
        self, from_date_timestamp: float, to_date_timestamp: float
    ) -> int:
        session = self.Session()
        try:
            balance = (
                session.query(func.sum(Payment.price))
                .filter(
                    Payment.created_at >= from_date_timestamp,
                    Payment.created_at <= to_date_timestamp,
                )
                .scalar()
            )
            return int(balance) if balance else 0
        except Exception as error:
            logger.error(
                f"Error while getting admin balance with MySQL,\n" f"Error: {error}"
            )

            if vars(error).get("orig"):
                raise Exception(vars(error).get("orig"))
            else:
                raise error

        finally:
            session.close()

    def is_valid_company_token(self, company_name: str, hashed_token: str) -> bool:
        session = self.get_session()

        company_token = (
            session.query(Company)
            .filter_by(company_name=company_name)
            .with_entities(Company.hashed_token)
            .one_or_none()
        )

        if company_token:
            return check_password_hash(company_token[0], hashed_token)

        else:
            return False

    def set_company_token(
        self,
        company_name: str,
        hashed_token: str,
        premium_upload_speed: int,
        premium_download_speed: int,
        regular_upload_speed: int,
        regular_download_speed: int,
    ):
        session = self.get_session()
        try:
            company_token = Company(
                company_name=company_name,
                hashed_token=hashed_token,
                premium_upload_speed=premium_upload_speed,
                premium_download_speed=premium_download_speed,
                regular_upload_speed=regular_upload_speed,
                regular_download_speed=regular_download_speed,
            )
            session.add(company_token)
            session.commit()

        except IntegrityError as error:
            session.rollback()
            raise Exception(
                f"Error while creating a new token for the company with MySQL,\n"
                f"Error: {error}"
            )

        except Exception as error:
            session.rollback()
            if vars(error).get("orig"):
                raise Exception(vars(error).get("orig"))
            else:
                raise error

    def get_company_speeds(self, company: str) -> Optional[Row[_TP]]:
        session = self.get_session()
        result = session.query(Company).filter_by(company_name=company).first()
        return result

    def get_premium_users(self, company: str) -> List[str]:
        session = self.get_session()
        users_ips = (
            session.query(User.ip)
            .join(
                WifiSession,
                (User.email == WifiSession.email)
                & (WifiSession.company_name == company),
            )
            .distinct()
            .all()
        )

        # Extract the IPs from the result
        users_ips = [user_ip[0] for user_ip in users_ips]

        return users_ips

    def get_companies(self):
        session = self.get_session()

        companies = session.query(Company.company_name).all()

        company_names = [company.company_name for company in companies]

        return company_names
