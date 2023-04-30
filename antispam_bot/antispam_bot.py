"""
provides class AntiSpamBot

Bot Help:

add_banned_word - Adds the specified input WORD to banned word list
remove_banned_word - Removes the specified input WORD from banned word list
find_banned_word - Returns a list of banned words, if WORD is issued it's used as a filter
add_allowed_link - Adds the specified input LINK to allowed link list
remove_allowed_link - Removes the specified input LINK from allowed link list
find_allowed_link - Returns a list of allowed links, if LINK is issued it's used as a filter
start - Displays Start screen
help - Displays Help screen

"""
import logging
import re
from functools import partial
from telegram.constants import ParseMode
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackQueryHandler
from telegram.ext import MessageHandler
from telegram.ext import ContextTypes
from telegram.ext import CommandHandler
from telegram.ext import BaseHandler
from persistence import AntiSpamPersistenceFactory
from telegram_api import TelegramAPIFactory
from utils.secrets import ANTISPAM_BOT, SPAM_CHAT_ID, SICURA


HELP_SCREEN = """
```
# Usage

## Banned Words

- /add_banned_word <WORD>
- /remove_banned_word <WORD>
- /find_banned_word [WORD]

Must WORD always be a non empty word. Spaces and tabs don't count.

If WORD is omitted while using /find_banned_word,
i'll return all banned words

## Allowed Links

- /add_allowed_link <LINK>
- /remove_allowed_link <LINK>
- /find_allowed_link [LINK]

Must LINK always be a non empty word. Spaces and tabs don't count.

If LINK is omitted while using /find_allowed_link,
i'll return all allowed links

## Misc

- /start display start screen
- /help display help screen
```
"""
START_SCREEN = """
```
#####################################
#####################################
##########                   #  #####
##### ########           ##    ######
#####    ########    ##     #########
##### #    #########    ##  #########
#####   #    ## #######    ##### ####
#####     #     ## ###########   ####
#####    #       #    #########  ####
#####  #    # #     ############ ####
##### #   #     ##########  #########
#####   #   ######### #     #########
#####  ##########        ##    ######
#############                ## #####
#####################################

Svoltamib Telegram Bot Infrastructure
            Bot  Antispam            
```
"""


def assemble_regex_for_finding_literals(literals: list[str]):
    """
    assemble a regex in order to match a word from a list of literals

    Args:
        literals (list[str]): list of literals
    """
    escaped_literals = [
        "(?:" + re.escape(literal) + ")"
        for literal in literals]
    return "|".join(escaped_literals)


def read_tlds():
    """
    read tlds from asset file
    """
    with open("assets/tlds.txt", mode="r", encoding="utf-8") as file:
        return file.read().split("\n")


