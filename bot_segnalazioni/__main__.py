"""
entry point for module bot_segnalazioni
"""
import logging
from bot_segnalazioni.bot_segnalazioni import bot_segnalazioni


def main() -> None:
    """
    entry point
    """
    logging.getLogger().setLevel(logging.INFO)
    bot = bot_segnalazioni()
    bot.start()


if __name__ == "__main__":
    main()
