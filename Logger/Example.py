import logging
import ExIOwithOdi

custemFormat = '%(asctime)s %(filename)s %(funcName)s %(lineno)d %(message)s %(thread)d'

logging.basicConfig(filename='logFile.log', level=logging.DEBUG, format=custemFormat)
controller_to_log = logging.getLogger('ExIOwithOdi')
controller_to_log.setLevel(logging.INFO)

def main():
    try:
        logging.debug("in the main s loop")
        fail = 1 / 0
    except Exception as e:
        logging.critical(str(e))


main()
ExIOwithOdi.foo()
