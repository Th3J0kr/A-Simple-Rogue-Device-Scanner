import os, sys, csv, datetime
from logging import Logger
import socket

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
        ipL = []
        for ip, host in ips1.items():
            if ip not in ips2.keys():
                self.logger.writeToLog(text='New device found: {} : {}'.format(ip, host), lType='rogue')
                rogueDevices[ip] = host
                ipL.append(ip)
                
        if rogueDevices:
            self.logger.writeToLog('New rogue devices discovered... check "rogue" log file!')
            print('[!] New device found: {}'.format(rogueDevices))
            return ipL
            
        f1.close()
        f2.close()

class CheckInventory:
    def __init__(self, ipL=[]):
        self.ipL = ipL
        self.logger = Logger()
        self.hostI = {}

    def readInventory(self):
        if not os.path.isdir('data'):
            self.logger.writeToLog('No inventory creating one!')
            os.mkdir('data')
        filePath = os.path.join('data', 'inventory.csv')
        self.logger.writeToLog('Checking inventory file {}'.format(filePath))

        if not os.path.isfile(filePath): #os.stat(filePath).st_size == 0:
            with open(filePath, 'w') as f:
                fieldnames = ['ip', 'host', 'first_seen', 'last_seen']
                writer = csv.DictWriter(f, fieldnames=fieldnames)

                writer.writeheader()
            f.close()
            self.logger.writeToLog('Log file was empty! Wrote header to new file.')

        else:
            with open(filePath, 'r') as f:
                csvReader = csv.reader(f)
                next(csvReader)
                for row in csvReader:
                    self.hostI[row[0]] = row
            f.close()
        return self.hostI

    def compareHosts(self, ipL=[]):
        if not ipL:
            ipL = self.ipL
        print('pre check inventory')
        print(self.hostI)

        if ipL:
            for ip in ipL:
                if ip not in self.hostI:
                    self.logger.writeToLog('Updating inventory with {}'.format(ip))
                    try:
                        host = socket.gethostbyaddr(ip)
                        self.hostI[ip] = [ip, host[0], str(datetime.datetime.now()), str(datetime.datetime.now())]
                    except:
                        self.hostI[ip] = [ip, ip, str(datetime.datetime.now()), str(datetime.datetime.now())]
                else:
                    self.hostI[ip][3] = str(datetime.datetime.now())

            filePath = os.path.join('data', 'inventory.csv')
            f = open(filePath, 'w')
            fieldnames = ['ip', 'host', 'first_seen', 'last_seen']

            csvWriter = csv.writer(f)
            csvWriter.writerow(fieldnames)
            # print(self.hostI)
            # sys.exit(0)
            for ip, row in self.hostI.items():
                csvWriter.writerow(row)
            f.close()

        else:
            print('No new devices')
        print('Current inventory:')
        print(self.hostI)
        


if __name__ == '__main__':
    checkRogue = CheckRogue()
    checkRogue.removeOld()
    checkRogue.checkRogue()