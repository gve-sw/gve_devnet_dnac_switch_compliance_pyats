"""
Copyright (c) 2021 Cisco and/or its affiliates.

This software is licensed to you under the terms of the Cisco Sample
Code License, Version 1.1 (the "License"). You may obtain a copy of the
License at

               https://developer.cisco.com/docs/licenses

All use of the material herein must be in accordance with the terms of
the License. All rights not expressly granted by the License are
reserved. Unless required by applicable law or agreed to separately in
writing, software distributed under the License is distributed on an "AS
IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied.
"""

from dnacentersdk import DNACenterAPI
from env_var import dnac_username, dnac_password, dnac_url
import yaml
import sys

def get_device_list(dnac_username, dnac_password, dnac_url):
    # Obtain a list of devices from DNAC
    api = DNACenterAPI(username=dnac_username, password=dnac_password, base_url=dnac_url, verify=False)
    device_list = api.devices.get_device_list()['response']
    return device_list

def create_testbed_file(device_list, device_filter, testbed_filename):
    # Create a testbed file using a device list from DNAC 
    filtered_device_list = []
    for device in device_list:
        # For this usecase: device_filter = 'Switches and Hubs'
        if device['family'] == device_filter:
            filtered_device_list.append(device)

    # Store the devices in a dictionary and write the dictionary to the testbed
    devices_dict = {}
    for device in filtered_device_list:
        try:
            hostname = device['hostname']
            ip = device['managementIpAddress']

            device_dict = {
                'connections': {
                    'cli': {
                        'ip': ip,
                        'protocol': 'ssh'
                    }
                },
                'os': 'iosxe', 
                'type': 'iosxe',
                'credentials': {
                    'default': {
                        'username': dnac_username,
                        'password': dnac_password
                    }
                }
            }
            devices_dict[hostname] = device_dict
        except Exception as e:
            print(e)
            print(f"Exception in parsing filtered_device_list for device {device['hostname']}")
            return 0
    
    testbed_dict = {
        'devices': devices_dict
    }

    with open(testbed_filename, 'w') as testbed_file:
        yaml.dump(testbed_dict, testbed_file, default_flow_style=False)
    return 1

if __name__ == "__main__":
    # Example usage:
    # $ python3 create_testbed_from_dnac_inventory.py testbed-test.yaml

    # Provide the testbed filename as an argument
    testbed_file_name = sys.argv[1]
    # Obtain a list of devices from DNAC
    device_list = get_device_list(dnac_username, dnac_password, dnac_url)
    # Filter out the switches and hubs
    device_filter = 'Switches and Hubs'
    # Create a testbed file and check whether it was successful or not
    if create_testbed_file(device_list, device_filter, testbed_file_name):
        print(f"Successfully created a testbed file with name: {testbed_file_name}")
    else:
        print("Error! We could not successfully create a testbed file")




    
    
    





