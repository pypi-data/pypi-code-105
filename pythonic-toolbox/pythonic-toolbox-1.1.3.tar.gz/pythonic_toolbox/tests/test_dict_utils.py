from pythonic_toolbox.utils.dict_utils import dict_until


def test_dict_until():
    data = {'full_name': 'Albert Lee', 'pen_name': None}
    assert dict_until(data, keys=['name', 'full_name']) == 'Albert Lee'
    assert dict_until(data, keys=['full_name', 'name']) == 'Albert Lee'
    assert dict_until(data, keys=['name', 'english_name']) is None
    assert dict_until(data, keys=['name', 'english_name'], default='anonymous') == 'anonymous'
    # test when pen_name is set None on purpose
    assert dict_until(data, keys=['pen_name'], default='anonymous') is None
    # test when value with None value is not acceptable
    assert dict_until(data, keys=['pen_name'], terminate=lambda x: x is not None, default='anonymous') == 'anonymous'
