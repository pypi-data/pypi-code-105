template = """

from app import create_app
from boa.core.bootstrap import bootstrap

config_file = os.getenv('APP_CONFIG_FILE', "app.config.py")


bootstrap(app, core, ["config", "api"])
core = create_app(app)


from app import create_app, core
from boa.core.bootstrap import bootstrap


config_file = os.getenv('APP_CONFIG_FILE', "app.config.py")
app = create_app()
bootstrap(app, core, ["config", "view", "routes"])

if __name__ == '__main__':    
    app.run(host=app.config["HOST"], port=app.config["PORT"])

"""
