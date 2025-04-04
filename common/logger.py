
class Logger:
    
    @staticmethod
    def log(message):
        Logger.write("INFO: ", message)
    
    @staticmethod
    def warn(message):
        Logger.write("WARN: ", message)

    @staticmethod
    def error(message):
        Logger.write("ERROR: ", message)
    
    @staticmethod
    def write(prefix, message):
        print(prefix + message)