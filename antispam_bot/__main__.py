"""
entry point for module antispam_bot
"""
import logging
from antispam_bot.antispam_bot import AntiSpamBot


def main() -> None:
    """
    entry point
    """
    logging.getLogger().setLevel(logging.INFO)
    bot = AntiSpamBot()
    bot.start()


if __name__ == "__main__":
    main()
