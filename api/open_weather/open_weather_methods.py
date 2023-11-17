"""Methods with OpenWeatherMap API"""
from typing import Optional, Any
import requests
from http import HTTPStatus
from api.open_weather.url_template import URL_TEMPLATE
from utils.errors import IncorrectCityError, ServerProblemsError


def get_api_weather(city: str) -> Optional[dict[Any, Any]]:
    """Gets weather data with API

    :param city: in which weather is got
    :return: API answer
    """
    response = requests.get(URL_TEMPLATE.format(city=city))

    if response.status_code == HTTPStatus.OK:
        return response.json()
    elif response.status_code in (HTTPStatus.BAD_REQUEST,
                                  HTTPStatus.NOT_FOUND):
        raise IncorrectCityError
    elif response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR:
        raise ServerProblemsError
