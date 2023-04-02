from sqlalchemy import Column, Integer, String, Float, TIMESTAMP, ForeignKey, BigInteger
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    email = Column(String(100), nullable=False, primary_key=True)
    full_name = Column(String(100), nullable=False)
    password = Column(String(128), nullable=False)
    created_at = Column(TIMESTAMP, server_default='NOW()')


class Admin(Base):
    __tablename__ = 'admins'
    email = Column(String(100), nullable=False, primary_key=True)
    full_name = Column(String(100), nullable=False)
    hashed_password = Column(String(128), nullable=False)
    created_at = Column(TIMESTAMP, server_default='NOW()')


class CreditCard(Base):
    __tablename__ = 'credit_cards'
    email = Column(String(255), ForeignKey('users.email'), nullable=False, primary_key=True)
    card_number = Column(String(16), nullable=False)
    expiration_month = Column(String(2), nullable=False)
    expiration_year = Column(String(4), nullable=False)
    hashed_cvv = Column(String(255), nullable=False)


class Payment(Base):
    __tablename__ = 'payments'
    email = Column(String(255), ForeignKey('users.email'), nullable=False, primary_key=True)
    price = Column(Integer, nullable=False)
    created_at = Column(BigInteger, nullable=False)


class CompanyToken(Base):
    __tablename__ = 'companies_tokens'
    company_name = Column(String(255), primary_key=True, nullable=False)
    hashed_token = Column(String(255), nullable=False)


class WifiSession(Base):
    __tablename__ = 'wifi_sessions'
    email = Column(String(255), ForeignKey('users.email'), nullable=False, primary_key=True)
    start_time = Column(Float, nullable=False)
    end_time = Column(Float, nullable=False)
    data_usage = Column(Integer, nullable=False)
