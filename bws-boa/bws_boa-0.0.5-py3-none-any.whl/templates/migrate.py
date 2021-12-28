template="""
from app import app, migrate
from boa.core.bootstrap import bootstrap


bootstrap(app, None, ["migrations"])


if __name__== '__main__':
    migrate.run()

"""
    