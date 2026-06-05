class Logger:
    def log(self, message):
        pass
class FileLogger:
    def log(self, message):
        return f"File: {message}"
class ConsoleLogger(FileLogger):
    def log(self, message):
        return f"Console: {message}"
class ServerLogger(FileLogger):
    def log(self, message):
        return f"Server: {message}"
class NetworkMonitor:
    def __init__(self, logger:FileLogger):
        self.logger=logger
    def check(self):
        return self.logger.log('мережа працює')
log1=ConsoleLogger()
log2=ServerLogger()
log3=FileLogger()
monitor1=NetworkMonitor(log1)
monitor2=NetworkMonitor(log2)
monitor3=NetworkMonitor(log3)
print(monitor1.check()) 
print(monitor2.check()) 
print(monitor3.check()) 