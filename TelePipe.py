import sys
import os
import argparse
import time
import json
import logging
import re
import zipfile
from bot import TelegramBot


# Configure logging
logging.basicConfig(filename='script.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def load_config(config_file='config.json'):
    """
    Loads configuration settings from a JSON file.

    Args:
        config_file (str): The path to the configuration file.

    Returns:
        dict: The configuration settings as a dictionary.

    Raises:
        FileNotFoundError: If the configuration file does not exist.
        json.JSONDecodeError: If the configuration file is not a valid JSON file.
    """
    logging.info("Loading configuration from config.json")
    try:
        with open(config_file) as f:
            config = json.load(f)
        logging.info("Configuration loaded successfully")
        return config
    except FileNotFoundError:
        logging.error("Config file not found")
        raise
    except json.JSONDecodeError:
        logging.error("Error parsing the config file")
        raise

def validate_extension(extension):
    """
    Validates the file extension to ensure it consists of alphanumeric characters only.

    Args:
        extension (str): The file extension to be validated.

    Raises:
        ValueError: If the file extension is not valid (contains non-alphanumeric characters).
    """
    if not re.match(r'^[a-zA-Z0-9]+$', extension):
        logging.error(f"Invalid file extension: {extension}")
        raise ValueError("Invalid file extension. Only alphanumeric characters are allowed.")
    logging.info(f"File extension '{extension}' validated")

def read_stdin():
    """
    Reads data from standard input (stdin).

    Returns:
        str: The data read from stdin.
    """
    logging.info("Reading data from stdin")
    return sys.stdin.read()

def save_to_file(data, file_extension):
    """
    Saves the provided data to a file with the specified extension.

    Args:
        data (str): The data to be saved.
        file_extension (str): The file extension for the saved file.

    Returns:
        str: The path to the saved file.

    Raises:
        IOError: If there is an error while writing to the file.
    """
    file_name = f"output.{file_extension}"
    logging.info(f"Saving data to file '{file_name}'")
    try:
        with open(file_name, 'w') as file:
            file.write(data)
        logging.info(f"Data successfully saved to '{file_name}'")
        return file_name
    except IOError as e:
        logging.error(f"Error saving file: {e}")
        raise

def save_to_zip(data, zip_name):
    """
    Saves the provided data to a zip file.

    Args:
        data (str): The data to be saved.
        zip_name (str): The name of the zip file to create.

    Returns:
        str: The path to the created zip file.

    Raises:
        IOError: If there is an error while writing to the zip file.
    """
    zip_path = f"{zip_name}.zip"
    logging.info(f"Saving data to zip file '{zip_path}'")
    try:
        with zipfile.ZipFile(zip_path, 'w') as zip_file:
            zip_file.writestr('output.txt', data)
        logging.info(f"Data successfully saved to zip file '{zip_path}'")
        return zip_path
    except IOError as e:
        logging.error(f"Error saving zip file: {e}")
        raise

def wait_for_chat_id(telegram_bot):
    """
    Waits for a chat ID to be obtained by polling the Telegram server until a message is received.

    Args:
        telegram_bot (TelegramBot): An instance of the TelegramBot class.

    Returns:
        int: The chat ID obtained from the latest message.
    """
    logging.info("Waiting for chat ID by polling the Telegram bot")
    chat_id = None
    while chat_id is None:
        logging.info("No interaction detected. Polling again in 10 seconds...")
        print("Waiting for interaction with the bot...")
        chat_id = telegram_bot.get_chat_id()
        if chat_id is None:
            print("No interaction detected. Polling again in 10 seconds...")
            time.sleep(10)
    logging.info(f"Chat ID {chat_id} found")
    print("Chat ID found!")
    return chat_id

def send_file_to_telegram(telegram_bot, chat_id, file_path):
    """
    Sends a file to Telegram.

    Args:
        telegram_bot (TelegramBot): An instance of the TelegramBot class.
        chat_id (int): The chat ID to which the file will be sent.
        file_path (str): The path of the file to be sent.
    """
    logging.info(f"Sending file '{file_path}' to chat ID {chat_id}")
    telegram_bot.send_file(chat_id, file_path)
    logging.info(f"File '{file_path}' successfully sent to Telegram")

def send_file_command(telegram_bot, file_path):
    """
    Sends a specified file to Telegram.

    Args:
        telegram_bot (TelegramBot): An instance of the TelegramBot class.
        file_path (str): The path of the file to be sent.
    """
    logging.info(f"Executing send-file command for '{file_path}'")
    chat_id = wait_for_chat_id(telegram_bot)
    send_file_to_telegram(telegram_bot, chat_id, file_path)

def archive_logs(telegram_bot, chat_id):
    """
    Archives piped output as a zip file and sends it to Telegram.

    Args:
        telegram_bot (TelegramBot): An instance of the TelegramBot class.
        chat_id (int): The chat ID to which the file will be sent.
    """
    logging.info("Archiving piped output to zip and sending to Telegram")
    received_data = read_stdin()
    if received_data:
        zip_path = save_to_zip(received_data, "archive")
        print(f"Data saved to zip file '{zip_path}'.")
        send_file_to_telegram(telegram_bot, chat_id, zip_path)
        os.remove(zip_path)
        logging.info(f"Zip file '{zip_path}' deleted after sending")
        print(f"Zip file '{zip_path}' deleted after sending.")

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
    BOT_TOKEN = config['bot_token']
    telegram_bot = TelegramBot(BOT_TOKEN)

    if args.command == 'send':
        try:
            validate_extension(args.extension)
        except ValueError as e:
            logging.error(f"Invalid extension provided: {args.extension}")
            print(e)
            sys.exit(1)
        chat_id = wait_for_chat_id(telegram_bot)
        file_path = save_to_file(read_stdin(), args.extension)
        send_file_to_telegram(telegram_bot, chat_id, file_path)
        os.remove(file_path)
        logging.info(f"File '{file_path}' deleted after sending")

    elif args.command == 'archive':
        chat_id = wait_for_chat_id(telegram_bot)
        archive_logs(telegram_bot, chat_id)

    elif args.command == 'send-file':
        send_file_command(telegram_bot, args.file_path)

    else:
        logging.info("Invalid command. Displaying help.")
        parser.print_help()

if __name__ == "__main__":
    main()
