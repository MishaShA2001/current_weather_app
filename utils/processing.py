"""Process API answers, database answers, etc"""
from typing import Any, Union
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
import copy

from content.templates import WEATHER_MESSAGE_TEMPLATE


@dataclass
class Weather:
    dt: Union[str, datetime]
    city_name: str
    description: str
    temp: float
    feels_like: float
    wind_speed: float


def get_weather_message(weather_object: Weather) -> str:
    """Gets a beautiful message for user

    :param weather_object: weather dataclass object
    :return: message to send
    """
    return WEATHER_MESSAGE_TEMPLATE.format(
        dt=weather_object.dt,
        city_name=weather_object.city_name,
        description=weather_object.description,
        temp=weather_object.temp,
        feels_like=weather_object.feels_like,
        wind_speed=weather_object.wind_speed
    )


def get_weather_params_from_api(api_weather: dict[Any, Any]) -> Weather:
    """Gets info about weather in dataclass format

    :param api_weather: json from API request
    :return: dataclass weather
    """
    return Weather(
        dt=convert_to_datetime(api_weather['dt'], api_weather['timezone']),
        city_name=api_weather['name'],
        description=api_weather['weather'][0]['description'],
        temp=api_weather['main']['temp'],
        feels_like=api_weather['main']['feels_like'],
        wind_speed=api_weather['wind']['speed']
    )


def get_weather_params_from_db_query(query_result: tuple[Any, ...]) -> Weather:
    """Turns row from database into Weather object

    :param query_result: got after select query
    :return: dataclass weather
    """
    return Weather(
        dt=query_result[0],
        city_name=query_result[1],
        description=query_result[2],
        temp=query_result[3],
        feels_like=query_result[4],
        wind_speed=query_result[5]
    )


def convert_to_datetime(timestamp: int, timezone_: int) -> datetime:
    """Turns given timestep and timezone into beautiful datetime format

    :param timestamp: unix time
    :param timezone_: time difference (from Prime Meridian)
    :return: datetime object with params info
    """
    timezone_ = timezone(timedelta(seconds=timezone_))
    return datetime.fromtimestamp(timestamp, timezone_)


def columns_pop(columns: dict[str, str],
                columns_to_delete: list[str]) -> dict[str, str]:
    """Deletes some columns from given column template

    :param columns: all columns (template)
    :param columns_to_delete: unnecessary columns
    :return: new column template
    """
    table_columns_copy = copy.deepcopy(columns)
    for column in columns_to_delete:
        table_columns_copy.pop(column)
    return table_columns_copy
