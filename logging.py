import os, sys, io, datetime

class Logger:

    def writeToLog(self, text="", lType="info"):
        logPath = 'logs/' + lType
        if not os.path.isdir('logs'):
            print('[!] Log directory not found, creating...')
            os.mkdir('logs')
        if not os.path.isdir(logPath):
            os.mkdir(logPath)
        timestamp = str(int(datetime.datetime.now().timestamp()))
        text = str(datetime.datetime.now()) + ' - ' + text + '\n'
        logFile = logPath + '/' + str(datetime.date.today()) + '.log'
        f = open(logFile, 'a')
        f.write(text)
        return
    
    def cleanupLogs(self, logpath='logs/', rotate=1):
        self.writeToLog('Checking logs')
        if os.path.isdir(logpath):
            logdirs = os.listdir(logpath)
            now = datetime.datetime.now()
            earliest = now - datetime.timedelta(days=rotate)
            for logdir in logdirs:
                logfiles = os.listdir(os.path.join(logpath, logdir))
                if logfiles:
                    for logfile in logfiles:
                        modDate = datetime.datetime.fromtimestamp(os.path.getmtime(os.path.join(logpath, logdir, logfile)))
                        if modDate < earliest:
                            print('[!] Old log file found {} in {} logs'.format(logfile, logdir))
                            self.writeToLog('Removing old log file {} from {} logs'.format(logfile, logdir))
                            os.remove(os.path.join(logpath, logdir, logfile))
                else:
                    self.writeToLog('No logs yet!')
        else:
            self.writeToLog('No logs yet!')
                        

if __name__ == '__main__':
    logger = Logger()
    logger.cleanupLogs()
