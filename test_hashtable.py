import pytest
from pytest_unordered import unordered
from unittest.mock import patch

from hashtable import HashTable, Pair
from collections import deque


@pytest.fixture
def hash_table():
    sample_data = HashTable(capacity=100)
    sample_data["hola"] = "hello"
    sample_data[98.6] = 37
    sample_data[False] = True
    return sample_data


def test_should_create_hashtable():
    assert HashTable(capacity=100) is not None


def test_should_report_length_of_empty_hash_table():
    assert len(HashTable(capacity=100)) == 0


def test_should_report_length(hash_table):
    assert len(hash_table) == 3


def test_should_return_pairs(hash_table):
    assert hash_table.pairs == [
        ("hola", "hello"),
        (98.6, 37),
        (False, True)
    ]


def test_should_get_pairs_of_empty_hash_table():
    assert HashTable(capacity=100).pairs == []


def test_should_return_copy_of_pairs(hash_table):
    assert hash_table.pairs is not hash_table.pairs


def test_should_not_include_blank_pairs(hash_table):
    assert None not in hash_table.pairs


def test_should_create_empty_pair_buckets():
    assert HashTable(capacity=3)._buckets == [deque(), deque(), deque()]


def test_should_insert_key_value_pairs(hash_table):
    assert ("hola", "hello") in hash_table.pairs
    assert (98.6, 37) in hash_table.pairs
    assert (False, True) in hash_table.pairs


def test_should_update_value(hash_table):
    assert hash_table["hola"] == "hello"
    hash_table["hola"] = "hallo"
    assert hash_table["hola"] == "hallo"
    assert hash_table[98.6] == 37
    assert hash_table[False] is True
    assert len(hash_table) == 3


def test_should_not_shrink_when_removing_elements(hash_table):
    assert ("hola", "hello") in hash_table.pairs
    del hash_table["hola"]
    assert ("hola", "hello") not in hash_table.pairs
    assert len(hash_table) == 2


def test_should_not_create_hashtable_with_zero_capacity():
    with pytest.raises(ValueError):
        HashTable(capacity=0)


def test_should_only_allow_integer_capacity():
    with pytest.raises(ValueError):
        HashTable(capacity="100")


def test_should_have_default_capacity():
    hash_table = HashTable()
    assert hash_table.capacity == 8


def test_should_not_create_hashtable_with_negative_capacity():
    with pytest.raises(ValueError):
        HashTable(capacity=-100)


def test_should_not_contain_none_value_when_created():
    assert None not in HashTable(capacity=100).values


def test_should_insert_none_value():
    hash_table = HashTable(capacity=100)
    hash_table["key"] = None
    assert ("key", None) in hash_table.pairs


def test_should_find_value_by_key(hash_table):
    assert hash_table["hola"] == "hello"
    assert hash_table[98.6] == 37
    assert hash_table[False] is True


def test_should_raise_error_on_missing_key():
    hash_table = HashTable(capacity=100)
    with pytest.raises(KeyError) as exception_info:
        hash_table["missing_key"]
    assert exception_info.value.args[0] == "missing_key"


def test_should_raise_key_error_when_deleting(hash_table):
    with pytest.raises(KeyError) as exception_info:
        del hash_table["missing_key"]
    assert exception_info.value.args[0] == "missing_key"


def test_should_find_key(hash_table):
    assert "hola" in hash_table


def test_should_not_find_key(hash_table):
    assert "missing_key" not in hash_table


def test_should_return_duplicate_values():
    hash_table = HashTable(capacity=100)
    hash_table["Alice"] = 24
    hash_table["Bob"] = 42
    hash_table["Joe"] = 42
    assert [24, 42, 42] == sorted(hash_table.values)


def test_should_get_value(hash_table):
    assert hash_table.get("hola") == "hello"


def test_should_get_values(hash_table):
    assert unordered(hash_table.values) == ["hello", 37, True]


def test_should_get_values_of_empty_hash_table():
    assert HashTable(capacity=100).values == []


def test_should_return_copy_of_values(hash_table):
    assert hash_table.values is not hash_table.values


def test_should_get_none_when_missing_key(hash_table):
    assert hash_table.get("missing_key") is None


def test_should_get_default_value_when_missing_key(hash_table):
    assert hash_table.get("missing_key", "default") == "default"


def test_should_get_value_with_default(hash_table):
    assert hash_table.get("hola", "default") == "hello"


def test_should_get_keys(hash_table):
    assert hash_table.keys == ["hola", 98.6, False]


def test_should_get_keys_of_empty_hash_table():
    assert HashTable(capacity=100).keys == []


def test_should_return_copy_of_keys(hash_table):
    assert hash_table.keys is not hash_table.keys


def test_should_convert_to_dict(hash_table):
    dictionary = dict(hash_table.pairs)
    assert list(dictionary.keys()) == hash_table.keys
    assert list(dictionary.items()) == hash_table.pairs
    assert list(dictionary.values()) == unordered(hash_table.values)


def test_should_iterate_over_keys(hash_table):
    for key in hash_table.keys:
        assert key in ("hola", 98.6, False)


def test_should_iterate_over_values(hash_table):
    for value in hash_table.values:
        assert value in ("hello", 37, True)


