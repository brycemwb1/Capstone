import os
import subprocess
import sys

def get_existing_directory():
    while True:
        report_dir = input("Enter the directory path where the report should be saved (or 'q' to quit): ").strip()
        if report_dir.lower() == 'q':
            print("Exiting the program.")
            sys.exit(0)
        if os.path.exists(report_dir):
            return report_dir
        print("Directory does not exist. Please enter an existing directory.")

def run_wapiti_scan():
    while True:
        run_scan = input("Do you want to run a Wapiti scan? (y/n/q): ").strip().lower()
        if run_scan == 'q':
            print("Exiting the program.")
            sys.exit(0)
        if run_scan != 'y':
            print("Scan canceled.")
            break

        website_url = input("Enter the website URL (e.g., http://example.com) or 'q' to quit: ").strip()
        if website_url.lower() == 'q':
            print("Exiting the program.")
            sys.exit(0)

        report_dir = get_existing_directory()

        folder_name = input("Enter the name for the report folder (or 'q' to quit): ").strip()
        if folder_name.lower() == 'q':
            print("Exiting the program.")
            sys.exit(0)

        report_folder_path = os.path.join(report_dir, folder_name)

        print("Running basic scan...")

        try:
            subprocess.run(f"wapiti -u {website_url} --flush-session -o \"{report_folder_path}/wapiti-report.html\"", shell=True, check=True)
            print(f"Scan completed. Report saved at {report_folder_path}/wapiti-report.html")
        except subprocess.CalledProcessError as e:
            print(f"Error during scan: {e}")

if __name__ == "__main__":
    run_wapiti_scan()
