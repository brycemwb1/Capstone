import os
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

        target = input("Enter the target URL or IP (or 'q' to quit): ").strip()
        if target.lower() == 'q':
            print("Exiting the program.")
            exit()

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

        # Get a valid directory from the user
        output_folder = get_valid_directory()

        # Generate filename with timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        output_file = os.path.join(output_folder, f"scan_{timestamp}.txt")

        # Append output file details to command
        command += f" -o \"{output_file}\" -Format txt"

        print(f"\nRunning: {command}")
        os.system(command)

        print(f"\nScan complete! Report saved at: {output_file}")

        # Ask if the user wants to perform another scan
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
