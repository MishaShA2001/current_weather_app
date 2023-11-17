"""Functions called after user command"""
import sys
from content.main_messages import (WHAT_CITY_MESSAGE,
                                   HOW_MANY_REQUESTS_MESSAGE,
                                   CLOSE_APP_MESSAGE, NO_HISTORY_MESSAGE,
                                   HISTORY_REMOVED_MESSAGE)
from api.geocoder_methods import get_user_city
from api.open_weather.open_weather_methods import get_api_weather
from utils.processing import (get_weather_message, get_weather_params_from_api,
                              get_weather_params_from_db_query, columns_pop,
                              Weather)
from utils.format import check_for_positive_int
from db.config import TABLE_NAME, TABLE_COLUMNS
from db.methods import insert_into_table, select_from_table, truncate_table
from utils.errors import NotPositiveIntError


def weather_in_user_city() -> None:
    """Gets user city at first and then sends info message"""
    user_city = get_user_city()
    get_and_print_weather(user_city)


def weather_in_any_city() -> None:
    """Asks for city and gets current weather for it"""
    city_message = input(WHAT_CITY_MESSAGE)
    get_and_print_weather(city_message.strip())


def get_and_print_weather(city: str) -> None:
    """Makes API call and turns it into a message

    :param city: city to get weather
    """
    api_weather = get_api_weather(city)
    weather_params = get_weather_params_from_api(api_weather)

    print(get_weather_message(weather_params))

    save_weather(weather_params)


def save_weather(weather_params: Weather) -> None:
    """Saves the result of user's query to the database

    :param weather_params: Weather dataclass object
    """
    values = {
        'dt': weather_params.dt,
        'city_name': weather_params.city_name,
        'description': weather_params.description,
        'temp': weather_params.temp,
        'feels_like': weather_params.feels_like,
        'wind_speed': weather_params.wind_speed
    }
    table_columns = columns_pop(TABLE_COLUMNS, ['id'])

    insert_into_table(TABLE_NAME, table_columns, values)


def history() -> None:
    """Asks user for quantity of desired last requests and sends it"""
    quantity = input(HOW_MANY_REQUESTS_MESSAGE)

    if check_for_positive_int(quantity):
        get_and_print_history(quantity)
    else:
        raise NotPositiveIntError


def get_and_print_history(quantity: str) -> None:
    """Makes sql query to get last requests

    :param quantity: user's number
    """
    table_columns = columns_pop(TABLE_COLUMNS, ['id'])

    query_result = select_from_table(
        TABLE_NAME, table_columns, quantity,
        order={'table_column': 'id', 'order_type': 'DESC'}
    )

    if query_result:
        for row in query_result:
            weather_params = get_weather_params_from_db_query(row)
            print(get_weather_message(weather_params))
    else:
        print(NO_HISTORY_MESSAGE)


def remove_history() -> None:
    """Removes all user's requests from database"""
    truncate_table(TABLE_NAME)
    print(HISTORY_REMOVED_MESSAGE)


def close() -> None:
    """Exits the program"""
    print(CLOSE_APP_MESSAGE)
    sys.exit()
