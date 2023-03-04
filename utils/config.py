"""
provides configuration classes
"""
import os


class BotConfig:
    """
    bot config
    """
    def __init__(self,
                 api_token: str) -> None:
        """
        default constructor
        """
        self.api_token = api_token


def get_env_or_default(
        environment_variable: str,
        default_value: str) -> str:
    """
    get content of environment variable if is define
    else returns default value

    Args:
        environment_variable (str): _description_
        default_value (str): _description_

    Returns:
        str: _description_
    """
    return os.environ.get(
        environment_variable,
        default_value
    )
