#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: n00B-ToT(shengta66396@163.com)

import logging 

class ColoredFormatter(logging.Formatter):
    colors = {'black': 30,'red': 31,'green': 32,'yellow': 33,'blue': 34,'magenta': 35,'cyan': 36,'white': 37,'bgred': 41,'bggrey': 100 }
    mapping = {'INFO': 'cyan','WARNING': 'yellow','ERROR': 'red','CRITICAL': 'bgred','DEBUG': 'bggrey','SUCCESS': 'green'}
    prefix = '\033['
    suffix = '\033[0m'

    def colored(self, text, color=None):
        if color not in self.colors: color = 'white'
        return (self.prefix+'%dm%s'+self.suffix) % (self.colors[color], text)

    def format(self, record):
        log_fmt = self.colored(record.levelname, self.mapping.get(record.levelname, 'white'))+" - %(asctime)s - process: %(process)d - %(filename)s - %(name)s - %(lineno)d - %(module)s - %(message)s"
        return logging.Formatter(log_fmt).format(record)

    def CusGetLogger(cus_color:int , cus_level:str , cus_level_name :str , custom_level_num:int):
        """ 
        cus_color          color num        example : 32
            https://stackoverflow.com/questions/5947742/how-to-change-the-output-color-of-echo-in-linux
        cus_level          Level            example : NMD
        cus_level_name     just custom_name example : nmd  
        custom_level_num   Numeric value    example : 29 
        """
        logger = logging.getLogger(__name__)
        handler = logging.StreamHandler()
        cf = ColoredFormatter()
        cf.mapping.update({cus_level:'custom'})
        cf.colors.update({'custom':cus_color})
        handler.setFormatter(cf)
        logger.addHandler(handler)
        logging.cus_level = custom_level_num  # between WARNING and INFO
        logging.addLevelName(logging.cus_level, cus_level)
        setattr(logger, cus_level_name , lambda message, *args: logger._log(logging.cus_level, message, args))
        logger.setLevel(logging.cus_level)
        return logger

    def add_level(logger , level_name , level_num  , cf_instance , cus_color ):
        handler = logging.StreamHandler()
        handler.setFormatter(cf_instance)
        level_name = level_name.upper()
        _low_level_name = level_name.lower()
        cf_instance.mapping.update({ level_name : 'custom_add' })
        cf_instance.colors.update({'custom_add':cus_color})
        logging.level_name = level_num
        logging.addLevelName(logging.level_name , level_name )
        setattr(logger ,_low_level_name ,  lambda message, *args: logger._log(logging.level_name, message, args))
        return logger


    def GetLogger():
        logger = logging.getLogger(__name__)
        handler = logging.StreamHandler()
        cf = ColoredFormatter()
        handler.setFormatter(ColoredFormatter())
        logger.addHandler(handler)
        logging.SUCCESS = 25 
        logging.addLevelName(logging.SUCCESS, 'SUCCESS')
        setattr(logger, 'success', lambda message, *args: logger._log(logging.SUCCESS, message, args))
        logger.setLevel(logging.INFO)
        return logger