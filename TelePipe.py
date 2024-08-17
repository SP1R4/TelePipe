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
