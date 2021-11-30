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

#!/bin/env python

# To get a logger for the script
import logging

# To build the table at the end
from tabulate import tabulate

# Needed for aetest script
from pyats import aetest
from pyats.log.utils import banner

# Genie Imports
from genie.conf import Genie

# Get your logger for your script
log = logging.getLogger(__name__)

import os, sys


currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)


###################################################################
#                  COMMON SETUP SECTION                           #
###################################################################

class common_setup(aetest.CommonSetup):
    """ Common Setup section """

    # Connect to each device in the testbed
    @aetest.subsection
    def connect(self, testbed):
        # Get specified testbed
        genie_testbed = Genie.init(testbed)
        # Save in environment variables
        self.parent.parameters['testbed'] = genie_testbed
        device_list = []
        # Try connect one by one and save device objects in a list
        for device in genie_testbed.devices.values():
            # Only connect to the access and core devices
            if 'external' in device.name:
                continue
            log.info(banner(
                "Connect to device '{d}'".format(d=device.name)))
            try:
                device.connect(init_exec_commands=[], init_config_commands=[], log_stdout=False)
            except Exception as e:
                self.failed("Failed to establish connection to '{}'".format(
                    device.name))
            # Add device to list
            device_list.append(device)
        # Pass list of devices the to testcases
        self.parent.parameters.update(dev=device_list)



###################################################################
#                     TESTCASES SECTION                           #
###################################################################

# Test case definition, you can implement as many as you desire
class show_commands(aetest.Testcase):
    @aetest.test
    def show_cts_test(self):
        results_list = []
        for dev in self.parent.parameters['dev']:
            # Define the commands that you would like to parse
            commands = [
                "show cts"
            ]
            for command in commands:
                try: 
                    output = dev.parse(command)
                    log.info(output)
                    if command == "show cts":
                        cts_role_based = output["ip_sgt_bindings"]["cts_role_based_enforcement"]
                        print(f"dev name {dev.name}")
                        results_list.append([dev.name, cts_role_based])
                        log.info(f"cts_role_based: {cts_role_based}")

                        ## Automatically enable the cts role-based enforcement if needed

                        # if cts_role_based == "Disabled":
                        #     dev.configure("cts role-based enforcement")
                        # output = dev.parse(command)
                        # log.info(f'cts_role_based: {output["ip_sgt_bindings"]["cts_role_based_enforcement"]}')

                except Exception as e:
                    log.warning(f"Exception: We could not execute the following command {command} due to the following reason:")
                    log.warning(e)

        log.warning(banner("Results of 'cts role-based enforcement' per switch"))
        log.warning(results_list)
        log.warning(" ")
        log.warning(tabulate(results_list, headers=["switch", "status"]))
        log.warning(" ")

        # note: also possible to write the results to a file

        for result in results_list:
            if "Disabled" in result:
                # In case there is a switch with 'cts role-based enforcement' disabled, then the test fails
                self.failed("On one of the switches, the 'cts role-based enforcement' was disabled")
        # In case all switches have 'cts role-based enforcement' enabled, then the test passes
        self.passed("All switches have 'cts role-based enforcement' enabled")

                
# #####################################################################
# ####                       COMMON CLEANUP SECTION                 ###
# #####################################################################


class common_cleanup(aetest.CommonCleanup):
    """ Common Cleanup for Sample Test """

    @aetest.subsection
    def clean_everything(self):
        """ Common Cleanup Subsection """
        log.info("Aetest Common Cleanup ")

        for dev in self.parent.parameters['dev']:
            log.info(f"Disconnecting from {dev.name} ")
            dev.disconnect()
            log.info(f"Successfully disconnected from {dev.name} ")


if __name__ == '__main__':  # pragma: no cover
    aetest.main()
