"""Here are the ways to answer user"""
from enum import StrEnum
from services.main_menu_actions import (weather_in_user_city,
                                        weather_in_any_city, history,
                                        remove_history,
                                        close)
from utils.errors import UnknownCommandError, errors_handler


class Action(StrEnum):
    """Matches action names and user commands"""
    WEATHER_IN_USER_CITY = '1'
    WEATHER_IN_ANY_CITY = '2'
    HISTORY = '3'
    REMOVE_HISTORY = '4'
    CLOSE = '5'


@errors_handler
def react_to_user_message(text: str) -> None:
    """Runs some function depending on user's command

    :param text: user's message
    """
    match text:
        case Action.WEATHER_IN_USER_CITY:
            weather_in_user_city()
        case Action.WEATHER_IN_ANY_CITY:
            weather_in_any_city()
        case Action.HISTORY:
            history()
        case Action.REMOVE_HISTORY:
            remove_history()
        case Action.CLOSE:
            close()
        case _:
            raise UnknownCommandError
