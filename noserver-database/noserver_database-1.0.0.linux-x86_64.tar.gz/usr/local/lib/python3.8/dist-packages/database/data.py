import os
import json
from database.alert import DatabaseAlert, DatabaseError
from database.table import Table


class Database:

    def __init__(self, name, folder='auto', debug=False, do_not_create=False):
        self.name = name
        self.debug = debug
        self.folder = folder
        if not do_not_create:
            if os.path.isdir(folder):
                DatabaseAlert(f'the noserver_database \'{self.name}\' is already created', self)
            elif folder == 'auto':
                if not os.path.isdir(self.name + '-noserver_database'):
                    os.mkdir(self.name + '-noserver_database')
                else:
                    DatabaseAlert(f'the noserver_database \'{self.name}\' is already created', self)
            else:
                os.mkdir(folder)
        self.folder = self.name + '-noserver_database' if folder == 'auto' else folder

    def create_table(self, name):
        if not os.path.isfile(self.folder + '/' + name + '.json'):
            with open(self.folder + '/' + name + '.json', 'w+') as f:
                dict_ = {'data': []}
                f.write(json.dumps(dict_))
                f.close()
        else:
            DatabaseAlert(f'the table \'{name}\' is already created', self)

    def get_table(self, name):
        return self > name

    def __gt__(self, name):
        return Table(name, self)
