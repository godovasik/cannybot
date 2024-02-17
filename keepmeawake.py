import subprocess
import time
import os
import psutil

def is_script_running(script_name):
    # Get list of all running processes
    lst = [p.info for p in psutil.process_iter(['name', 'exe', 'cmdline'])]

    # Check if script_name is in the list of running processes
    return any(script_name in item['cmdline'] for item in lst if item['cmdline'])

def main():
    script_name = 'main.py'  # replace with your script name

    while True:
        if not is_script_running(script_name):
            print(f'{script_name} is not running. Starting it now...')
            subprocess.Popen(['python3', script_name])  # replace 'python' with 'py' or 'python3' if necessary
        time.sleep(60)  # check every minute

if __name__ == '__main__':
    main()