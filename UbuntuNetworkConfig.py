#!/usr/bin/env python3

import os
import subprocess
import yaml
import glob

def get_netplan_files():
    """
    Detects and returns a list of Netplan configuration files.

    Returns:
        list: A list of Netplan configuration file paths.
    """
    netplan_dir = '/etc/netplan/'
    netplan_files = glob.glob(netplan_dir + '*')
    return netplan_files

def select_netplan_file(netplan_files):
    """
    Presents a list of detected Netplan files to the user and allows them to select one.

    Args:
        netplan_files: A list of Netplan configuration file paths.

    Returns:
        str: The path of the selected Netplan file.
    """
    if not netplan_files:
        print("No Netplan configuration files found.")
        return None

    print("Detected Netplan files:")
    for i, file in enumerate(netplan_files):
        print(f"{i+1}. {file}")

    while True:
        try:
            choice = int(input("Select the Netplan file to modify (enter the number): "))
            if 1 <= choice <= len(netplan_files):
                return netplan_files[choice - 1]
            else:
                print("Invalid choice. Please select a number from the list.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def get_user_input():
    """
    Prompts the user for network configuration details.

    Returns:
        tuple: A tuple containing the network adapter name, IP address, subnet mask, gateway, and DNS servers.
    """
    adapter = input("Enter network adapter name (e.g., ens18): ")
    ip = input("Enter IP address (e.g., 192.168.1.100): ")
    subnet = input("Enter subnet mask (e.g., 24): ")
    gateway = input("Enter gateway IP address (e.g., 192.168.1.1): ")
    dns_servers = input("Enter DNS server addresses (comma-separated, e.g., 8.8.8.8,1.1.1.1): ")

    return adapter, ip, subnet, gateway, dns_servers

def generate_netplan_config(adapter, ip, subnet, gateway, dns_servers):
    """
    Generates the Netplan YAML configuration based on user input.

    Args:
        adapter: Network adapter name.
        ip: IP address.
        subnet: Subnet mask.
        gateway: Gateway IP address.
        dns_servers: Comma-separated list of DNS server addresses.

    Returns:
        str: The generated YAML configuration.
    """
    dns_server_list = dns_servers.split(',')
    config = f"""
network:
  version: 2
  renderer: networkd
  ethernets:
    {adapter}:
      addresses: [{ip}/{subnet}]
      gateway4: {gateway}
      nameservers:
        addresses: {dns_server_list}
    """
    return config

def save_netplan_config(config, filename):
    """
    Saves the generated YAML configuration to the specified Netplan file.

    Args:
        config: The YAML configuration string.
        filename: The path to the Netplan file.
    """
    with open(filename, 'w') as f:
        f.write(config)

def confirm_action(message):
    """
    Asks the user to confirm an action.

    Args:
        message: The message to display to the user.

    Returns:
        bool: True if the user confirms, False otherwise.
    """
    while True:
        response = input(f"{message} (yes/no): ").lower()
        if response in ['yes', 'y']:
            return True
        elif response in ['no', 'n']:
            return False
        else:
            print("Invalid input. Please enter 'yes' or 'no'.")

def apply_netplan_config():
    """
    Applies the Netplan configuration.
    """
    subprocess.run(['sudo', 'netplan', 'apply'])

def main():
    """
    Main function to execute the script.
    """
    netplan_files = get_netplan_files()
    selected_file = select_netplan_file(netplan_files)

    if selected_file:
        adapter, ip, subnet, gateway, dns_servers = get_user_input()
        config = generate_netplan_config(adapter, ip, subnet, gateway, dns_servers)

        if confirm_action(f"Write configuration to {selected_file}? "):
            save_netplan_config(config, selected_file)

            if confirm_action("Apply Netplan configuration?"):
                apply_netplan_config()

if __name__ == "__main__":
    main()