# Test Switch Compliance
This folder contains the scripts to automatically test after changes have been made. 

## File Structure
The folder contains 3 files that are relevant for the test execution:

* **test_file.py**: this file contains the different sections to be executed, incluiding a setup, test sections and a cleaning section. Each of them are defined following the indications from the [Aetest documentation](https://pubhub.devnetcloud.com/media/pyats/docs/aetest/index.html), and as observed they are defined as clasess and subclasess with *@markers* for the further test execution. This file is where you should define the actions taken by your tests and depending on the information gathered if they are succesful or not.

* **test_file_job.py**: the job file is necessary as we will be running the test scripts with the help of easypy and it requires to use the run function included in a main function. Remember to define the correct path to the *test_file.py* file.


## Execution

The execution is done using [easypy](https://pubhub.devnetcloud.com/media/pyats/docs/easypy/introduction.html) which is a pyATS moduled designed to make the execution of pyATS jobs easier. 
