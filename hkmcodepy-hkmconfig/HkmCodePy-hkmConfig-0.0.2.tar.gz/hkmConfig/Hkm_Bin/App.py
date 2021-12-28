from BaseConfig import BaseConfig

class App(BaseConfig):
    def RUN(self):
        self.config_file = 'App'
        self.baseURL = "http://localhost"
        self.port = "8080"
        self.defaultLocale = 'en'
        self.supportedLocales = ['en']
        self.appTimezone = 'UTC'
        self.charset = 'UTF-8'
        self.sessionCookieName = 'hkm_session'
        self.sessionExpiration = 7200
        self.sessionTimeToUpdate = 300
        self.cookiePrefix = ''
        
        