from sqlalchemy import create_engine
from plotly.express.data import gapminder

from hydenv.util import env


class HydenvGapMinderExample:
    """
    Gapminder Dataset Loader.\n
    Loads  the Gapminder dataset as published in the plotly.express library.
    The dataset is available athttps://plotly.com/python-api-reference/generated/plotly.express.data.html
    The database has to be installed and initialized before. 
    Do that by hand or use the two CLI commands:
        python -m hydenv database install  --connection=postgresql://postgres:<adminpassword>@localhost:5432/postgres
        python -m hydenv database init --clean --connection=postgresql://hydenv:hydenv@localhost:5432/hydenv
    :param connection: The database URI following syntax:\n
        postgresql://<user>:<password>@<host>:<port>/<database>
    :param overwrite_url: string - overwrite the default data url to load other data. 
        Can be a remote or local path.
    :param quiet: bool - suppresses print output to stdout
    

    """
    def __init__(self, connection="postgresql://{usr}:{pw}@{host}:{port}/{dbname}", quiet=True) -> None:
        # substitute and save
        self.__connection = env.build_connection(connection=connection)
        self.engine = create_engine(self.__connection)

        self.quiet = quiet

    def run(self):
        """
        Loads the gapminder dataset and uploads to the database
        """
        df = gapminder()

        # drop the columns not used
        df.drop(columns=['iso_alpha', 'iso_num'], inplace=True)

        if not self.quiet:
            print('Uploading Gapminder dataset...', end='')
        
        # do the upload
        df.to_sql('gapminder', self.engine, if_exists='replace', index=None)

        if not self.quiet:
            print('done.')
