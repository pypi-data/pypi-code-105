# from app import core
import importlib
import logging

logger = logging.getLogger("Boot core")


def bootstrap(app, core=None, types=["config", "api"]):    
    # Register core of apps
    for type_ in types:
        for package in app.config.get("INSTALLED_APPS", []):
            if type_ in ["config"]:
                assert not core is None 
                for file in ["config"]:
                    package_core = "%s.%s" % (package, file)
                    try:
                        logger.debug("import %s" % package_core)
                        module = importlib.import_module(package_core)
                        register_frontend_views = getattr(module, "register_frontend_views", lambda a: 0)
                        register_api_views = getattr(module, "register_api_views", lambda a: 0)
                        register_frontend_views(core)
                        register_api_views(core)
                        logger.debug("imported %s" % package_core)
                    except ModuleNotFoundError as exc:
                        if not package_core in str(exc):
                            raise exc
                
                # core.bootstrap_frontends()

            elif type_ in ["api", "routes", "rpc"]:
                for file in ["api", "routes", "rpc"]:
                    package_core = "%s.%s" % (package, file)
                    try:
                        logger.debug("api.import %s" % package_core)
                        __import__(package_core)
                        logger.debug("api.imported %s" % package_core)
                    except ModuleNotFoundError as exc:
                        if not package_core in str(exc):
                            raise exc            
            else:
                for file in [type_]:
                    package_core = "%s.%s" % (package, file)
                    try:
                        __import__(package_core)
                        logger.debug("import %s" % package_core)
                    except ModuleNotFoundError as exc:
                        if not package_core in str(exc):
                            raise exc
