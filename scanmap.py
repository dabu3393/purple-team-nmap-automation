#!/usr/bin/env python3

import subprocess
import time

def run_nmap_scan(target, options=''):
    command = f'nmap {options} {target}'
    
    try:
        result = subprocess.run(command, shell=True, text=True, capture_output=True)
        
        if result.returncode == 0:
            print("Nmap scan completed successfully.")
            return result.stdout
        else:
            print("Error occurred while running Nmap:")
            print(result.stderr)
            return None

    except Exception as e:
        print(f"An exception occurred: {str(e)}")
        return None

def get_scan_frequency():
    frequency_input = input("Enter scan frequency (number followed by 'minute(s)', 'hour(s)', or 'day(s)'): ")
    parts = frequency_input.split()
    
    if len(parts) == 2:
        try:
            count = int(parts[0])
            unit = parts[1].lower()
            
            if 'minute' in unit:
                return count * 60
            elif 'hour' in unit:
                return count * 3600
            elif 'day' in unit:
                return count * 86400
            else:
                print("Invalid unit. Defaulting to 1 hour.")
                return 3600
        except ValueError:
            print("Invalid number format. Defaulting to 1 hour.")
            return 3600
    else:
        print("Invalid format. Defaulting to 1 hour.")
        return 3600

if __name__ == "__main__":
    target = input("Enter the target IP address or hostname: ")
    
    options = "-sS -sV -A -T4 -p-"
    
    scan_interval = get_scan_frequency()
    
    output_filename = input("Enter the name of the file to save results (e.g., 'results.txt'): ")
    
    if not output_filename.strip():
        print("No filename provided. Using 'results.txt' as default.")
        output_filename = "results.txt"

    while True:
        print("Running Nmap scan...")
        scan_result = run_nmap_scan(target, options)
        
        if scan_result:
            print(scan_result)
            with open(output_filename, "a") as file:
                file.write(f"Nmap scan results for {target}:\n")
                file.write(scan_result)
                file.write("\n" + "-" * 60 + "\n")
            
        print(f"Waiting for {scan_interval // 60} minutes before the next scan...")
        time.sleep(scan_interval)
