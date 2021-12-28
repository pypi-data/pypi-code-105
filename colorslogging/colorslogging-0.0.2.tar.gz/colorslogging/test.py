from colorslogging import ColoredFormatter
import logging  

logger = ColoredFormatter.GetLogger()
logger.info("test")
logger.setLevel(logging.SUCCESS)
logger.info("test")
logger.success("test")
logger = ColoredFormatter.add_level(logger = logger , level_name = 'nmb' ,level_num = 45 , cf_instance=ColoredFormatter() ,  cus_color = 100 )
logger.nmb('cao')