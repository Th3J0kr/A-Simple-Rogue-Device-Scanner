import os, sys, io, datetime

class Logger:
    def __init__(self, logpath='logs/'):
        self.logpath = logpath

    def writeToLog(self, text="", lType="info"):
        
        if not os.path.isdir(self.logpath):
            print('[!] Log directory not found, creating...')
            os.mkdir(self.logpath)
        logDir = os.path.join(self.logpath, lType)
        if not os.path.isdir(logDir):
            os.mkdir(logDir)
        timestamp = str(int(datetime.datetime.now().timestamp()))
        text = str(datetime.datetime.now()) + ' - ' + text + '\n'
        logFile = logDir + '/' + str(datetime.date.today()) + '.log'
        f = open(logFile, 'a')
        f.write(text)
        f.close()
        return
    
    def cleanupLogs(self, rotate=1):
        self.writeToLog('Checking logs')
        if os.path.isdir(self.logpath):
            logdirs = os.listdir(self.logpath)
            now = datetime.datetime.now()
            earliest = now - datetime.timedelta(days=rotate)
            for logdir in logdirs:
                logfiles = os.listdir(os.path.join(self.logpath, logdir))
                if logfiles:
                    for logfile in logfiles:
                        modDate = datetime.datetime.fromtimestamp(os.path.getmtime(os.path.join(self.logpath, logdir, logfile)))
                        if modDate < earliest:
                            print('[!] Old log file found {} in {} logs'.format(logfile, logdir))
                            self.writeToLog('Removing old log file {} from {} logs'.format(logfile, logdir))
                            os.remove(os.path.join(self.logpath, logdir, logfile))
                else:
                    self.writeToLog('No logs yet!')
        else:
            self.writeToLog('No logs yet!')
                        

if __name__ == '__main__':
    logger = Logger()
    logger.cleanupLogs()
