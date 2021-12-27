import json
from glob import glob
from os.path import join
from pathlib import Path
from platform import system
from allure import step


def get_settings(environment):
    ROOT_DIR = Path(__file__).parent.parent.parent.parent.parent.parent
    CONFIG_PATH = join(ROOT_DIR, 'config/config.json')
    with open(CONFIG_PATH) as data:
        config = json.load(data)
        return config[environment]


def formatted_time_for_testrail(seconds):
    hour = seconds // 3600
    seconds = seconds % 3600
    minutes = seconds // 60
    seconds = seconds % 60
    if hour != 0 and minutes != 0 and seconds != 0:
        return f'{hour}h {minutes}m {seconds}s'
    if minutes != 0 and seconds != 0:
        return f'{minutes}m {seconds}s'
    return f'{seconds}s'


def get_count_tests(reporter):
    tests_count = 0
    for status in ['passed', 'failed', 'xfailed', 'skipped']:
        if status in reporter.stats:
            tests_count += len(reporter.stats[status])
    return tests_count


def get_fixtures():
    fixtures = join(Path(__file__).parent.parent.parent, 'fixtures')
    file_path = []
    for file in glob(f'{fixtures}/*'):
        file = file.split('/') if system().lower() in ['linux', 'macos'] else file.split('\\')
        file = file[-1].split('.')[0]
        if file not in ['__init__', '__pycache__']:
            file_path.append(f'fixtures.{file}')
    return file_path


@step('Проверка соответсвия приходящего JSON')
def asserts(expected_data, asserts_data):
    for key, item in enumerate(asserts_data):
        if isinstance(item, dict):
            for value in item.keys():
                if str(value).lower() in dict(expected_data[key]).keys() \
                        and str(value).lower() in dict(asserts_data[key]).keys():
                    assert expected_data[key][str(value).lower()] == asserts_data[key][str(value).lower()], \
                        f'Не найден {str(value).lower()} в списке {item}'
        elif isinstance(asserts_data[item], dict):
            for data in asserts_data[item]:
                assert expected_data[item][data] == asserts_data[item][data]
        else:
            assert expected_data[item] == asserts_data[item]
