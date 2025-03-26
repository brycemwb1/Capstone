import subprocess

# List of script paths
scripts = [
    "/home/bryce/Desktop/CapstoneProject/scripts/Clamscan/clamscan7.py",
    "/home/bryce/Desktop/CapstoneProject/scripts/Nikto/NiktoScan10.py",
    "/home/bryce/Desktop/CapstoneProject/scripts/Nmap/Nmap9.py",
    "/home/bryce/Desktop/CapstoneProject/scripts/Wapiti/wapiti10.py"
]

# Function to run each script
def run_script(script):
    try:
        subprocess.run(["python3", script], check=True)
        print(f"Successfully ran {script}")
    except subprocess.CalledProcessError as e:
        print(f"Error running {script}: {e}")

# Run all scripts
for script in scripts:
    run_script(script)
