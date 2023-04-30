"""
provides secrets
"""
from utils.config import ChatConfig, BotConfig, BoolConfig
from utils.config import get_env_or_default


ANTISPAM_BOT = (
    BotConfig(
        api_token=(
            get_env_or_default(
                "ANTISPAM_BOT_API_TOKEN",
                "<API-TOKEN>")
        )))

POST_BOT = (
    BotConfig(
        api_token=(
            get_env_or_default(
                "POST_BOT_API_TOKEN",
                "<API-TOKEN>")
        )))


REPORT_BOT = (
    BotConfig(
        api_token=(
            get_env_or_default(
                "REPORT_BOT_API_TOKEN",
                "<API-TOKEN>")
        )))

ADMIN_CHAT_ID = (
    ChatConfig(
        chat_id=(
            get_env_or_default(
                "ADMIN_CHAT_ID",
                "<CHAT_ID>")
        )))

SPAM_CHAT_ID = (
    ChatConfig(
        chat_id=(
            get_env_or_default(
                "ADMIN_CHAT_ID",
                "<CHAT_ID>")
        )))

CHECK_POST_CHAT_ID = (
    ChatConfig(
        chat_id=(
            get_env_or_default(
               "CHECK_POST_CHAT_ID",
               "<CHAT_ID>")
        )))

FORWARD_POST_CHAT_ID = (
    ChatConfig(
        chat_id=(
            get_env_or_default(
               "FORWARD_POST_CHAT_ID",
               "<CHAT_ID>")
        )))

SICURA = (
    BoolConfig(
        value=(
            get_env_or_default(
               "SICURA",
               "True")
        )))
