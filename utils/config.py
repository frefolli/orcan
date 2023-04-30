"""
provides configuration classes
"""
from dotenv import dotenv_values

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

class ChatConfig:
    """
    bot config
    """
    def __init__(self,
                 chat_id: str) -> None:
        """
        default constructor
        """
        self.chat_id = chat_id

class BoolConfig:
    """
    bot config
    """
    def __init__(self,
                 value: str) -> None:
        """
        default constructor
        """
        match value.lower():
            case "true":
                self.value = True
                return
            case "false":
                self.value = False
                return
            case _:
                raise ValueError(f"SICURA has invalid value {value}")

def get_env_or_default(
        environment_variable: str,
        default_value: str) -> str:
    """
    get content of .env file if is define
    else returns default value

    Args:
        environment_variable (str): _description_
        default_value (str): _description_

    Returns:
        str: _description_
    """
    config = dotenv_values('.env')
    value = (config.get(environment_variable) if config.get(environment_variable) is not None else default_value)
    return value
