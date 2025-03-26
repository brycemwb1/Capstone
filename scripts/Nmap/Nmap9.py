import os
import subprocess
import datetime

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

    # Generate the report filename with the current date
    current_date = datetime.datetime.now().strftime("%Y-%m-%d")
    report_path = os.path.join(report_dir, f"NMAP_SCAN_{current_date}.txt")

    print(messages[scan_type])
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
                target = input("\nEnter the target IP address or range: ").strip()
                if not target:
                    print("Target cannot be empty. Please try again.\n")
                    continue
                print()
                run_nmap(choice, target, report_dir)
                
                repeat = get_yes_no("\nWould you like to perform another scan? (y/n/q): ")
                if repeat == "no" or repeat == "q":
                    print("Exiting the program.\n")
                    return
            else:
                print("Invalid choice, please select a valid option.\n")

if __name__ == "__main__":
    main()