# TLDS = read_tlds()
# assume text is lowercase
LINK_REGEX = (
    # open capture group
    # protocol
    r"(?:[a-z0-9]+:\/\/)?" +
    "(" +
    # domain
    r"(?:[a-z0-9][\-a-z0-9]+)(?:\.[a-z0-9][\-a-z0-9]+)+" +
    # top level domain
    # f"(?:\\.{assemble_regex_for_finding_literals(TLDS)})" +
    # close capture group
    ")"
)


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
        self.__link_finder = re.compile(LINK_REGEX)
        self.__update_allowed_links_finder()
        self.__update_banned_words_finder()

    def __update_allowed_links_finder(self) -> None:
        """
        update allowed links finder
        extracting informations from persistence
        """
        allowed_links = self.__persistence.get_all_allowed_links()
        regex_object = re.compile(
            "^(" + assemble_regex_for_finding_literals(allowed_links) + ")$")
        if len(allowed_links) > 0:
            self.__allowed_links_finder = partial((
                lambda regex, text: (
                    len(regex.findall(text)) > 0
                )
            ), regex_object)
        else:
            self.__allowed_links_finder = lambda text: False

    def __update_banned_words_finder(self) -> None:
        """
        update banned words finder
        extracting informations from persistence
        """
        banned_words = self.__persistence.get_all_banned_words()
        regex_object = re.compile(
            "(" + assemble_regex_for_finding_literals(banned_words) + ")")
        if len(banned_words) > 0:
            self.__banned_words_finder = partial((
                lambda regex, text: (
                    len(regex.findall(text)) > 0
                )
            ), regex_object)
        else:
            self.__banned_words_finder = lambda text: False

    def __build_handler_list(self) -> list[BaseHandler]:
        """
        assemble handler list
        """
        return [
            CommandHandler(
                "add_banned_word",
                partial(self.authenticated,
                        self.__handle_add_banned_word)),
            CommandHandler(
                "add_allowed_link",
                partial(self.authenticated,
                        self.__handle_add_allowed_link)),

            CommandHandler(
                "remove_banned_word",
                partial(self.authenticated,
                        self.__handle_remove_banned_word)),
            CommandHandler(
                "remove_allowed_link",
                partial(self.authenticated,
                        self.__handle_remove_allowed_link)),

            CommandHandler(
                "find_banned_word",
                partial(self.authenticated,
                        self.__handle_find_banned_word)),
            CommandHandler(
                "find_allowed_link",
                partial(self.authenticated,
                        self.__handle_find_allowed_link)),

            CommandHandler(
                "help",
                self.__handle_help),
            CommandHandler(
                "start",
                self.__handle_start),
            CallbackQueryHandler(
                partial(self.authenticated,self.__handle_delete),
                pattern="^DELETE:[0-9]+:[0-9]+$"
            ),
            CallbackQueryHandler(
                partial(self.authenticated,self.__handle_delete_and_ban),
                pattern="^BAN:[0-9]+:[0-9]+:[0-9]+$"
            ),
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

    async def __report_incident(self,
                                event: str,
                                update: Update,
                                __context: ContextTypes.DEFAULT_TYPE) -> None:
        distress_signal = f"Distress: `Spam`\nType: `{event}`"
        if event == "Unwanted Link" or event == "Unwanted Word":
            distress_signal += f"\nMessage: ```\n\n{update.message.text}\n```"
        reply_markup = InlineKeyboardMarkup([[
            InlineKeyboardButton(
                "Delete",
                callback_data=f"DELETE:{update.message.chat_id}:{update.message.id}"),
            InlineKeyboardButton(
                "Delete And Ban",
                callback_data=f"BAN:{update.message.chat_id}:{update.message.id}:{update.message.from_user.id}")
        ]])
        await update._bot.send_message(chat_id=SPAM_CHAT_ID.chat_id,
                                       text=distress_signal,
                                       parse_mode=ParseMode.MARKDOWN_V2,
                                       reply_markup=reply_markup)

    async def __handle_delete(self,
                              update: Update,
                              __context: ContextTypes.DEFAULT_TYPE) -> None:
        (_, chat_id, msg_id) = update.callback_query.data.split(":")
        await update._bot.deleteMessage(chat_id, msg_id)
        await update.callback_query.message.edit_reply_markup()
        await update.callback_query.message.edit_text("deleted correctly!")

    async def __handle_delete_and_ban(self,
                              update: Update,
                              __context: ContextTypes.DEFAULT_TYPE) -> None:
        (_, chat_id, msg_id, usr_id) = update.callback_query.data.split(":")
        print(chat_id, msg_id, usr_id)
        await update._bot.deleteMessage(chat_id, msg_id)
        if not SICURA.value:
            await update._bot.banChatMember(chat_id, usr_id)
        await update.callback_query.message.edit_reply_markup()
        await update.callback_query.message.edit_text("deleted and banned correctly!")

    async def authenticated(self, then, update: Update,
                            context: ContextTypes.DEFAULT_TYPE) -> None:
        """applies authentication (authorization) to command request

        Args:
            then (_type_): callback
            update (Update): update object
            context (ContextTypes.DEFAULT_TYPE): context if any

        Calls:
            then: (_type_): callback
        """
        user_id: int = 0
        if update.callback_query is not None:
            user_id = update.callback_query.from_user.id
        if update.message is not None:
            user_id = update.message.from_user.id
        member = await self.__telegram_api.is_admin(user_id)
        if member:
            return await then(update, context)
        else:
            return await self.__report_incident("Unauthorized", update, context)

    def __get_command_argument(self, message: str) -> str:
        return " ".join(message.split(" ")[1:])

    async def __handle_message(
            self,
            update: Update,
            context: ContextTypes.DEFAULT_TYPE) -> None:
        """handle incoming message

        Args:
            update (Update): _description_
            context (ContextTypes.DEFAULT_TYPE): _description_
        """
        text_message = update.message.text.lower()
        links = self.__link_finder.findall(text_message)
        for link in links:
            if not self.__allowed_links_finder(link):
                await self.__report_incident("Unwanted Link", update, context)

        if self.__banned_words_finder(text_message):
            await self.__report_incident("Unwanted Word", update, context)

    async def __handle_add_banned_word(
            self,
            update: Update,
            _context: ContextTypes.DEFAULT_TYPE) -> None:
        """handle /add_banned_word

        Args:
            update (Update): _description_
            context (ContextTypes.DEFAULT_TYPE): _description_
        """
        word = self.__get_command_argument(update.message.text.lower()).strip()
        if len(word) == 0:
            return await update.message.reply_text(
                "invalid word issued",
                quote=True)
        self.__persistence.add_banned_word(word)
        self.__update_banned_words_finder()
        await update.message.reply_text(
            "banned words updated correctly",
            quote=True)

    async def __handle_add_allowed_link(
            self,
            update: Update,
            _context: ContextTypes.DEFAULT_TYPE) -> None:
        """handle /add_allowed_link

        Args:
            update (Update): _description_
            context (ContextTypes.DEFAULT_TYPE): _description_
        """
        link = self.__get_command_argument(update.message.text.lower()).strip()
        if len(link) == 0:
            return await update.message.reply_text(
                "invalid link issued",
                quote=True)
        self.__persistence.add_allowed_link(link)
        self.__update_allowed_links_finder()
        await update.message.reply_text(
            "allowed links updated correctly",
            quote=True)

    async def __handle_remove_banned_word(
            self,
            update: Update,
            _context: ContextTypes.DEFAULT_TYPE) -> None:
        """handle /remove_banned_word

        Args:
            update (Update): _description_
            context (ContextTypes.DEFAULT_TYPE): _description_
        """
        word = self.__get_command_argument(update.message.text.lower()).strip()
        if len(word) == 0:
            return await update.message.reply_text(
                "invalid word issued",
                quote=True)
        self.__persistence.remove_banned_word(word)
        self.__update_banned_words_finder()
        await update.message.reply_text(
            "banned words updated correctly",
            quote=True)

    async def __handle_remove_allowed_link(
            self,
            update: Update,
            _context: ContextTypes.DEFAULT_TYPE) -> None:
        """handle /remove_allowed_link

        Args:
            update (Update): _description_
            context (ContextTypes.DEFAULT_TYPE): _description_
        """
        link = self.__get_command_argument(update.message.text.lower()).strip()
        if len(link) == 0:
            return await update.message.reply_text(
                "invalid link issued",
                quote=True)
        self.__persistence.remove_allowed_link(link)
        self.__update_allowed_links_finder()
        await update.message.reply_text(
            "allowed links updated correctly",
            quote=True)

    async def __handle_find_banned_word(
            self,
            update: Update,
            _context: ContextTypes.DEFAULT_TYPE) -> None:
        """handle /find_banned_word

        Args:
            update (Update): _description_
            context (ContextTypes.DEFAULT_TYPE): _description_
        """
        word = self.__get_command_argument(update.message.text.lower().strip())
        matching_words = list(filter((lambda candidate: word in candidate),
                              self.__persistence.get_all_banned_words()))
        if len(matching_words) == 0:
            await update.message.reply_text("no matching words found")
        else:
            await update.message.reply_markdown_v2(
                "matching words:\n```\n\t- %s\n```"
                % "\n\t- ".join(matching_words),
                quote=True)

    async def __handle_find_allowed_link(
            self,
            update: Update,
            _context: ContextTypes.DEFAULT_TYPE) -> None:
        """handle /find_allowed_link

        Args:
            update (Update): _description_
            context (ContextTypes.DEFAULT_TYPE): _description_
        """
        link = self.__get_command_argument(update.message.text.lower().strip())
        matching_links = list(filter((lambda candidate: link in candidate),
                              self.__persistence.get_all_allowed_links()))
        if len(matching_links) == 0:
            await update.message.reply_text("no matching links found")
        else:
            await update.message.reply_markdown_v2(
                "matching links:\n```\n\t- %s\n```"
                % "\n\t- ".join(matching_links),
                quote=True)

    async def __handle_help(
            self,
            update: Update,
            _context: ContextTypes.DEFAULT_TYPE) -> None:
        """handle /help

        Args:
            update (Update): _description_
            context (ContextTypes.DEFAULT_TYPE): _description_
        """
        await update.message.reply_markdown_v2(
            HELP_SCREEN,
            quote=True)

    async def __handle_start(
            self,
            update: Update,
            _context: ContextTypes.DEFAULT_TYPE) -> None:
        """handle /start

        Args:
            update (Update): _description_
            context (ContextTypes.DEFAULT_TYPE): _description_
        """
        await update.message.reply_markdown_v2(
            START_SCREEN,
            quote=True)

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
