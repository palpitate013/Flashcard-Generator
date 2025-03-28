#!/usr/bin/env python3

import os
import subprocess
import sys
import venv
import threading
import signal
import pkg_resources
import importlib.util

# List of standard Python modules (built-in modules that don't need installation)
standard_libs = set([
    'os', 'sys', 'time', 'datetime', 'math', 'json', 'argparse', 're', 'platform', 'logging', 'socket', 'http', 'email',
    # Add more built-in modules here if needed
])

# Function to check if a virtual environment exists
def check_virtualenv(env_name):
    return os.path.exists(env_name)

# Function to create a new virtual environment
def create_virtualenv(env_name):
    venv.create(env_name, with_pip=True)
    print(f"Virtual environment '{env_name}' created successfully.")

# Function to run a command in the virtual environment
def run_in_virtualenv(env_name, command):
    # Determine the path to the virtual environment's Python executable
    env_python = os.path.join(env_name, 'Scripts', 'python') if os.name == 'nt' else os.path.join(env_name, 'bin', 'python')

    if not os.path.exists(env_python):
        raise FileNotFoundError(f"The Python interpreter in the virtual environment was not found at: {env_python}")

    # Prepend the virtual environment's Python executable to the command
    full_command = [env_python] + command

    print(f"Running command in virtual environment: {' '.join(full_command)}")
    result = subprocess.run(full_command, capture_output=True, text=True)

    # Print output and errors
    print(result.stdout)
    if result.stderr:
        print(result.stderr, file=sys.stderr)

    return result.returncode

# Function to install missing modules from a given list of imports
def install_missing_modules(env_name, files):
    # Collect imports from the provided Python files
    imports = set()
    for file in files:
        with open(file, 'r') as f:
            content = f.read()
            for line in content.splitlines():
                if line.startswith("import") or line.startswith("from"):
                    module = line.split()[1].split('.')[0]  # Get module name
                    imports.add(module)

    # Get the Python executable for the virtual environment
    env_python = os.path.join(env_name, 'Scripts', 'python') if os.name == 'nt' else os.path.join(env_name, 'bin', 'python')

    # Get a list of installed packages in the virtual environment
    result = subprocess.run([env_python, "-m", "pip", "freeze"], capture_output=True, text=True)
    installed_packages = {line.split('==')[0].lower() for line in result.stdout.splitlines()}

    # Filter out standard library modules from the list of modules to install
    missing_modules = {module for module in imports if module not in standard_libs and module.lower() not in installed_packages}

    if missing_modules:
        print(f"Installing missing modules: {', '.join(missing_modules)}")
        # Install missing modules
        subprocess.check_call([env_python, "-m", "pip", "install"] + list(missing_modules))
    else:
        print("All required modules are already installed.")

# Function to run the script files in parallel using threads
def run_files_parallel(env_name, files):
    threads = []
    for file in files:
        thread = threading.Thread(target=run_in_virtualenv, args=(env_name, [file]))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

# Function to handle keyboard interrupt (Ctrl+C) and clean up
def signal_handler(sig, frame):
    print("\nKeyboardInterrupt received. Shutting down.")
    sys.exit(0)

# Main script execution
def main():
    # Path to the virtual environment
    env_name = 'venv'

    # Step 1: Check if the virtual environment exists
    if not check_virtualenv(env_name):
        print(f"Virtual environment '{env_name}' does not exist. Creating it now...")
        create_virtualenv(env_name)

    # Step 2: Scan the Python files for missing modules and install them
    files_to_scan = ['', '']  # Put file names that you want to run here
    install_missing_modules(env_name, files_to_scan)

    # Step 3: Run the files using threading
    run_files_parallel(env_name, files_to_scan)

# Register the signal handler for keyboard interrupt (Ctrl+C)
signal.signal(signal.SIGINT, signal_handler)

# Run the script
if __name__ == "__main__":
    main()
