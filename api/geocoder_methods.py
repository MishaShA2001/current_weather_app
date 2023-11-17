"""Methods with using geocoder"""
from typing import Optional
from geocoder import ip
from utils.errors import UserCityCantBeFoundError


def get_user_city() -> Optional[str]:
    """Gets user's city by his current place

    :return: user's city
    """
    try:
        return ip('me').city
    except Exception:
        raise UserCityCantBeFoundError
