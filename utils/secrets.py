"""
provides secrets
"""
from utils.config import BotConfig
from utils.config import ChatConfig
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

BOT_SEGNALAZIONI = (
    BotConfig(
        api_token=(
            get_env_or_default(
                "BOT_SEGNALAZIONI_API_TOKEN",
                "<API-TOKEN>")
        )))


CHECK_SEGNAL_CHAT_ID = (
    ChatConfig(
        chat_id=(
            get_env_or_default(
               "CHECK_SEGNAL_CHAT_ID",
               "<CHAT_ID>")
        )))

FORWARD_SEGNAL_CHAT_ID = (
    ChatConfig(
        chat_id=(
            get_env_or_default(
               "FORWARD_SEGNAL_CHAT_ID",
               "<CHAT_ID>")
        )))

ADMIN_CHAT_ID = (
    ChatConfig(
        chat_id=(
            get_env_or_default(
               "ADMIN_CHAT_ID",
               "<CHAT_ID>")
        )))