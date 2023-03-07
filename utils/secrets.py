"""
provides secrets
"""
from utils.config import BotConfig
from utils.config import get_env_or_default


ANTISPAM_BOT = (
    BotConfig(
        api_token=(
            get_env_or_default(
                "ANTISPAM_BOT_API_TOKEN",
                "<API-TOKEN>")
        )))

REPOST_BOT = (
    BotConfig(
        api_token=(
            get_env_or_default(
                "REPOST_BOT_API_TOKEN",
                "<API-TOKEN>")
        )))


REPORT_BOT = (
    BotConfig(
        api_token=(
            get_env_or_default(
                "REPORT_BOT_API_TOKEN",
                "<API-TOKEN>")
        )))
