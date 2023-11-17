from typing import Callable
from content.errors_messages import (USER_CITY_CANT_BE_FOUND_MESSAGE,
                                     INCORRECT_CITY_MESSAGE,
                                     SERVER_PROBLEMS_MESSAGE,
                                     UNKNOWN_COMMAND_MESSAGE,
                                     DATABASE_PROBLEM_MESSAGE,
                                     NOT_POSITIVE_INT_MESSAGE,
                                     UNEXPECTED_PROBLEM_MESSAGE)


def errors_handler(func: Callable[..., None]) -> Callable[..., None]:
    """Decorator to handle exceptions

    :param func: function to decorate
    """

    def wrapper(*args, **kwargs) -> None:
        try:
            func(*args, **kwargs)
        except (UserCityCantBeFoundError, IncorrectCityError,
                ServerProblemsError, UnknownCommandError,
                DatabaseProblemError, NotPositiveIntError) as e:
            print(e)
        except Exception:
            raise UnexpectedProblemError

    return wrapper


class UserCityCantBeFoundError(Exception):
    """If there are some problems with geocoder"""

    def __init__(self):
        super().__init__(USER_CITY_CANT_BE_FOUND_MESSAGE)


class IncorrectCityError(Exception):
    """It API link with entered city gives 400-errors"""

    def __init__(self):
        super().__init__(INCORRECT_CITY_MESSAGE)


class ServerProblemsError(Exception):
    """It API link with entered city gives 400-errors"""

    def __init__(self):
        super().__init__(SERVER_PROBLEMS_MESSAGE)


class UnknownCommandError(Exception):
    """It API link with entered city gives 400-errors"""

    def __init__(self):
        super().__init__(UNKNOWN_COMMAND_MESSAGE)


class DatabaseProblemError(Exception):
    """It API link with entered city gives 400-errors"""

    def __init__(self):
        super().__init__(DATABASE_PROBLEM_MESSAGE)


class NotPositiveIntError(Exception):
    """It API link with entered city gives 400-errors"""

    def __init__(self):
        super().__init__(NOT_POSITIVE_INT_MESSAGE)


class UnexpectedProblemError(Exception):
    """It API link with entered city gives 400-errors"""

    def __init__(self):
        super().__init__(UNEXPECTED_PROBLEM_MESSAGE)
