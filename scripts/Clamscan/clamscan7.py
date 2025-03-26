import os
import subprocess
import datetime

def update_clamscan_db():
    """Updates the ClamAV virus database using freshclam."""
    print("Updating ClamAV virus database...")
    subprocess.run(['sudo', 'freshclam'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

def get_valid_path(prompt):
    """Continually asks the user for a valid file or folder path until a valid one is provided."""
    while True:
        path = input(prompt).strip()
        if path.lower() == 'q':
            print("Exiting the program.")
            exit()
        if os.path.exists(path):
            return path
        print("Invalid path. The file or folder does not exist. Please try again.")

def get_valid_directory(prompt):
    """Continually asks the user for a valid directory path until a valid one is provided."""
    while True:
        directory = input(prompt).strip()
        if directory.lower() == 'q':
            print("Exiting the program.")
            exit()
        if os.path.isdir(directory):
            return directory
        print("Invalid directory. Please enter a valid folder path.")

def run_clamscan(path, report_dir):
    """Runs ClamAV scan on the specified path and saves the output to a text file in the given directory."""
    current_date = datetime.datetime.now().strftime("%Y-%m-%d")
    report_path = os.path.join(report_dir, f"ClamscanAV.{current_date}.txt")

    print(f"Running clamscan on {path}...\nReport will be saved as: {report_path}\n")
    command = ['clamscan', '--recursive', '--infected', '--remove=no', path]
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    # Save the scan results to the report file
    try:
        with open(report_path, "w") as report_file:
            report_file.write(result.stdout)
        print(f"Scan completed. Report saved to: {report_path}\n")
    except Exception as e:
        print(f"Error saving the report: {e}")

if __name__ == "__main__":
    # Ask if the user wants to perform a malware scan
    while True:
        start_scan = input("Would you like to perform a malware file scan? (y/n/q): ").strip().lower()
        if start_scan in ['y', 'n', 'q']:
            break
        print("Invalid input. Please enter 'y', 'n', or 'q'.")

    if start_scan != 'y':
        print("Exiting the program.")
        exit()

    # Update ClamAV database
    update_clamscan_db()

    while True:
        # Get valid file or folder path
        path = get_valid_path("\nEnter the file or folder path to scan (e.g., /path/to/file/file.exe): ")

        # Get valid report directory
        report_dir = get_valid_directory("Enter the output folder path (e.g., /path/to/reports): ")

        # Run the scan and save the output
        run_clamscan(path, report_dir)

        # Ask if the user wants to scan another file/folder
        while True:
            repeat = input("Do you want to scan another file or folder? (y/n/q): ").strip().lower()
            if repeat in ['y', 'n', 'q']:
                break
            print("Invalid input. Please enter 'y', 'n', or 'q'.")

        if repeat != 'y':
            print("Exiting the program.")
            break
