import os
import subprocess
import datetime
import re

def get_valid_directory(prompt):
    """Continually asks the user for a valid directory path until a valid one is provided."""
    while True:
        directory = input(prompt).strip()
        if directory.lower() == 'q':
            print("Exiting...\n")
            exit()
        if os.path.isdir(directory):
            return directory
        print("Invalid directory. Please enter a valid folder path (e.g., /path/to/file/): ")

def get_yes_no(prompt):
    """Continually asks the user for 'y' or 'n'. Accepts 'q' to exit."""
    while True:
        response = input(prompt).strip().lower()
        if response in ['y', 'n', 'q']:
            return response
        print("Invalid input. Please enter 'y', 'n', or 'q'.")

def is_valid_target(target):
    """Validate if the target is a valid IP address or address range (CIDR)."""
    # Regular expression for validating IPv4 address or range (CIDR)
    ipv4_pattern = re.compile(r'^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.'  # octet 1
                              r'(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.'  # octet 2
                              r'(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.'  # octet 3
                              r'(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)'  # octet 4
                              r'(\s*\/\s*(3[0-2]|[1-2]?[0-9]))?$')  # optional CIDR part (e.g., /24)
    # Regular expression for validating IPv6 address (just for demonstration, can be expanded)
    ipv6_pattern = re.compile(r'([0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}')

    # Check if target matches either IPv4 or IPv6
    if ipv4_pattern.match(target) or ipv6_pattern.match(target):
        return True
    return False

def run_nmap(scan_type, target, report_dir):
    """Runs Nmap with the chosen scan type on the target and saves output to a file."""
    commands = {
        "1": ["nmap", "--script=vuln*", "-O", "-Pn", target],
        "2": ["nmap", "-sV", "-O", "-Pn", target],
        "3": ["nmap", "-sS", "-T3", "--max-retries", "5", "--max-rate", "30", "-Pn", target]  # Adjusted for reliability
    }
    
    messages = {
        "1": "Certainly! Your Wish is My Command! One Comprehensive NMAP Vulnerability Scan coming right up!\n",
        "2": "Certainly! Your Wish is My Command! One NMAP Service-Version Scan coming right up!\n",
        "3": "Certainly! Your Wish is My Command! One Super-Stealthy NMAP Scan with Adjusted Settings coming right up!\n"
    }

    # Description of each scan type
    scan_descriptions = {
        "1": "This scan uses Nmap’s scripting engine (NSE) to detect vulnerabilities in the target system. "
              "It performs OS detection and service scanning to look for common vulnerabilities and misconfigurations.",
        "2": "This scan is focused on identifying services running on the target system and performing version detection. "
              "It also performs OS detection and attempts to identify open ports and services.",
        "3": "This scan is a stealthier SYN scan that adjusts Nmap's settings to avoid detection. "
              "It reduces network noise and limits retries to avoid triggering intrusion detection systems."
    }

    # Generate the report filename with the current date
    current_date = datetime.datetime.now().strftime("%Y-%m-%d")
    report_path = os.path.join(report_dir, f"NMAP_SCAN_{current_date}.txt")

    print(messages[scan_type])

    # Ask user if they want to know what the scan does right after they confirm to run the scan
    explain_scan = get_yes_no("Would you like to know what this scan does? (y/n): ")
    if explain_scan == "y":
        print(f"\nScan Type {scan_type}: {scan_descriptions[scan_type]}\n")

    print(f"Running scan on {target}...\nOutput will be saved to: {report_path}\n")

    # Run the scan and save output to a file
    try:
        with open(report_path, "w") as report_file:
            subprocess.run(commands[scan_type], stdout=report_file, stderr=subprocess.STDOUT, text=True)
        print(f"Scan completed. Report saved to: {report_path}\n")
    except Exception as e:
        print(f"Error saving the report: {e}")

def main():
    while True:
        start_scan = get_yes_no("\nWould you like to perform an Nmap scan? (y/n/q): ")
        if start_scan == "n" or start_scan == "q":
            print("Exiting the program.\n")
            return
        
        # Get valid directory for output before proceeding
        report_dir = get_valid_directory("Enter the directory where you want to save the scan report (e.g., /path/to/file/): ")

        while True:
            print("\nPlease choose one of the following NMAP Network Vulnerability Scans:\n")
            print("1. NMAP NSE Comprehensive Vulnerability Scan")
            print("2. NMAP Service-Version Scan")
            print("3. NMAP Super-Stealthy Scan with Adjusted Settings")
            print("\nPress 'q' to exit.\n")
            
            choice = input("Enter your scan choice (1-3) or 'q' to exit: ").strip()
            if choice.lower() == "q":
                print("Exiting the program.\n")
                return
            elif choice in ["1", "2", "3"]:
                while True:
                    target = input("\nEnter the target IP address or range: ").strip()
                    if not target:
                        print("Target cannot be empty. Please try again.\n")
                        continue
                    if is_valid_target(target):
                        break
                    print("Invalid target format. Please enter a valid IP address or CIDR range.\n")
                
                print()
                run_nmap(choice, target, report_dir)
                
                repeat = get_yes_no("\nWould you like to perform another scan? (y/n/q): ")
                if repeat == "n" or repeat == "q":
                    print("Exiting the program.\n")
                    return
            else:
                print("Invalid choice, please select a valid option.\n")

if __name__ == "__main__":
    main()
