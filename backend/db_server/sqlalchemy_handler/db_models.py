from sqlalchemy import (
    Column,
    Integer,
    String,
    TIMESTAMP,
    ForeignKey,
    BigInteger,
    text,
)
from sqlalchemy.event import listens_for
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    email = Column(String(100), nullable=False, primary_key=True)
    full_name = Column(String(100), nullable=False)
    hashed_password = Column(String(128), nullable=False)
    created_at = Column(TIMESTAMP, server_default=text("NOW()"))
    ip = Column(String(15), nullable=False)


class Admin(Base):
    __tablename__ = "admins"
    email = Column(String(100), nullable=False, primary_key=True)
    full_name = Column(String(100), nullable=False)
    hashed_password = Column(String(128), nullable=False)
    created_at = Column(TIMESTAMP, server_default=text("NOW()"))


class CreditCard(Base):
    __tablename__ = "credit_cards"
    email = Column(
        String(255), ForeignKey("users.email"), nullable=False, primary_key=True
    )
    card_number = Column(String(16), nullable=False)
    expiration_month = Column(String(2), nullable=False)
    expiration_year = Column(String(4), nullable=False)
    hashed_cvv = Column(String(255), nullable=False)


class Payment(Base):
    __tablename__ = "payments"
    id = Column(Integer, primary_key=True)

    email = Column(String(255), ForeignKey("users.email"), nullable=False)
    price = Column(Integer, nullable=False)
    created_at = Column(BigInteger, nullable=False)


class Company(Base):
    __tablename__ = "companies"
    company_name = Column(String(255), primary_key=True, nullable=False)
    hashed_token = Column(String(255), nullable=False)
    premium_upload_speed = Column(Integer, nullable=False)
    premium_download_speed = Column(Integer, nullable=False)
    regular_upload_speed = Column(Integer, nullable=False)
    regular_download_speed = Column(Integer, nullable=False)


class UserCompany(Base):
    __tablename__ = "user_companies"
    id = Column(Integer, primary_key=True)
    company_name = Column(
        String(255), ForeignKey("companies.company_name"), nullable=False
    )
    email = Column(String(255), ForeignKey("users.email"), nullable=False)


class WifiSession(Base):
    __tablename__ = "wifi_sessions"
    email = Column(
        String(255), ForeignKey("users.email"), nullable=False, primary_key=True
    )
    start_time = Column(Integer, nullable=False)
    end_time = Column(Integer, nullable=False)
    data_usage = Column(Integer, nullable=False)
    company_name = Column(
        String(255), ForeignKey("user_companies.company_name"), nullable=False
    )


class WifiSessionHistory(Base):
    __tablename__ = "wifi_sessions_history"
    id = Column(Integer, primary_key=True)
    email = Column(String(255), ForeignKey("users.email"), nullable=False)
    start_time = Column(Integer, nullable=False)
    end_time = Column(Integer, nullable=False)
    company_name = Column(String(255), ForeignKey("user_companies.company_name"), nullable=False)


@listens_for(WifiSession, "after_insert")
def after_wifi_session_insert(mapper, connection, target):
    Session = sessionmaker(bind=connection)
    session = Session()
    wifi_session_history = WifiSessionHistory(
        email=target.email,
        start_time=target.start_time,
        end_time=target.end_time,
        company_name=target.company_name,
    )
    session.add(wifi_session_history)
    session.commit()
    session.close()
