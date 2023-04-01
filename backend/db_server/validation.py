import re
from datetime import datetime

import validate_email as validate_email_package

from utiles import Const
from mysql_util.mysql_exception import (
    InvalidEmailException,
    InvalidPasswordException,
    InvalidCreditCardException,
)


def validate_register_request(full_name: str, password: str, email: str):

    validate_full_name(full_name)
    validate_strong_password(password)
    validate_email(email)


def validate_token(token):
    if token != "46d5d479-5a07-4767-9847-516f04d78fbd":
        raise InvalidEmailException("Sorry, you need a valid token to register as admin")


def validate_full_name(full_name: str):
    pass


def validate_email(email: str):
    is_valid = validate_email_package.validate_email(email, check_mx=False)

    if not is_valid:
        raise InvalidEmailException()


def validate_strong_password(password):
    if len(password) < 8:
        raise InvalidPasswordException("Minimum length is 8 characters")

    if not re.search(r"[a-z]", password):
        raise InvalidPasswordException("The password should include a-z character")

    if not re.search(r"[A-Z]", password):
        raise InvalidPasswordException("The password should include A-Z character")

    if not re.search(r"\d", password):
        raise InvalidPasswordException("The password should include a number")


def validate_credit_card(card_number: str):
    card_number = [int(num) for num in card_number]
    checkDigit = card_number.pop(-1)
    card_number.reverse()
    card_number = [
        num * 2 if idx % 2 == 0 else num for idx, num in enumerate(card_number)
    ]
    card_number = [
        num - 9 if idx % 2 == 0 and num > 9 else num
        for idx, num in enumerate(card_number)
    ]
    card_number.append(checkDigit)
    checkSum = sum(card_number)
    if not (checkSum % 10 == 0):
        raise InvalidCreditCardException


def validate_datetime(str_date: str):
    try:
        datetime.strptime(str_date, Const.DATE_FORMAT)
    except ValueError:
        raise Exception("The string is not in the correct format.")
