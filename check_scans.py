import os, sys, csv
from logging import Logger

class CheckRogue:
    def __init__(self):
        self.logger = Logger()
        self.logger.writeToLog('starting rogue checking...')
        pass
    
    def removeOld(self, backlog=10):
        scanDir = 'scans/'
        scans = os.listdir(scanDir)
        if len(scans) > backlog:
            oldestL = []
            self.logger.writeToLog('Sorting scans')
            for scan in scans:
                scanTL = scan.split('.')
                oldestL.append(scanTL[0])
            
            oldestL.sort()
         
            i = 0            
            while i < (len(oldestL) - backlog):
                self.logger.writeToLog('Removing {}'.format(oldestL[i]))
                os.remove(os.path.join(scanDir, oldestL[i] + '.csv'))
                i += 1

    def checkRogue(self):
        self.logger.writeToLog('Checking for rogue devices')
        scanDir = 'scans/'
        scans = os.listdir(scanDir)
        scans.sort()
        file1 = os.path.join(scanDir, scans[len(scans) - 1 ])
        file2 = os.path.join(scanDir, scans[len(scans) - 2 ])
        f1 = open(file1, 'r')
        csvReader1 = csv.reader(f1)
        f2 = open(file2, 'r')
        csvReader2 = csv.reader(f2)

        self.logger.writeToLog('Comparing scan {} and {}'.format(scans[len(scans) - 1 ], scans[len(scans) - 2 ]))
        next(csvReader1)
        next(csvReader2)
        ips1 = {}
        ips2 = {}
        for row in csvReader1:
            if row[1]:
                ips1[row[0]] = row[1]
            else:
                ips1[row[0]] = row[0]
        for row in csvReader2:
            if row[1]:
                ips2[row[0]] = row[1]
            else:
                ips2[row[0]] = row[0]
       
        rogueDevices = {}
        for ip, host in ips1.items():
            if ip not in ips2.keys():
                self.logger.writeToLog(text='New device found: {} : {}'.format(ip, host), lType='rogue')
                rogueDevices[ip] = host
                
        if rogueDevices:
            self.logger.writeToLog('New rogue devices discovered... check "rogue" log file!')
            print('[!] New device found: {}'.format(rogueDevices))
            
        f1.close()
        f2.close()


if __name__ == '__main__':
    checkRogue = CheckRogue()
    checkRogue.removeOld()
    checkRogue.checkRogue()