from setuptools import setup
setup(
    name = 'tempestas',
    packages = ['tempestas'],
    version = '2.0.1',
    license = 'MIT',
    description = 'Forecast data for the next 24 hours',
    keywords = ['weather', 'forecast', 'temperature'],
    install_requires = [
            'requests'
        ]
)    
