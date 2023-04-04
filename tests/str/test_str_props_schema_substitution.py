from baby_steps import then, when, given
from district42 import schema
from pytest import raises

from revolt import substitute
from revolt.errors import SubstitutionError

# len
# max_len
# min_len
# min_max_len
# alpha
# substr
# regexp

"""
DictSchema ranging via one steps clarifying mutations tree
    
    schema.str > schema.str.len(1, ) > schema.str.len(1, 10)
    schema.str > schema.str.len(..., 10) > schema.str.len(1, 10)
    
    schema.str.len(..., 10) > schema.str.len(..., 10).contains('abc')
    
    ! schema.str.len(..., 10).contains('a'*20)
    ! schema.str.len(10).contains('a'*20)
    
    schema.str > schema.str.contains('abc') > schema.str.contains('abc').len(1,...)
    
    schema.str.contains('abc') > schema.str('abc')
    schema.str.contains('abc') > schema.str('erc abc def')
 
"""


def test_schema_str_len_with_schema_str_with_same_len_value_substitution():
    with given:
        len_value = 41

    with given:
        sch = schema.str.len(len_value)

    with given:
        clarification_type = schema.str.len(len_value)

    with when:
        res = substitute(sch, clarification_type)

    with then:
        assert res == clarification_type
        assert repr(res) == repr(clarification_type)
        assert id(res) != id(clarification_type)
        assert id(res) != id(sch)

def test_schema_str_len_with_schema_str_with_different_len_value_substitution_error():
    with given:
        len_value = 41
        another_len_value = 42

    with given:
        sch = schema.str.len(len_value)

    with given:
        clarification_type = schema.str.len(another_len_value)

    with when, raises(Exception) as exception:
        substitute(sch, clarification_type)

    with then:
        assert exception.type is SubstitutionError
        assert sch == schema.str.len(len_value)

# min max

def test_schema_str_len_with_schema_str_with_same_len_value_substitution():
    with given:
        len_value = 41

    with given:
        sch = schema.str.len(len_value)

    with given:
        clarification_type = schema.str.len(len_value)

    with when:
        res = substitute(sch, clarification_type)

    with then:
        assert res == clarification_type
        assert repr(res) == repr(clarification_type)
        assert id(res) != id(clarification_type)
        assert id(res) != id(sch)


def test_schema_str_with_schema_str_with_len_value_substitution():
    with given:
        value = 'banana'
        len_value = len(value)

    with given:
        sch = schema.str(value)

    with given:
        clarification_type = schema.str(value).len(len_value)

    with when:
        res = substitute(sch, clarification_type)

    with then:
        assert res == schema.str(value)
        assert repr(res) == repr(schema.str(value))
        assert id(res) != id(clarification_type)
        assert id(res) != id(sch)


def test_schema_str_with_schema_str_with_smaller_min_len_value_substitution():
    with given:
        value = 'banana'
        len_value = len(value)

    with given:
        sch = schema.str(value)

    with given:
        clarification_type = schema.str(value).len(len_value, ...)

    with when:
        res = substitute(sch, clarification_type)

    with then:
        assert res == clarification_type
        assert repr(res) == repr(clarification_type)
        assert id(res) != id(clarification_type)
        assert id(res) != id(sch)


def test_schema_str_with_schema_str_with_bigger_max_len_value_substitution():
    with given:
        value = 'banana'
        len_value = len(value)

    with given:
        sch = schema.str(value)

    with given:
        clarification_type = schema.str(value).len(..., len_value)

    with when:
        res = substitute(sch, clarification_type)

    with then:
        assert res == clarification_type
        assert repr(res) == repr(clarification_type)
        assert id(res) != id(clarification_type)
        assert id(res) != id(sch)


def test_schema_str_contains_with_schema_str_contains_with_same_value_substitution():
    with given:
        value = 'banana'

    with given:
        sch = schema.str.contains(value)

    with given:
        clarification_type = schema.str.contains(value)

    with when:
        res = substitute(sch, clarification_type)

    with then:
        assert res == clarification_type
        assert repr(res) == repr(clarification_type)
        assert id(res) != id(clarification_type)
        assert id(res) != id(sch)


