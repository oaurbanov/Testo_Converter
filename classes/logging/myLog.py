import logging
import datetime


class myLogClass(object):
    '''Logging class'''
    def __init__(self, args):
        self.__type = args['type']
        self.__verbose = args['verb']  # verbose: 0 clean; 1 error; 2 full
        logging.basicConfig(filename=args['logsFile'], level=logging.DEBUG)

    def timeStamp(self):
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def logInfo(self, stringy):
        stringy = str(stringy)
        to_print = " %s %s %s" % (self.timeStamp(), self.__type, stringy)
        logging.info(to_print)
        if self.__verbose >= 2:
            print (to_print)

    def logExc(self, stringy):
        stringy = str(stringy)
        to_print = " %s %s %s" % (self.timeStamp(), self.__type, stringy)
        logging.exception(to_print)
        if self.__verbose >= 1:
            print (to_print)

    def logCritical(self, stringy):
        stringy = str(stringy)
        to_print = " %s %s %s" % (self.timeStamp(), self.__type, stringy)
        logging.critical(to_print)
        if self.__verbose >= 1:
            print (to_print)
