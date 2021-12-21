from tracardi_key_counter.service.key_counter import KeyCounter


def test_key_counter():
    c = KeyCounter({"d": 1})
    c.count('a')
    c.count('b')
    c.count(['a', 'c'])
    c.count({"a": 10, "b": 1, "f": 1, "g": "asas"})
    c.count([{"a": 10, "b": 1, "f": 1, "g": "asas"}])

    result = c.counts

    assert result == {'d': 1, 'a': 12, 'b': 2, 'c': 1, 'f': 1}

c = KeyCounter({"d": 1})
c.count('a')
c.count('b')
c.count(['a', 'c'])
c.count({"a": 10, "b": 1, "f": 1, "g": "asas"})
c.count([{"a": 10, "b": 1, "f": 1, "g": "asas"}])

print(c.counts)