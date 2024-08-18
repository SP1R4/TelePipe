import sys
import os
import argparse
import logging
from bot import TelegramBot
from utils import (load_config,
                   validate_extension, 
                   wait_for_chat_id, 
                   save_to_file, 
                   archive_logs, 
                   send_file_command, 
                   send_file_to_telegram, 
                   read_stdin) 


# Configure logging
logging.basicConfig(filename='TelePipe.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def handle_send_command(extension, telegram_bot):
    """
    Handles the 'send' command: saves piped output as a file and sends it to Telegram.

    Args:
        extension (str): The file extension for the saved file.
        telegram_bot (TelegramBot): The instance of the TelegramBot class.
    """
    try:
        validate_extension(extension)
        chat_id = wait_for_chat_id(telegram_bot)
        file_path = save_to_file(read_stdin(), extension)
        send_file_to_telegram(telegram_bot, chat_id, file_path)
        os.remove(file_path)
        logging.info(f"File '{file_path}' deleted after sending")
    except ValueError as e:
        logging.error(f"Invalid file extension: {extension}")
        print(e)
        sys.exit(1)
    except Exception as e:
        logging.error(f"Error handling 'send' command: {e}")
        print("An error occurred. Please check the log file for details.")
        sys.exit(1)

def handle_archive_command(telegram_bot):
    """
    Handles the 'archive' command: archives piped output and sends it to Telegram.

    Args:
        telegram_bot (TelegramBot): The instance of the TelegramBot class.
    """
    try:
        chat_id = wait_for_chat_id(telegram_bot)
        archive_logs(telegram_bot, chat_id)
    except Exception as e:
        logging.error(f"Error handling 'archive' command: {e}")
        print("An error occurred. Please check the log file for details.")
        sys.exit(1)

def handle_send_file_command(file_path, telegram_bot):
    """
    Handles the 'send-file' command: sends a specified file to Telegram.

    Args:
        file_path (str): The path to the file to be sent.
        telegram_bot (TelegramBot): The instance of the TelegramBot class.
    """
    try:
        send_file_command(telegram_bot, file_path)
    except Exception as e:
        logging.error(f"Error handling 'send-file' command: {e}")
        print("An error occurred. Please check the log file for details.")
        sys.exit(1)

def main():
    """
    Main function that handles command-line arguments and dispatches commands.
    """
    parser = argparse.ArgumentParser(description="A script to interact with Telegram bot.")
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Send file command
    send_file_parser = subparsers.add_parser('send-file', help='Send a specified file to Telegram')
    send_file_parser.add_argument('file_path', help='Path to the file to be sent')

    # Send command
    send_parser = subparsers.add_parser('send', help='Send piped output as a file to Telegram')
    send_parser.add_argument('--extension', required=True, help='The file extension to save the piped output as (e.g., txt, json, log)')

    # Archive command
    archive_parser = subparsers.add_parser('archive', help='Archive piped output as a zip file and send to Telegram')

    args = parser.parse_args()
    
    config = load_config()
    BOT_TOKEN = config.get('bot_token')
    if not BOT_TOKEN:
        logging.error("Bot token not found in configuration.")
        print("Configuration error: Bot token not found. Please check config.json.")
        sys.exit(1)

    telegram_bot = TelegramBot(BOT_TOKEN)

    if args.command == 'send':
        handle_send_command(args.extension, telegram_bot)

    elif args.command == 'archive':
        handle_archive_command(telegram_bot)

    elif args.command == 'send-file':
        handle_send_file_command(args.file_path, telegram_bot)

    else:
        logging.info("Invalid command. Displaying help.")
        parser.print_help()

if __name__ == "__main__":
    main()