def test_should_iterate_over_pairs(hash_table):
    for key, value in hash_table.pairs:
        assert key in hash_table.keys
        assert value in hash_table.values


def test_should_iterate_over_instance(hash_table):
    for key in hash_table:
        assert key in ("hola", 98.6, False)


def test_should_use_dict_literal_for_str(hash_table):
    assert str(hash_table) in {
        "{'hola': 'hello', 98.6: 37, False: True}",
        "{'hola': 'hello', False: True, 98.6: 37}",
        "{98.6: 37, 'hola': 'hello', False: True}",
        "{98.6: 37, False: True, 'hola': 'hello'}",
        "{False: True, 'hola': 'hello', 98.6: 37}",
        "{False: True, 98.6: 37, 'hola': 'hello'}",
    }


def test_should_create_hashtable_from_dict():
    dictionary = {"hola": "hello", 98.6: 37, False: True}

    hash_table = HashTable.from_dict(dictionary)

    assert hash_table.capacity == 6  # with load_factor 0.6
    assert hash_table.keys == list(dictionary.keys())
    assert hash_table.pairs == list(dictionary.items())
    assert unordered(hash_table.values) == list(dictionary.values())


def test_should_create_hashtable_from_dict_with_custom_capacity():
    dictionary = {"hola": "hello", 98.6: 37, False: True}

    hash_table = HashTable.from_dict(dictionary, capacity=100)

    assert hash_table.capacity == 100
    assert hash_table.keys == list(dictionary.keys())
    assert hash_table.pairs == list(dictionary.items())
    assert unordered(hash_table.values) == list(dictionary.values())


def test_should_have_canonical_string_representation(hash_table):
    assert repr(hash_table) in {
        "HashTable.from_dict({'hola': 'hello', 98.6: 37, False: True})",
        "HashTable.from_dict({'hola': 'hello', False: True, 98.6: 37})",
        "HashTable.from_dict({98.6: 37, 'hola': 'hello', False: True})",
        "HashTable.from_dict({98.6: 37, False: True, 'hola': 'hello'})",
        "HashTable.from_dict({False: True, 'hola': 'hello', 98.6: 37})",
        "HashTable.from_dict({False: True, 98.6: 37, 'hola': 'hello'})",
    }


def test_should_compare_equal_to_itself(hash_table):
    assert hash_table == hash_table


def test_should_compare_equal_to_copy(hash_table):
    assert hash_table is not hash_table.copy()
    assert hash_table == hash_table.copy()


def test_should_compare_equal_different_key_value_order():
    h1 = HashTable.from_dict({"a": 1, "b": 2, "c": 3})
    h2 = HashTable.from_dict({"b": 2, "a": 1, "c": 3})
    assert h1 == h2


def test_should_compare_unequal(hash_table):
    other = HashTable.from_dict({"different": "value"})
    assert hash_table != other


def test_should_compare_unequal_another_data_type(hash_table):
    assert hash_table != 42


def test_should_copy_keys_values_pairs_capacity(hash_table):
    copy = hash_table.copy()
    assert copy is not hash_table
    assert set(hash_table.keys) == set(copy.keys)
    assert unordered(hash_table.values) == copy.values
    assert set(hash_table.pairs) == set(copy.pairs)
    assert hash_table.capacity == copy.capacity


def test_should_compare_equal_different_capacity():
    data = {"a": 1, "b": 2, "c": 3}
    h1 = HashTable.from_dict(data, capacity=50)
    h2 = HashTable.from_dict(data, capacity=100)
    assert h1 == h2


def test_collided_keys_should_share_bucket():
    with patch("builtins.hash", return_value=5):
        hash_table = HashTable(capacity=10)
        assert hash_table.capacity == 10
        hash_table["test1"] = "123"
        hash_table["test2"] = "246"
        assert hash_table._buckets[5] == \
               deque([
                   Pair(key='test1', value='123'),
                   Pair(key='test2', value='246')
               ])
        assert len(hash_table) == 2
        assert hash_table.capacity == 10


def test_should_delete_pair():
    hash_table = HashTable(capacity=10)
    hash_table["test1"] = "123"
    assert len(hash_table) == 1
    del hash_table["test1"]
    assert len(hash_table) == 0


def test_should_increase_capacity():
    hash_table = HashTable(capacity=1)

    hash_table[1] = "one"
    assert hash_table.capacity == 1

    hash_table[2] = "two"
    assert hash_table.capacity == 2

    assert hash_table.pairs == [
        (1, "one"),
        (2, "two"),
    ]


def test_should_return_correct_load_factor(hash_table):
    assert hash_table.load_factor == 0.03
    hash_table[4] = "test"
    assert hash_table.load_factor == 0.04


def test_should_increase_capacity_at_load_factor_threshold():
    hash_table = HashTable(capacity=10)
    assert hash_table._load_factor_threshold == 0.6
    assert hash_table.capacity == 10

    for i in range(1, 7):  # add 6 pairs
        hash_table[i] = i
    assert hash_table.capacity == 10
    assert len(hash_table) == 6

    hash_table["test"] = "test"  # 7th pair triggers resize
    assert hash_table.capacity == 20
    assert len(hash_table) == 7
