import logging

logger = logging.getLogger(__name__)



def foo():
    logger.info("This is a info msg")
    logger.debug("This is a debug msg")
    return 1

foo()