from typing import Optional


class UniqueViolationException(Exception):
    def __init__(self, error_msg: Optional[str] = None):
        msg = error_msg if error_msg else "Invalid email"
        super().__init__(msg)


class InvalidTokenException(ValueError):
    def __init__(self, error_msg: Optional[str] = None):
        msg = error_msg if error_msg else "Invalid token"
        super().__init__(msg)

class InvalidEmailException(ValueError):
    def __init__(self, error_msg: Optional[str] = None):
        msg = error_msg if error_msg else "Invalid email"
        super().__init__(msg)


class InvalidUsernameException(ValueError):
    def __init__(self, error_msg: Optional[str] = None):
        msg = error_msg if error_msg else "Invalid email"
        super().__init__(msg)


class InvalidPasswordException(ValueError):
    def __init__(self, error_msg: Optional[str] = None):
        msg = error_msg if error_msg else "Invalid email"
        super().__init__(msg)


class InvalidCreditCardException(ValueError):
    def __init__(self, error_msg: Optional[str] = None):
        msg = error_msg if error_msg else "Invalid credit card"
        super().__init__(msg)
