import re
import validate_email as validate_email_package

from exception import (
    InvalidEmailException,
    InvalidPasswordException,
    InvalidCreditCardException,
)


def validate_register_request(username: str, password: str, email: str):
    validate_username(username)
    validate_strong_password(password)
    validate_email(email)


def validate_username(username: str):
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
