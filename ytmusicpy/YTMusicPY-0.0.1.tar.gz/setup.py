from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = r'YTMusicPY is an API wrapper for the YTMDesktop remote (https://github.com/ytmdesktop/ytmdesktop/)'
LONG_DESCRIPTION = r'YTMusicPY is an API wrapper for the YTMDesktop remote ( https://github.com/ytmdesktop/ytmdesktop/ ).' \
                   r'You can find the Docs at https://github.com/quintindunn/YTMusicPY/wiki'
# Setting up
setup(
    name="YTMusicPY",
    version=VERSION,
    author="T1ps",
    author_email="quintindunn67@gmail.com",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    install_requires=['requests'],
    keywords=['python', 'youtube', 'music', 'player', 'YTMAPI', 'api']
)