def test_schema_str_contains_with_schema_str_contains_with_different_value_substitution_error():
    with given:
        value = 'banana'
        another_value = 'apple'

    with given:
        sch = schema.str.contains(value)

    with given:
        clarification_type = schema.str.contains(another_value)

    with when, raises(Exception) as exception:
        substitute(sch, clarification_type)

    with then:
        assert exception.type is SubstitutionError
        assert sch == schema.str.contains(value)


def test_schema_str_contains_with_schema_str_contains_with_sub_value_substitution():
    with given:
        value = 'ap-banana-ple'
        another_value = 'banana'

    with given:
        sch = schema.str.contains(value)

    with given:
        clarification_type = schema.str.contains(another_value)

    with when:
        res = substitute(sch, clarification_type)

    with then:
        assert res == clarification_type
        assert repr(res) == repr(clarification_type)
        assert id(res) != id(clarification_type)
        assert id(res) != id(sch)


def test_schema_str_contains_with_schema_str_with_same_value_substitution():
    with given:
        value = 'banana'

    with given:
        sch = schema.str.contains(value)

    with given:
        clarification_type = schema.str(value)

    with when:
        res = substitute(sch, clarification_type)

    with then:
        assert res == clarification_type
        assert repr(res) == repr(clarification_type)
        assert id(res) != id(clarification_type)
        assert id(res) != id(sch)


def test_schema_str_contains_with_schema_str_with_superstring_value_substitution():
    with given:
        value = 'banana'
        another_value = f'ap-{value}-ple'

    with given:
        sch = schema.str.contains(value)

    with given:
        clarification_type = schema.str(another_value)

    with when:
        res = substitute(sch, clarification_type)

    with then:
        assert res == clarification_type
        assert repr(res) == repr(clarification_type)
        assert id(res) != id(clarification_type)
        assert id(res) != id(sch)


def test_schema_str_contains_with_schema_str_with_different_value_substitution_error():
    with given:
        value = 'banana'
        another_value = 'apple'

    with given:
        sch = schema.str.contains(value)

    with given:
        clarification_type = schema.str(another_value)

    with when, raises(Exception) as exception:
        substitute(sch, clarification_type)

    with then:
        assert exception.type is SubstitutionError
        assert sch == schema.str.contains(value)


def test_schema_str_len_with_schema_str_with_possible_contains_value_substitution():
    with given:
        len_value = 10
        another_value = 'a' * len_value

    with given:
        sch = schema.str.len(len_value)

    with given:
        clarification_type = schema.str.len(len_value).contains(another_value)

    with when:
        res = substitute(sch, clarification_type)

    with then:
        assert res == schema.str.len(len_value).contains(another_value)
        assert repr(res) == repr(schema.str.len(len_value).contains(another_value))
        assert id(res) != id(clarification_type)
        assert id(res) != id(sch)


def test_schema_str_len_with_schema_str_with_bigger_contains_value_substitution_error():
    with given:
        len_value = 10
        another_value = 'a' * (len_value + 1)

    with given:
        sch = schema.str.len(len_value)

    with given:
        clarification_type = schema.str.len(len_value).contains(another_value)

    with when, raises(Exception) as exception:
        substitute(sch, clarification_type)

    with then:
        assert exception.type is SubstitutionError
        assert sch == schema.str.len(len_value)


def test_schema_str_len_with_schema_str_with_stronger_len_substitution():
    with given:
        len_value = 10

    with given:
        sch = schema.str.len(len_value, ...)

    with given:
        clarification_type = schema.str.len(len_value)

    with when:
        res = substitute(sch, clarification_type)

    with then:
        assert res == clarification_type
        assert repr(res) == repr(schema.str.len(len_value))
        assert id(res) != id(clarification_type)
        assert id(res) != id(sch)
