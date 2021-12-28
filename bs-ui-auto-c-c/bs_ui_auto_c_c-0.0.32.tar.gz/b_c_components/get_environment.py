import os

from b_c_components.get_config.get_config import Setting


def get_environment_data(environment=None):
    """

    :return:
    """
    if environment is None:
        environment = os.environ.get('environment')
        if environment is None:
            environment = Setting(os.environ.get('config_path')).get_setting('environment_data', 'environment')

    url_dict = {

        'test': {
            'italent_url': 'https://www.italent.link',
            'cloud_url': 'https://cloud.italent.link',
            'tms_url': 'https://tms.beisen.net',
            'account': 'https://account.italent.link'

        },
        'prod': {
            'italent_url': 'https://www.italent.cn',
            'cloud_url': 'https://cloud.italent.cn',
            'tms_url': 'https://tms.beisen.com',
            'account': 'https://account.italent.cn'
        }

    }

    return url_dict.get(environment)


def get_host(environment=None):
    """
    return
    """
    if environment is None:
        environment = os.environ.get('environment')
        if environment is None:
            environment = Setting(os.environ.get('config_path')).get_setting('environment_data', 'environment')

    host_dict = {
        'test': {
            'italent': 'www.italent.link',
            'cloud': 'cloud.italent.link',
            'tms': 'tms.beisen.net',
            'account': 'account.italent.link'

        },
        'prod': {
            'italent': 'www.italent.cn',
            'cloud': 'cloud.italent.cn',
            'tms': 'tms.beisen.com',
            'account': 'account.italent.cn'
        }
    }

    return host_dict.get(environment)

