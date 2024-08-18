# TelePipe: Telegram Pipe Automation Script

**TelePipe** is a Python script that integrates with Telegram to automate the process of sending command-line tool outputs and files directly to your Telegram account. Using the `telebot` library, the script supports sending file outputs from piped commands, existing files, and even archiving results into zip files for transmission.

## Features

- Send piped command output as a file to Telegram.
- Archive command output into a zip file and send it to Telegram.
- Send any specified file from your filesystem to Telegram.
- Logs all script operations for easy troubleshooting and monitoring.

## Prerequisites

1. **Python 3.x**
2. **Telebot Library**  
   Install it via pip:
   ```bash
   pip3 install pyTelegramBotAPI
   ```
3. **Telegram Bot**
   - Create a bot using [BotFather](https://core.telegram.org/bots#botfather).
   - Obtain your bot token and configure it in the `config.json` file.

## Installation

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/SP1R4/TelePipe.git
   cd TelePipe-main
   ```

2. **Install Required Dependencies:**
   ```bash
   pip3 install -r requirements.txt
   ```

3. **Configure the Bot Token:**
   Create a `config.json` file in the project root directory with the following content:
   ```json
   {
     "bot_token": "YOUR_BOT_TOKEN_HERE"
   }
   ```

## Usage

The script provides the following commands to interact with Telegram via pipes or direct file sending.

### 1. Send Command Output as a File

Sends the piped output of a command to Telegram, saved as a file with the specified extension.

```bash
<command> | python3 TelePipe.py send --extension <file_extension>
```

**Example:**
```bash
nmap 10.10.10.11 -sC -sV | python3 TelePipe.py send --extension json
```

**Explanation:**
- This will run `nmap` and send the output to Telegram as a `.json` file.

### 2. Send a Specific File

Send any specified file from your filesystem to Telegram.

```bash
python3 TelePipe.py send-file <file_path>
```

**Example:**
```bash
python3 TelePipe.py send-file scan_results.txt
```

**Explanation:**
- This will send the `scan_results.txt` file to your Telegram account.

### 3. Archive Command Output and Send as Zip

Saves the piped command output to a zip file and sends it to Telegram.

```bash
<command> | python3 TelePipe.py archive
```

**Example:**
```bash
nmap 10.10.10.11 -sC -sV | python3 TelePipe.py archive
```

**Explanation:**
- This will run `nmap`, archive the output into a zip file, and send the zip file to your Telegram account.

## Configuration

Ensure you have a `config.json` file with your Telegram bot's token:

```json
{
  "bot_token": "YOUR_BOT_TOKEN_HERE"
}
```

## Logging

The script uses Python's `logging` module to track operations and errors. Logs are stored in `TelePipe.log`.

**Example Log Entries:**
```
2024-08-17 12:00:00 - INFO - Loading configuration from config.json
2024-08-17 12:00:01 - INFO - Configuration loaded successfully
2024-08-17 12:00:05 - INFO - Reading data from stdin
```

Logs provide details for troubleshooting and monitoring script execution.

## Error Handling

- **No Interaction Detected:**  
  If the script doesn't detect an interaction with the bot (i.e., you haven't sent a `/start` message), it will prompt you to interact with the bot and wait for you to do so.

- **Invalid File Extension:**  
  The script validates the file extension to ensure it's alphanumeric. If an invalid extension is provided, it will raise an error.

## Example Scenarios

### 1. Automating Network Scans

Automate network scans with `nmap` and receive the results directly in Telegram:

```bash
nmap 192.168.1.1 -sC -sV | python3 TelePipe.py send --extension txt
```

### 2. Sending Pre-existing Log Files

Send log files generated from other processes directly to your Telegram account:

```bash
python3 TelePipe.py send-file /var/log/syslog
```

### 3. Archiving and Sending Multiple Scans

Run multiple network scans and archive the results in a zip file before sending:

```bash
nmap 192.168.1.0/24 -sP | python3 TelePipe.py archive
```

## Making the Script Executable

To make the script executable without typing `python3`, follow these steps:

1. **Add a Shebang Line** at the top of `TelePipe.py`:
   ```python
   #!/usr/bin/env python3
   ```

2. **Make the Script Executable**:
   ```bash
   chmod +x TelePipe.py
   ```

3. **Run the Script** directly:
   ```bash
   <command> | ./TelePipe.py send --extension txt
   ```

