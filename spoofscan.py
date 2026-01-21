#!/usr/bin/env python3

import subprocess
import time
import os
from lxml import etree
import datetime
import webbrowser


def run_nmap_scan(target, options, xml_output_file, spoofed_ip=None, interface=None):
    command = f'nmap {options} {target} -oX {xml_output_file}'

    if spoofed_ip and interface:
        command += f' -S {spoofed_ip} -e {interface}'  # Include -S for spoofed IP and -e for interface

    try:
        print(f"Executing command: {command}")
        result = subprocess.run(command, shell=True, text=True, capture_output=True)

        if result.returncode == 0:
            print("Nmap scan completed successfully.")
            return True
        else:
            print("Error occurred while running Nmap:")
            print(result.stderr)
            return False

    except Exception as e:
        print(f"An exception occurred: {str(e)}")
        return False


def transform_xml_to_html(xml_file, xslt_file, output_html_file):
    try:
        # Parse the XML and XSLT files
        xml_tree = etree.parse(xml_file)
        xslt_tree = etree.parse(xslt_file)

        # Apply the XSLT transformation
        transform = etree.XSLT(xslt_tree)
        html_tree = transform(xml_tree)

        # Save the output to an HTML file
        with open(output_html_file, "wb") as html_file:
            html_file.write(etree.tostring(html_tree, pretty_print=True, method="html", encoding="UTF-8"))
        print(f"HTML report generated: {output_html_file}")
    except Exception as e:
        print(f"Error occurred while transforming XML to HTML: {str(e)}")


def get_scan_frequency():
    while True:
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
                    print("Invalid unit. Please try again.")
            except ValueError:
                print("Invalid number format. Please try again.")
        else:
            print("Invalid format. Please try again.")


if __name__ == "__main__":
    if os.geteuid() != 0:
        print("This script must be run as root (i.e., with sudo).")
        exit(1)

    # Ensure the Nmap_Scans directory exists
    output_dir = "Nmap_Scans"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created directory: {output_dir}")

    target = input("Enter the target IP address or hostname: ")

    custom_options = input("Do you want to use custom Nmap options? (yes/no): ").strip().lower()

    if custom_options == 'yes':
        options = input("Enter your custom Nmap options, or press Enter for default options: ").strip()
        if not options:  # If no custom options are provided, use the default
            options = "-sS -sV -A -T4 -p- -Pn"
    else:
        options = "-sS -sV -A -T4 -p- -Pn"  # Default options

    spoof_choice = input("Do you want to spoof your source IP? (yes/no): ").strip().lower()
    spoofed_ip = None
    interface = None

    if spoof_choice == 'yes':
        spoofed_ip = input("Enter the spoofed IP address: ").strip()
        interface = input("Enter the network interface to use (e.g., eth0, en1): ").strip()

    scan_interval = get_scan_frequency()

    output_filename = input("Enter the base filename (e.g., 'results'): ").strip()

    if not output_filename:
        print("No filename provided. Using 'results' as default.")
        output_filename = "results"

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")
    xml_output_filename = os.path.join(output_dir, f"{output_filename}_{timestamp}.xml")
    html_output_filename = os.path.join(output_dir, f"{output_filename}_{timestamp}.html")
    xslt_filename = "nmap_to_html.xslt"

    print(f"Results will be saved as:\nXML: {xml_output_filename}\nHTML: {html_output_filename}")

    if not os.path.exists(xslt_filename):
        print(f"XSLT file '{xslt_filename}' not found. Please provide a valid XSLT file.")
        exit(1)

    while True:
        print("Running Nmap scan...")
        scan_success = run_nmap_scan(target, options, xml_output_filename, spoofed_ip, interface)

        if scan_success:
            print(f"Nmap scan saved to {xml_output_filename}.")
            transform_xml_to_html(xml_output_filename, xslt_filename, html_output_filename)
            webbrowser.open(f"file://{os.path.abspath(html_output_filename)}")

        print(f"Waiting for {scan_interval // 60} minutes before the next scan...")
        time.sleep(scan_interval)
