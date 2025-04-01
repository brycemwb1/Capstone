import os
import re
from datetime import datetime

def show_tuning_options():
    tuning_options = {
        "0": "Upload files - Remote File Retrieval - Server Wide",
        "1": "View specific file in log",
        "2": "Default file misconfiguration",
        "3": "Display information disclosure",
        "4": "Injection (XSS/Script/HTML)",
        "5": "Remote File Retrieval - Inside Web Root",
        "6": "Denial of Service",
        "7": "Remote File Retrieval - Server Wide",
        "8": "Command Execution / Remote Shell",
        "9": "SQL Injection",
        "a": "Authentication Bypass",
        "b": "Software Identification",
        "c": "Remote Source Inclusion"
    }

    print("\nNikto Tuning Options:")
    for key, desc in tuning_options.items():
        print(f"[{key}] {desc}")
    print("\n")

def is_valid_target(target):
    """Validate if the target is a valid URL or IP address."""
    url_pattern = re.compile(
        r'^(https?:\/\/)?'  # Optional http or https
        r'(([a-zA-Z0-9_-]+\.)+[a-zA-Z]{2,6}|'  # Domain name
        r'((\d{1,3}\.){3}\d{1,3}))'  # OR IPv4
        r'(:\d{1,5})?'  # Optional port
        r'(\/.*)?$',  # Optional path
        re.IGNORECASE
    )
    return bool(url_pattern.match(target))

def get_valid_directory():
    """Prompt user for a valid directory, ensuring it exists before returning."""
    while True:
        output_folder = input("Enter the output folder path (e.g., /path/to/reports) or 'q' to quit: ").strip()
        if output_folder.lower() == 'q':
            print("Exiting the program.")
            exit()
        if os.path.isdir(output_folder):
            return output_folder
        print("Error: The specified directory does not exist. Please enter a valid directory.")

def explain_scan():
    """Provide a brief explanation of what the scan will do."""
    print("\nA website scan with Nikto will check for common vulnerabilities, misconfigurations, and security risks.")
    print("This includes outdated software, default files, potential exploits, and security issues.")
    print("It helps identify weaknesses but does not exploit them.\n")

def run_nikto_scan():
    while True:
        start_scan = input("Would you like to perform a Website Nikto scan? (y/n/q): ").strip().lower()
        if start_scan in ["y", "n", "q"]:
            if start_scan == "q" or start_scan == "n":
                print("Exiting the program.")
                exit()
            break
        print("Invalid input. Please enter 'y', 'n', or 'q'.")

    while True:
        explain = input("Would you like a brief explanation of what this scan will do? (y/n): ").strip().lower()
        if explain in ["y", "n"]:
            if explain == "y":
                explain_scan()
            break
        print("Invalid input. Please enter 'y' or 'n'.")

    while True:
        print("\nNikto Scanner Options:")
        print("1. Basic Scan")
        print("2. Scan with User-Specified Ports")
        print("3. Tuning Scan (0-9, a-c)")

        choice = input("Enter your choice (1/2/3) or 'q' to quit: ").strip().lower()
        if choice == 'q':
            print("Exiting the program.")
            exit()
        if choice in ["1", "2", "3"]:
            break
        print("Invalid choice. Please enter 1, 2, 3, or 'q'.")

    while True:
        target = input("Enter the target URL or IP (or 'q' to quit): ").strip()
        if target.lower() == 'q':
            print("Exiting the program.")
            exit()
        if is_valid_target(target):
            break
        print("Error: Invalid target. Please enter a valid URL or IP address.")

    if choice == "1":
        command = f"nikto -h {target}"
    elif choice == "2":
        ports = input("Enter the ports to scan (comma-separated, e.g., 80,443,8080) or 'q' to quit: ").strip()
        if ports.lower() == 'q':
            print("Exiting the program.")
            exit()
        command = f"nikto -h {target} -p {ports}"
    elif choice == "3":
        show_tuning_options()
        while True:
            tuning_option = input("Enter the tuning option (0-9, a-c) or 'q' to quit: ").strip().lower()
            if tuning_option == 'q':
                print("Exiting the program.")
                exit()
            if tuning_option in "0123456789abc":
                break
            print("Invalid tuning option. Please enter a valid option or 'q' to quit.")
        command = f"nikto -h {target} -Tuning {tuning_option}"

    output_folder = get_valid_directory()

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    output_file = os.path.join(output_folder, f"scan_{timestamp}.txt")

    command += f" -o \"{output_file}\" -Format txt"

    print(f"\nRunning: {command}")
    os.system(command)

    print(f"\nScan complete! Report saved at: {output_file}")

    while True:
        another_scan = input("\nDo you want to perform another website scan? (y/n/q): ").strip().lower()
        if another_scan in ["y", "n", "q"]:
            if another_scan == "q" or another_scan == "n":
                print("Exiting the program.")
                exit()
            break
        print("Invalid input. Please enter 'y', 'n', or 'q'.")

if __name__ == "__main__":
    run_nikto_scan()
