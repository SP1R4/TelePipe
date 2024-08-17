# Telegram Pipe Automation Script

This script allows you to automate tasks by sending the output of Linux command-line tools (such as `nmap`) directly to your Telegram account via a bot. You can use the script with Linux pipes to send results as files or archives to your Telegram chat. It leverages the `telebot` library for communication with Telegram.

## Features

- Send piped command output directly to Telegram as a file.
- Archive command output into a zip file and send it to Telegram.
- Send any specified file from your filesystem to Telegram.
- Logs script operations for easy troubleshooting and monitoring.

## Prerequisites

1. **Python 3.x**
2. **Telebot library**  
   Install it via pip:
   ```bash
   pip3 install pyTelegramBotAPI
   ```

3. **Telegram Bot**
   - Create a bot using [BotFather](https://core.telegram.org/bots#botfather).
   - Get your bot token and configure it in the `config.json` file.

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/SP1R4/TelePipe.git
   cd TelePipe
   ```

2. Install the required dependencies:
   ```bash
   pip3 install -r requirements.txt
   ```

3. Create a `config.json` file in the project root directory. This file should contain your bot's token:
   ```json
   {
     "bot_token": "YOUR_BOT_TOKEN_HERE"
   }
   ```

## Make the Script Executable

If you'd like to run the script without having to call it with `python3`, follow these steps:

1. **Add a Shebang Line**:  
   Add the following line at the very top of your `TelePipe.py` script:
   ```bash
   #!/usr/bin/env python3
   ```

2. **Make the Script Executable**:  
   Run the following command to make the script executable:
   ```bash
   chmod +x TelePipe.py
   ```

3. **(Optional) Move the Script to a Directory in Your PATH**:  
   If you'd like to run the script from anywhere, move it to a directory that's included in your `PATH` environment variable:
   ```bash
   sudo mv TelePipe.py /usr/local/bin/telepipe
   ```

   Now you can run the script from anywhere by simply typing:
   ```bash
   telepipe [options]
   ```

## Usage

The script provides the following commands for interaction with Telegram via pipes or direct file sending.

### **1. Send Command Output as a File**

Sends the piped output of a command to Telegram, saved as a file with the specified extension.

```bash
<command> | telepipe send --extension <file_extension>
```

- **Example:**
  ```bash
  nmap 10.10.10.11 -sC -sV | telepipe send --extension json
  ```

- **Explanation:**
  - This will run `nmap` and send the output to Telegram as a `.json` file.

### **2. Send a Specific File**

Send any specified file from your system to Telegram.

```bash
telepipe send-file <file_path>
```

- **Example:**
  ```bash
  telepipe send-file scan_results.txt
  ```

- **Explanation:**
  - This will send the `scan_results.txt` file to your Telegram account.

### **3. Archive Command Output and Send as Zip**

Saves the piped command output to a zip file and sends it to Telegram.

```bash
<command> | telepipe archive
```

- **Example:**
  ```bash
  nmap 10.10.10.11 -sC -sV | telepipe archive
  ```

- **Explanation:**
  - This will run `nmap`, archive the output into a zip file, and send the zip file to your Telegram account.

## Configuration

Ensure that you have a `config.json` file that contains your Telegram bot's token:

```json
{
  "bot_token": "YOUR_BOT_TOKEN_HERE"
}
```

This configuration is required for the bot to interact with your Telegram account.

## Logging

The script uses Python's `logging` module to track operations and errors. Logs are stored in `TelePipe.log`.

- **Example Log Entries:**
  ```text
  2024-08-17 12:00:00 - INFO - Loading configuration from config.json
  2024-08-17 12:00:01 - INFO - Configuration loaded successfully
  2024-08-17 12:00:05 - INFO - Reading data from stdin
  ```

Logs provide useful details for troubleshooting and monitoring the script's execution.

## Example Scenarios

### **1. Automating Network Scans**

You can automate network scans with `nmap` and receive the results directly in Telegram:

```bash
nmap 192.168.1.1 -sC -sV | telepipe send --extension txt
```

### **2. Sending Pre-existing Log Files**

You can send log files generated from other processes directly to your Telegram account:

```bash
telepipe send-file /var/log/syslog
```

### **3. Archiving and Sending Multiple Scans**

Run multiple network scans and archive the results in a zip file before sending:

```bash
nmap 192.168.1.0/24 -sP | telepipe archive
```

## Error Handling

- **No Interaction Detected:**  
  If the script doesn't detect an interaction with the bot (i.e., you haven't sent a `/start` message), it will prompt you to interact with the bot and wait for you to do so.

- **Invalid File Extension:**  
  The script validates the file extension to ensure it's alphanumeric. If an invalid extension is provided, it will raise an error.

## License

This project is licensed under the MIT License.

---
