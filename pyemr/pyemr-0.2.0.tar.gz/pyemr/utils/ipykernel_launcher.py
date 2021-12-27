"""Entry point for launching an IPython kernel.

This is separate from the ipykernel package so we can avoid doing imports until
after removing the cwd from sys.path.
"""
import sys


# spark.conf.set("spark.sql.legacy.timeParserPolicy","LEGACY")
# spark.sql("set spark.sql.legacy.timeParserPolicy=LEGACY")

if __name__ == "__main__":
    sys.path += sys.argv[1].split(",")
    from pyemr.utils.poetry import set_spark_home
    set_spark_home()
    # Remove the CWD from sys.path while we load stuff.
    # This is added back by InteractiveShellApp.init_path()
    from pyemr.utils.mocking import launch_kernelapp
    # get additional site package paths
    
    if sys.path[0] == "":
        del sys.path[0]
    
    launch_kernelapp()
