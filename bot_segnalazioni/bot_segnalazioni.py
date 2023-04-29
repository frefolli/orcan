"""
provides class bot_segnalazioni
"""
import logging
from telegram import Update
from telegram import *
from telegram.ext import MessageHandler
from telegram.ext import ContextTypes
from telegram.ext import CommandHandler
from telegram.ext import BaseHandler
from persistence.bot_segnalazioni import SegnalazioniPersistenceFactory
from telegram_api import TelegramAPIFactory
from utils.secrets import BOT_SEGNALAZIONI
from utils.secrets import CHECK_SEGNAL_CHAT_ID
from utils.secrets import FORWARD_SEGNAL_CHAT_ID
from utils.secrets import ADMIN_CHAT_ID


class bot_segnalazioni:
    """
    bot_segnalazioni telegram bot
    """
    def __init__(self) -> None:
        """
        default constructor
        """
        self.__build_persistence()
        self.__build_context()
        self.__build_telegram_api()

    def __build_persistence(self) -> None:
        self.__chats = {
            'CHECK_GROUP': CHECK_SEGNAL_CHAT_ID,
            'ADMIN_CHAT_ID': ADMIN_CHAT_ID,
            'FORWARD_GROUP': FORWARD_SEGNAL_CHAT_ID
        }
        self.__persistence = SegnalazioniPersistenceFactory.new()

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
                "manda",
                self.__handle_manda),

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
            api_token=BOT_SEGNALAZIONI.api_token,
            handlers=handlers
        )

    """forse non è ottimale stia qui txt2md"""
    def __text2md(self, str:str) -> str:
        charset = ['_', '*', '[', '`']
        for i in charset:
            str= str.replace(i, '\\'+i)
        return str

    async def __handle_message(
            self,
            update: Update,
            context: ContextTypes.DEFAULT_TYPE) -> None:
        """handle incoming message

        Args:
            update (Update): _description_
            context (ContextTypes.DEFAULT_TYPE): _description_
        """
        logging.warning("\n(__handle_message) MESS ARRIVATO: \n %s\n" % update)
        await self.__handle_help(update, context)

        

    async def __handle_manda(
            self,
            update: Update,
            context: ContextTypes.DEFAULT_TYPE) -> None:
        """handle /manda
        Args:
            update (Update): _description_
            context (ContextTypes.DEFAULT_TYPE): _description_
        """
        logging.warning("(__handle_manda) mess arrivato: \n%s" % update)

        query = update.callback_query

        logging.warning("%s", update.effective_chat.id)

        """ Versione: semplice inoltro mess nel gruppo target
            problema: con certe impostazioni di privacy alcuni utenti potrebbero non essere raggiungibili cliccando sul loro nome dopo "inoltrato da"
            await update._bot.forward_message(chat_id = self.__chats['ADMIN_CHAT_ID'].chat_id,
                            from_chat_id = update.effective_chat.id,
                            message_id = update.message.message_id)"""
        
        
        if "/manda" not in update.message.text:
            logging.error("/manda non è mel mess ricevuto. qualcosa non va!!")
            return


        messConComandoTolto = update.message.text.replace("/manda","")
        testoMessModificato = "Segnalazione da " + str(update.message.from_user.first_name) + "\n\n" + self.__text2md(messConComandoTolto) + "\n\nPer contattare l'utente: " + "[Toccami](tg://user?id=" + str(update.message.from_user.id) +")"

        logging.warning(testoMessModificato)

        await update._bot.send_message(text=testoMessModificato, 
                        parse_mode = "MarkdownV2", 
                        chat_id = self.__chats['ADMIN_CHAT_ID'].chat_id)

        await update._bot.send_message(text="Segnalazione mandata. Grazie per aver usato questo bot.", 
                        chat_id = update.effective_chat.id)


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

        await update._bot.send_message(text="<i><b>Benvenuto nel Bot Segnalazioni di SvoltaMiB</b></i>\nSe vuoi spedire una segnalazione basta scrivere\n /manda corpo della segnalazione \nProva!", 
                        parse_mode = "HTML", 
                        chat_id = update.effective_chat.id)

    def start(self) -> None:
        """
        start the telegram api and the bot
        """
        logging.info("bot_segnalazioni [STARTED]")
        self.__telegram_api.start()
        logging.info("bot_segnalazioni [STOPPED]")

    def __enter__(self) -> "bot_segnalazioni":
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
