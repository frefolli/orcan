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
    chat config
    """
    def __init__(self,
                 chat_id: str) -> None:
        """
        default constructor
        """
        self.chat_id = chat_id

class BoolConfig:
    """
    bool config
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

def text2md(str : str) -> str:
    """
    return a string 

    Args:
        str (str): string to parse in md

    Returns:
        str: formatted string ready to be encoded in md 
    """
    charset = ['_', '*', '[', ']', '(', ')', '~', '`', '>', '#', '+', '-', '=', '|', '{', '}', '.', '!']
    for i in charset:
        str = str.replace(i,'\\'+i)
    return str