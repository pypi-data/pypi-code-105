template="""
from app import app, cmd
from boa.core.bootstrap import bootstrap


bootstrap(app, None, ["cmd"])


if __name__== '__main__':
    cmd.run()

"""
