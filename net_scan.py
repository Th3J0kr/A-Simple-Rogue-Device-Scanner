#!/usr/bin/env python3

import os, sys, nmap, argparse, datetime, socket, csv, datetime, time

class Scanner():
    def __init__(self, ips):
        self.ips = ips
        self.hostL = []
    
    def scan(self):      

        nm = nmap.PortScanner()

        nm.scan(hosts=self.ips, arguments='-n -sP -PE -PA21,23,80,3389')
        hosts_list = [(x, nm[x]['status']['state']) for x in nm.all_hosts()]
        #daemon.Main.writeToLog(text='Scan complete')
        dataM = DataManager()
        
        print()
        print('[*] Processing scan info...')

        for host, status in hosts_list:    
            self.hostL = dataM.process(host, status)

        dataM.write(self.hostL)

class DataManager():
    def __init__(self):
        self.date = '{}-{}-{}'.format(datetime.datetime.now().month, datetime.datetime.now().day, datetime.datetime.now().year)
        self.ts = str(int(datetime.datetime.now().timestamp()))
        self.wDir = os.path.dirname(os.path.realpath(__file__)) + '/scans/'
        self.wFileName = os.path.join(self.wDir, self.ts + '_scan.csv')
        self.hostL = []
        self.inHosts = []

        if not os.path.isdir(self.wDir):
            os.mkdir(self.wDir)

    def process(self, ip, status):
        ts = datetime.datetime.now().timestamp()
        try:
            hostname = socket.gethostbyaddr(ip)
            hostname = hostname[0]
           
            self.hostL.append({'ip' : ip, 'hostname(s)' : hostname, 'last_seen' : ts})

        except:
            self.hostL.append({'ip' : ip, 'hostname(s)' : "", 'last_seen' : ts})
        return self.hostL

    def write(self, hostL):
        filename = self.wFileName
        fields = ['ip', 'hostname(s)', 'last_seen', 'first_seen']
        with open(filename, 'w') as f:
            print('\n[*] Writing to file')
            fileWriter = csv.DictWriter(f, fieldnames=fields)
            fileWriter.writeheader()
            for host in self.hostL:
                fileWriter.writerow(host)
        f.close()
