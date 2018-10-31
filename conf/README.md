# A Simple Rogue Device Scanner

This is just a simple python program that runs ping sweeps/simple nmap scans across a subnet every X seconds and reports any new devices.

##### Disclaimer: This is still very much in development

## Installation

aSRDS uses mostly the python standard library except for `python-nmap`. Just run `pip3 install python-nmap` or `pip install -r requirements.txt` to install dependencies.

Make sure nmap is installed on your system as well as python 3 (3.7 would be ideal).

Not sure if it works on windows, only been tested on linux.

## Configuration

You can edit things like where the logs are stored and what range to scan in the `conf/main.conf` file.

## Usage

Once you have configured your settings as needed simply run `python3 daemon.py` to start the deamon.

By default logs are written to the logs directory:

* logs
    * info
        * general logs from the program
    * rogue
        * where information about new devices is written
    * startup
        * information about the startup is written (pid, conf file path)

I run it in a screen (`screen -S aSRDS -d -m python3 daemon.py`) and then use syslog to forward the logs to a log server where I can monitor them more easily.

Hope you can find a good use for it!

-- Th3J0kr