import logging

logger = logging.getLogger(__name__)

logger.setLevel(logging.INFO)

class InfoHandler(logging.FileHandler):
    """Handler for info logs only"""
    def emit(self, record):
        if record.levelno == logging.INFO:
            super().emit(record)

class ErrorHandler(logging.FileHandler):
    """Handler for error logs and critical logs"""
    def emit(self, record):
        if record.levelno >= logging.ERROR:
            super().emit(record)


# Create handlers
info_handler = InfoHandler(filename='../.logs/info.log',
                                   mode='a', encoding='utf-8')
error_logger = ErrorHandler(filename='../.logs/error.log',
                                   mode='a', encoding='utf-8')

# Create formatter and add it to handlers
format = logging.Formatter('%(asctime)s - %(filename)s - %(lineno)d - %(levelname)s - %(message)s')
info_handler.setFormatter(format)
error_logger.setFormatter(format)

# Add handlers to the logger
logger.addHandler(info_handler)
logger.addHandler(error_logger)
