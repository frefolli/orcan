"""
provides class AntiSpamBot
"""
import logging
from telegram import Update
from telegram import InlineKeyboardButton
from telegram import InlineKeyboardMarkup

from telegram.ext import MessageHandler
from telegram.ext import ContextTypes
from telegram.ext import CommandHandler
from telegram.ext import BaseHandler
from telegram.ext import CallbackQueryHandler
from telegram.ext import ConversationHandler
from telegram.ext import filters

from telegram_api import TelegramAPIFactory

from post_bot.post import Post
from post_bot.state import State
from post_bot.state import CallbackData

from utils.secrets import CHECK_POST_CHAT_ID
from utils.secrets import FORWARD_POST_CHAT_ID

from utils.secrets import POST_BOT

class PostBot:
    """
    Post telegram bot
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
        self.__chats = {
            'CHECK_GROUP': CHECK_POST_CHAT_ID,
            'FORWARD_GROUP': FORWARD_POST_CHAT_ID
        }
        return None

    def __build_context(self) -> None:
        """
        setup context
        extracting informations from persistence
        """
        return None
    
    def __build_handler_list(self) -> list[BaseHandler]:
        """
        assemble handler list
        """
        conv_handler = ConversationHandler(
            entry_points=[
                CommandHandler("start", self.__start),
                CommandHandler("create_new_post", self.__start),
                ],
            states={
                State.ASK_TITLE: [
                    CallbackQueryHandler(self.__ask_title, pattern="^" + str(CallbackData.CREATE) + "$"),
                ],
                State.TITLE: [
                    MessageHandler(filters.TEXT, self.__handle_title),
                ],
                State.DESCRIPTION: [
                    MessageHandler(filters.TEXT, self.__handle_description),
                ],
                State.ASK_ATTACHMENT: [
                    CallbackQueryHandler(self.__ask_attachment, pattern="^" + str(CallbackData.ATTACHMENT_YES) + "$"),
                    CallbackQueryHandler(self.__handle_no_attachment, pattern="^" + str(CallbackData.ATTACHMENT_NO) + "$"),
                ],
                State.ATTACHMENT: [
                    MessageHandler(filters.ATTACHMENT, self.__handle_attachment),
                ],
                State.CONFIRM: [
                    CallbackQueryHandler(self.__handle_confirm, pattern="^" + str(CallbackData.POST_CHECK) + "$"),
                    CallbackQueryHandler(self.__handle_deletion_confirm, pattern="^" + str(CallbackData.POST_DELETE) + "$")
                ]
            },
            fallbacks=[MessageHandler(filters.ALL, self.__cancel)],
        )

        return [
            conv_handler,
            CommandHandler(
                "help",
                self.__handle_help),
            CallbackQueryHandler(
                self.__handle_publish, 
                pattern="^" + str(CallbackData.POST_PUBLISH) + "$"
            )
        ]

    def __build_telegram_api(self) -> None:
        """
        setup telegram api
        """
        handlers = self.__build_handler_list()
        self.__telegram_api = TelegramAPIFactory.new(
            api_token=POST_BOT.api_token,
            handlers=handlers
        )
    
    async def __start(
            self,
            update: Update,
            context: ContextTypes.DEFAULT_TYPE) -> None:
        """
        handle /start

        Args:
            update (Update): _description_
            context (ContextTypes.DEFAULT_TYPE): _description_
        """
        user = update.message.from_user
        logging.info("User %s started the conversation.", user.first_name)
        keyboard = [
            [
                InlineKeyboardButton("create new post", callback_data=str(CallbackData.CREATE))
            ]
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.message.reply_text("What do you want to do?", reply_markup=reply_markup)

        return State.ASK_TITLE
        
    async def __ask_title(
            self,
            update: Update,
            context: ContextTypes.DEFAULT_TYPE) -> int:
        query = update.callback_query

        await query.answer()
        await query.edit_message_text(text="What is the title of your post?")

        return State.TITLE

    async def __handle_title(
            self,
            update: Update,
            context: ContextTypes.DEFAULT_TYPE) -> int:
        """
            handle title of the post
        
            Args:
                update (Update): _description_
                context (ContextTypes.DEFAULT_TYPE): _description_
        """
        context.chat_data["Post"] = Post(update.message.text)
        logging.info("setting title post")
        await update.message.reply_text("Insert a description of your post:")
        return State.DESCRIPTION

    async def __handle_description(
            self,
            update: Update,
            context: ContextTypes.DEFAULT_TYPE) -> int:
        
        context.chat_data["Post"].set_description(update.message.text)
        logging.info("setting description post")
        keyboard = [
            [
                InlineKeyboardButton("Yes", callback_data=str(CallbackData.ATTACHMENT_YES)),
                InlineKeyboardButton("No", callback_data=str(CallbackData.ATTACHMENT_NO))
            ]
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.message.reply_text("Do you want to add an attachment?", reply_markup=reply_markup)
        return State.ASK_ATTACHMENT

    async def __ask_attachment(
            self,
            update: Update,
            context: ContextTypes.DEFAULT_TYPE) -> int:
        query = update.callback_query
        
        await query.edit_message_text(text="Drop an attachment from your gallery:")

        return State.ATTACHMENT
    
    async def __handle_attachment(
            self,
            update: Update,
            context: ContextTypes.DEFAULT_TYPE) -> int:
        
        f = await update.message.photo[-1].get_file()
        context.chat_data['Post'].set_file_id(f.file_id)


        keyboard = [
            [
                InlineKeyboardButton("Publish", callback_data=str(CallbackData.POST_CHECK)),
                InlineKeyboardButton("Delete", callback_data=str(CallbackData.POST_DELETE))
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.message.reply_text(text="***POST RESUME***")
        await update._bot.send_photo(chat_id = update.message.chat_id, 
                                     photo = context.chat_data['Post'].get_file_id(),
                                     caption = context.chat_data['Post'].get_text(),
                                     reply_markup = reply_markup) 
        return State.CONFIRM
    
    async def __handle_no_attachment(
            self,
            update: Update,
            context: ContextTypes.DEFAULT_TYPE) -> int:
        
        query = update.callback_query

        keyboard = [
            [
                InlineKeyboardButton("Publish", callback_data=str(CallbackData.POST_CHECK)),
                InlineKeyboardButton("Delete", callback_data=str(CallbackData.POST_DELETE))
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await update._bot.send_message(chat_id = query.message.chat_id, text="***POST RESUME***")
        await update._bot.send_message(chat_id = query.message.chat_id, 
                                       text = context.chat_data['Post'].get_text(),
                                       reply_markup = reply_markup) 
        
        return State.CONFIRM

    async def __handle_confirm(
            self,
            update: Update,
            context: ContextTypes.DEFAULT_TYPE) -> None:
        query = update.callback_query

        keyboard = [
            [
                InlineKeyboardButton("CONFIRM", callback_data=str(CallbackData.POST_PUBLISH)),
                InlineKeyboardButton("Delete", callback_data=str(CallbackData.POST_DELETE))
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        if context.chat_data['Post'].get_file_id() != None:
            await update._bot.send_photo(chat_id = self.__chats['CHECK_GROUP'], 
                                         photo = context.chat_data['Post'].get_file_id(),
                                         caption = context.chat_data['Post'].get_text(),
                                         reply_markup = reply_markup) 
        else:
            await update._bot.send_message(chat_id = self.__chats['CHECK_GROUP'], 
                                           text = context.chat_data['Post'].get_text(),
                                           reply_markup = reply_markup) 
        return ConversationHandler.END
    
    async def __handle_publish(
            self,
            update: Update,
            context: ContextTypes.DEFAULT_TYPE) -> None:
        query = update.callback_query

        
        if context.chat_data['Post'].get_file_id() != None:
            await update._bot.send_photo(chat_id = self.__chats['FORWARD_GROUP'], 
                                         photo = context.chat_data['Post'].get_file_id(),
                                         caption = context.chat_data['Post'].get_text()) 
        else:
            await update._bot.send_message(chat_id = self.__chats['FORWARD_GROUP'], 
                                           text = context.chat_data['Post'].get_text()) 
    
    async def __handle_deletion_confirm(
            self,
            update: Update,
            context: ContextTypes.DEFAULT_TYPE) -> None:
        
        return ConversationHandler.END

    async def __cancel(
            self,
            update: Update,
            context: ContextTypes.DEFAULT_TYPE) -> None:
        """handle if something goes wrong

        Args:
            update (Update): _description_
            context (ContextTypes.DEFAULT_TYPE): _description_
        """
        await update.message.reply_text("This input doesn't expected, the creation of post is canceled. Please create e new post typing /create_new_post")
        logging.info("/cancel: %s" % update)
        return ConversationHandler.END

    async def __handle_help(
            self,
            update: Update,
            context: ContextTypes.DEFAULT_TYPE) -> None:
        """handle /help

        Args:
            update (Update): _description_
            context (ContextTypes.DEFAULT_TYPE): _description_
        """
        await update.message.reply_text("Use /start or /create_new_post to create a new post.")
        logging.info("/help: %s" % update)


    def start(self) -> None:
        """
        start the telegram api and the bot
        """
        logging.info("Post Bot [STARTED]")
        self.__telegram_api.start()
        logging.info("Post Bot [STOPPED]")

    def __enter__(self) -> 'PostBot':
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
