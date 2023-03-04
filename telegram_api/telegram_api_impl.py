"""
provides concrete TelegramAPI implementation
"""
from telegram.ext import BaseHandler
from telegram.ext import ApplicationBuilder
from telegram_api.i_telegram_api import ITelegramAPI


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
        self.__assign_api_token(api_token)
        self.__initialize_application()
        self.__assign_application_handlers(handlers)

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
