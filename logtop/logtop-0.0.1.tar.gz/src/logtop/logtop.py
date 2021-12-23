import sys
from loguru import logger
import inspect

def logsconfig(logfile=None, cmdout=True, formats=None, cmdlog_level=5, logfile_level=30, logstyle=None):
    logger.remove(0)
    if logfile is None and cmdout and formats is None:
        logger.add(sys.stderr, format="<level>{time:YYYY-MM-DD HH:mm:ss}</level>  |  <level>{level}</level>  |  <level>{extra[filename]}</level>  |  <level>func: {extra[function]}()</level>  | <level>{extra[line]}</level>: <level>{message}</level>", colorize=True,level=cmdlog_level)
    elif logfile is not None and formats is None:
        if cmdout:
            logger.add(sys.stderr, format="<level>{time:YYYY-MM-DD HH:mm:ss}</level>  |  <level>{level}</level>  |  <level>{extra[filename]}</level>  |  <level>func: {extra[function]}()</level>  | <level>{extra[line]}</level>: <level>{message}</level>", colorize=True,level=cmdlog_level)
            logger.add(logfile, format="<level>{time:YYYY-MM-DD HH:mm:ss:SSS}</level>  |  <level>{level}</level>  |  <level>{extra[filename]}</level>  |  <level>func: {extra[function]}()</level>  | <level>{extra[line]}</level>: <level>{message}</level>", colorize=False,level=logfile_level)
        else:
            logger.add(logfile, format="<level>{time:YYYY-MM-DD HH:mm:ss:SSS}</level>  |  <level>{level}</level>  |  <level>{extra[filename]}</level>  |  <level>func: {extra[function]}()</level>  | <level>{extra[line]}</level>: <level>{message}</level>", colorize=False,level=logfile_level)
    else:
        pass
        pass
    if logstyle is None:
        logger.level(name=' TRACE    ', no=5, color='<bold>')
        logger.level(name=' INFO     ', no=20, color='<cyan><bold>')
        logger.level(name=' SUCCESS  ', no=25, color='<green><bold>')
        logger.level(name=' DEBUG    ', no=30, color='<magenta><bold>')
        logger.level(name=' WARNING  ', no=35, color='<yellow><bold>')
        logger.level(name=' ERROR    ', no=50, color='<red><bold>')
        logger.level(name=' CRITICAL ', no=55, color='<RED><bold>')

def trace(msg):
    full_path = inspect.stack()[1][1]
    filename=full_path[full_path.rfind('/')+1:]
    try:
        context_logger = logger.bind(line=inspect.stack()[1][2],function=inspect.stack()[1][3],filename=filename)
        context_logger.log(' TRACE    ',msg)
    except ValueError:
        return logger.trace(msg)

def info(msg):
    full_path = inspect.stack()[1][1]
    filename=full_path[full_path.rfind('/')+1:]
    try:
        context_logger = logger.bind(line=inspect.stack()[1][2],function=inspect.stack()[1][3],filename=filename)
        return context_logger.log(' INFO     ',msg)
    except ValueError:
        return logger.info(msg)

def success(msg):
    full_path = inspect.stack()[1][1]
    filename=full_path[full_path.rfind('/')+1:]
    try:
        context_logger = logger.bind(line=inspect.stack()[1][2],function=inspect.stack()[1][3],filename=filename)
        return context_logger.log(' SUCCESS  ',msg)
    except ValueError:
        return logger.success(msg)

def debug(msg):
    full_path = inspect.stack()[1][1]
    filename=full_path[full_path.rfind('/')+1:]
    try:
        context_logger = logger.bind(line=inspect.stack()[1][2],function=inspect.stack()[1][3],filename=filename)
        return context_logger.log(' DEBUG    ',msg)
    except ValueError:
        return logger.debug(msg)

def warning(msg):
    full_path = inspect.stack()[1][1]
    filename=full_path[full_path.rfind('/')+1:]
    try:
        context_logger = logger.bind(line=inspect.stack()[1][2],function=inspect.stack()[1][3],filename=filename)
        return context_logger.log(' WARNING  ',msg)
    except ValueError:
        return logger.warning(msg)

def error(msg):
    full_path = inspect.stack()[1][1]
    filename=full_path[full_path.rfind('/')+1:]
    try:
        context_logger = logger.bind(line=inspect.stack()[1][2],function=inspect.stack()[1][3],filename=filename)
        return context_logger.log(' ERROR    ',msg)
    except ValueError:
        return logger.error(msg)

def critical(msg):
    full_path = inspect.stack()[1][1]
    filename=full_path[full_path.rfind('/')+1:]
    try:
        context_logger = logger.bind(line=inspect.stack()[1][2],function=inspect.stack()[1][3],filename=filename)
        return context_logger.log(' CRITICAL ',msg)
    except ValueError:
        return logger.critical(msg)

logsconfig()