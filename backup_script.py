import os
import paramiko
from datetime import datetime

# Configuration
SOURCE_DIR = "C:/data"  # Directory to back up
DESTINATION_SERVER = "8.8.4.4"  # Remote server address (replace with your server's IP or hostname)
DESTINATION_USER = "Ria"  # Username for the remote server (replace with your username)
DESTINATION_PATH = "tar -czvf /backup_access.tar C:/Users/riyav/OneDrive/Desktop"  # Remote backup path
LOG_FILE = "C:/python37/backup/backup_log.txt"  # Log file path
SSH_KEY_PATH = "//wsl.localhost/Ubuntu/home/coderiya/.ssh" # Path to your SSH private key

def log_message(message):
    """Write a message to the log file."""
    with open(LOG_FILE, "a") as log_file:
        log_file.write(f"{datetime.now()} - {message}\n")

def backup_directory():
    """Backup the directory to the remote server."""
    try:
        # Establish SSH connection
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(DESTINATION_SERVER, username=DESTINATION_USER, key_filename=SSH_KEY_PATH)

        # Use SFTP to upload files
        sftp = ssh.open_sftp()
        for root, dirs, files in os.walk(SOURCE_DIR):
            remote_root = os.path.join(DESTINATION_PATH, os.path.relpath(root, SOURCE_DIR))
            try:
                sftp.mkdir(remote_root)
            except IOError:
                pass  # Directory already exists

            for file in files:
                local_file = os.path.join(root, file)
                remote_file = os.path.join(remote_root, file)
                sftp.put(local_file, remote_file)

        sftp.close()
        ssh.close()
        log_message("Backup completed successfully.")
        print("Backup completed successfully.")

    except Exception as e:
        log_message(f"Backup failed: {e}")
        print(f"Backup failed: {e}")

# Run the backup
backup_directory()
