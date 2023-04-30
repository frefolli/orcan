"""
entry point for module antispam_bot
"""
import logging
from post_bot.post_bot import PostBot


def main() -> None:
    """
    entry point
    """
    logging.getLogger().setLevel(logging.INFO)
    bot = PostBot()
    bot.start()


if __name__ == "__main__":
    main()
