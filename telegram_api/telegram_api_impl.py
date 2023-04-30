"""
provides concrete TelegramAPI implementation
"""
import telegram
from telegram.ext import BaseHandler
from telegram.ext import ApplicationBuilder
from telegram_api.i_telegram_api import ITelegramAPI
from utils.secrets import ADMIN_CHAT_ID


class TelegramAPIImpl(ITelegramAPI):
    """
    concrete TelegramAPI implementation
    """
    def __init__(self,
                 api_token: str,
                 handlers: list[BaseHandler] = None) -> None:
        """
        default constructor
        """
        self.__collect_secrets()
        self.__assign_api_token(api_token)
        self.__initialize_application()
        self.__assign_application_handlers(handlers)

    def __collect_secrets(self) -> None:
        """
        collects secrets
        """
        self.__admin_chat_id = ADMIN_CHAT_ID.chat_id

    def __assign_api_token(self, api_token: str) -> None:
        """
        assigns api token
        """
        self.__api_token = api_token

    def __initialize_application(self) -> None:
        """
        initializes telegram.ext.Application instance
        """
        self.__application = (ApplicationBuilder()
                              .token(self.__api_token)
                              .build())

    def __assign_application_handlers(self,
                                      handlers: list[BaseHandler] = None
                                      ) -> None:
        """
        applies application handlers
        """
        if handlers is not None:
            self.__application.add_handlers(handlers)

    def start(self) -> None:
        """
        starts application
        """
        self.__application.run_polling()

    def __enter__(self) -> None:
        """
        starts application
        """
        self.__application.start()
        return self

    def __exit__(self,
                 exception_type,
                 exception_value,
                 exception_traceback) -> None:
        """
        closes application
        """

    def get_api_token(self) -> str:
        """
        returns api token passed as input
        """
        return self.__api_token

    async def is_admin(self, user_id: str) -> bool:
        """
        should True if a user_id is an admin
        """
        try:
            member = await self.__application.bot.get_chat_member(self.__admin_chat_id, user_id)
            return (member.status not in ["left", "kicked", "restricted"])
        except telegram.error.TelegramError as err:
            print(err)
            return False