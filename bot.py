import telebot
import logging


class TelegramBot:
    """
    A class to interact with the Telegram Bot API.
    """

    def __init__(self, bot_token):
        """
        Initializes the TelegramBot instance with the provided bot token.

        Args:
            bot_token (str): The token for the Telegram bot.
        """
        self.bot = telebot.TeleBot(bot_token)

    def get_chat_id(self):
        """
        Polls for updates from the Telegram server to retrieve the chat ID from the latest message.

        Returns:
            int: The chat ID of the latest message if available; otherwise, None.
        """
        try:
            updates = self.bot.get_updates(timeout=10)
            if updates:
                return updates[-1].message.chat.id
        except Exception as e:
            logging.error(f"Error getting updates: {e}")
        return None

    def send_file(self, chat_id, file_path):
        """
        Sends a file to the specified Telegram chat.

        Args:
            chat_id (int): The chat ID to which the file will be sent.
            file_path (str): The path of the file to be sent.

        Raises:
            Exception: If an error occurs while sending the file.
        """
        try:
            with open(file_path, 'rb') as file:
                self.bot.send_document(chat_id, file)
            logging.info(f"File '{file_path}' sent successfully.")
        except Exception as e:
            logging.error(f"Failed to send file '{file_path}': {e}")
