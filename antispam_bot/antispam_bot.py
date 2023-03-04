"""
provides class AntiSpamBot
"""
import logging
from telegram import Update
from telegram.ext import MessageHandler
from telegram.ext import ContextTypes
from telegram.ext import CommandHandler
from telegram.ext import BaseHandler
from persistence import AntiSpamPersistenceFactory
from telegram_api import TelegramAPIFactory
from utils.secrets import ANTISPAM_BOT


class AntiSpamBot:
    """
    antispam telegram bot
    """
    def __init__(self) -> None:
        """
        default constructor
        """
        self.__build_persistence()
        self.__build_context()
        self.__build_telegram_api()

    def __build_persistence(self) -> None:
        """
        setup persistence
        """
        self.__persistence = AntiSpamPersistenceFactory.new()

    def __build_context(self) -> None:
        """
        setup context
        extracting informations from persistence
        """
        self.__banned_words = self.__persistence.get_all_banned_words()
        self.__allowed_links = self.__persistence.get_all_allowed_links()

    def __build_handler_list(self) -> list[BaseHandler]:
        """
        assemble handler list
        """
        return [
            CommandHandler(
                "get_banned_words",
                self.__handle_get_banned_words),
            CommandHandler(
                "get_allowed_links",
                self.__handle_get_allowed_links),

            CommandHandler(
                "add_banned_word",
                self.__handle_add_banned_word),
            CommandHandler(
                "add_allowed_link",
                self.__handle_add_allowed_link),

            CommandHandler(
                "remove_banned_word",
                self.__handle_remove_banned_word),
            CommandHandler(
                "remove_allowed_link",
                self.__handle_remove_allowed_link),

            CommandHandler(
                "find_banned_word",
                self.__handle_find_banned_word),
            CommandHandler(
                "find_allowed_link",
                self.__handle_find_allowed_link),

            CommandHandler(
                "help",
                self.__handle_help),
            MessageHandler(
                filters=None,
                callback=self.__handle_message)
        ]

    def __build_telegram_api(self) -> None:
        """
        setup telegram api
        """
        handlers = self.__build_handler_list()
        self.__telegram_api = TelegramAPIFactory.new(
            api_token=ANTISPAM_BOT.api_token,
            handlers=handlers
        )

    async def __handle_message(
            self,
            update: Update,
            context: ContextTypes.DEFAULT_TYPE) -> None:
        """handle incoming message

        Args:
            update (Update): _description_
            context (ContextTypes.DEFAULT_TYPE): _description_
        """
        logging.warning("message: %s" % update)

    async def __handle_add_banned_word(
            self,
            update: Update,
            context: ContextTypes.DEFAULT_TYPE) -> None:
        """handle /add_banned_word

        Args:
            update (Update): _description_
            context (ContextTypes.DEFAULT_TYPE): _description_
        """
        logging.warning("/add_banned_word: %s" % update)

    async def __handle_add_allowed_link(
            self,
            update: Update,
            context: ContextTypes.DEFAULT_TYPE) -> None:
        """handle /add_allowed_link

        Args:
            update (Update): _description_
            context (ContextTypes.DEFAULT_TYPE): _description_
        """
        logging.warning("/add_allowed_link: %s" % update)

    async def __handle_remove_banned_word(
            self,
            update: Update,
            context: ContextTypes.DEFAULT_TYPE) -> None:
        """handle /remove_banned_word

        Args:
            update (Update): _description_
            context (ContextTypes.DEFAULT_TYPE): _description_
        """
        logging.warning("/remove_banned_word: %s" % update)

    async def __handle_remove_allowed_link(
            self,
            update: Update,
            context: ContextTypes.DEFAULT_TYPE) -> None:
        """handle /remove_allowed_link

        Args:
            update (Update): _description_
            context (ContextTypes.DEFAULT_TYPE): _description_
        """
        logging.warning("/remove_allowed_link: %s" % update)

    async def __handle_find_banned_word(
            self,
            update: Update,
            context: ContextTypes.DEFAULT_TYPE) -> None:
        """handle /find_banned_word

        Args:
            update (Update): _description_
            context (ContextTypes.DEFAULT_TYPE): _description_
        """
        logging.warning("/find_banned_word: %s" % update)

    async def __handle_find_allowed_link(
            self,
            update: Update,
            context: ContextTypes.DEFAULT_TYPE) -> None:
        """handle /find_allowed_link

        Args:
            update (Update): _description_
            context (ContextTypes.DEFAULT_TYPE): _description_
        """
        logging.warning("/find_allowed_link: %s" % update)

    async def __handle_get_banned_words(
            self,
            update: Update,
            context: ContextTypes.DEFAULT_TYPE) -> None:
        """handle /get_banned_words

        Args:
            update (Update): _description_
            context (ContextTypes.DEFAULT_TYPE): _description_
        """
        logging.warning("/get_banned_words: %s" % update)

    async def __handle_get_allowed_links(
            self,
            update: Update,
            context: ContextTypes.DEFAULT_TYPE) -> None:
        """handle /get_allowed_links

        Args:
            update (Update): _description_
            context (ContextTypes.DEFAULT_TYPE): _description_
        """
        logging.warning("/get_allowed_links: %s" % update)

    async def __handle_help(
            self,
            update: Update,
            context: ContextTypes.DEFAULT_TYPE) -> None:
        """handle /help

        Args:
            update (Update): _description_
            context (ContextTypes.DEFAULT_TYPE): _description_
        """
        logging.warning("/help: %s" % update)

    def start(self) -> None:
        """
        start the telegram api and the bot
        """
        logging.info("AntiSpam Bot [STARTED]")
        self.__telegram_api.start()
        logging.info("AntiSpam Bot [STOPPED]")

    def __enter__(self) -> "AntiSpamBot":
        """
        with-as semantic
        """
        self.start()
        return self

    def __exit__(self,
                 exception_type,
                 exception_value,
                 exception_traceback) -> None:
        """
        with-as semantic
        """
