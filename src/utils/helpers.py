import random
import re
from utils.logger import logger

def generate_OTP():
    code = ''.join(random.choices('0123456789', k=8))
    return code


def avoid_danger_in_json(**kwargs):
    """Escape the following characters from input: '";<>()--\\"""
    try:
        sanitized_kwargs = {key: re.sub(r'[()\"\'<>\\;]+|-{2}', '', value) if
                        isinstance(value, str) and key != 'password'
                        else value for key, value in kwargs.items()}
        return sanitized_kwargs
    except TypeError as e:
        logger.exception(e)
        return None
    except Exception as e:
        logger.exception(e)
        return None
