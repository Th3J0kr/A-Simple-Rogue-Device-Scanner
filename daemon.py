#!/usr/bin/env python3
#TODO:
    #Clean up logdir reading in conf
    #Add multi range support
    #Make sure low impact scan
    #Add whitelisting
    #Figure out the noise (type of scan?)

import net_scan
from net_scan import Scanner, DataManager
import time, os, sys, argparse
import datetime
import check_scans
from check_scans import CheckRogue, CheckInventory
import logging
from logging import Logger

class Main():
    def __init__(self):
        self.runTime = None
        self.ranges = []
        self.progPath = os.path.dirname(os.path.realpath(__file__))
        self.confFiles = ['main.conf']
        self.start = time.time()
        self.confD = self.checkConfig()
        self.logger = Logger(logpath=self.confD['logdir'])
        self.pid = self.checkPID()


    def checkPID(self):
        self.logger.writeToLog(text='Checking for PID file...', lType='startup')
        curPid = str(os.getpid())
        if os.path.isfile('my.pid'):
            self.logger.writeToLog(text='Found old PID file', lType='startup')
            fpid = open('my.pid', 'r')
            oldPid = fpid.read()
            fpid.close()

            if oldPid == curPid:
                self.logger.writeToLog(text='Already running with pid {}, exiting!'.format(curPid))
                sys.exit(0)
            else:
                self.logger.writeToLog(text='Old PID file, cleaning up...', lType='startup')
                os.remove('my.pid')
        if not os.path.isfile('my.pid'):
            self.logger.writeToLog(text='Writing out pid {}'.format(curPid), lType='startup')
            fpid = open('my.pid', 'w')
            fpid.write(curPid)
            fpid.close()
            return curPid

    def checkConfig(self):
        #self.logger.writeToLog('Checking my config files')
        for cFile in self.confFiles:
            confFile = os.path.join(self.progPath, 'conf', cFile)
            if os.path.isfile(confFile):
         #       self.logger.writeToLog('Reading {}'.format(confFile), lType='startup')
                with open(confFile, 'r') as f:
                    config = f.readlines()
                    self.confD = {}
                    for line in config:
                        lineL = line.split('    ')
                        confI = lineL[0]
                        confL = confI.split('=')
                        self.confD[confL[0]] = confL[1]
                        
                f.close()
                print(self.confD)
                return self.confD
            else:
          #      self.logger.writeToLog('Config file not found {}'.format(cFile), lType='startup')
                sys.exit(0)

    def main(self):
        
        self.logger.writeToLog(text='Starting Daemon...')
        
        self.ranges.append(self.confD['range']) #Fix this later
        while True:
            startTime = time.time()
            for ipRange in self.ranges:
                self.logger.writeToLog(text='Starting new scan')
                print('[*] starting scan on {}...'.format(ipRange))
                scanner = Scanner(ipRange)
                scanner.scan()

            end = time.time()
            self.logger.writeToLog(text='Scan completed in {} seconds'.format(end - startTime))
            print('\n[*] Scan completed in {} seconds\n'.format(end - startTime))
            self.logger.writeToLog('Checking scans...')
            checkrogue = CheckRogue()
            checkrogue.removeOld(int(self.confD['backlog']))
            newDevices = checkrogue.checkRogue()
            if newDevices:
                checkScans = CheckInventory(newDevices)
                checkScans.readInventory()
                checkScans.compareHosts(newDevices)
            else:
                self.logger.writeToLog('No new devices')

            self.logger.cleanupLogs(rotate=int(self.confD['logrotate']))
            print('[*] Sleeping for {} seconds...\n'.format(self.confD['wait']))
            time.sleep(int(self.confD['wait']))

if __name__ == '__main__':
    prog = Main()
    try:
        prog.main()
    except KeyboardInterrupt:
        if os.path.isfile('my.pid'):
            os.remove('my.pid')
            print('\r[!] Exiting!')