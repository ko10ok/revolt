from baby_steps import then, when, given
from district42 import schema
from pytest import raises

from revolt import substitute
from revolt.errors import SubstitutionError


def test_schema_int_min_value_with_schema_int_with_bigger_min_value_substitution():
    with given:
        value = 42
        another_value = 51

    with given:
        sch = schema.int.min(value)

    with given:
        clarification_type = schema.int.min(another_value)

    with when:
        res = substitute(sch, clarification_type)

    with then:
        assert res == clarification_type
        assert repr(res) == repr(clarification_type)
        assert id(res) != id(clarification_type)
        assert id(res) != id(sch)


def test_schema_int_min_value_with_schema_int_with_smaller_min_value_substitution_error():
    with given:
        value = 42
        another_value = 31

    with given:
        sch = schema.int.min(value)

    with given:
        clarification_type = schema.int.min(another_value)

    with when, raises(Exception) as exception:
        substitute(sch, clarification_type)

    with then:
        assert exception.type is SubstitutionError
        assert sch == schema.int.min(value)


def test_schema_int_min_value_with_schema_int_with_bigger_exact_value_substitution():
    with given:
        value = 42
        another_value = 51

    with given:
        sch = schema.int.min(value)

    with given:
        clarification_type = schema.int(another_value)

    with when:
        res = substitute(sch, clarification_type)

    with then:
        assert res == clarification_type
        assert repr(res) == repr(clarification_type)
        assert id(res) != id(clarification_type)
        assert id(res) != id(sch)


def test_schema_int_min_value_with_schema_int_with_smaller_exact_value_substitution_error():
    with given:
        value = 42
        another_value = 31

    with given:
        sch = schema.int.min(value)

    with given:
        clarification_type = schema.int(another_value)

    with when, raises(Exception) as exception:
        substitute(sch, clarification_type)

    with then:
        assert exception.type is SubstitutionError
        assert sch == schema.int.min(value)


def test_schema_int_max_value_with_schema_int_with_smaller_max_value_substitution():
    with given:
        value = 42
        another_value = 31

    with given:
        sch = schema.int.max(value)

    with given:
        clarification_type = schema.int.max(another_value)

    with when:
        res = substitute(sch, clarification_type)

    with then:
        assert res == clarification_type
        assert repr(res) == repr(clarification_type)
        assert id(res) != id(clarification_type)
        assert id(res) != id(sch)


def test_schema_int_max_value_with_schema_int_with_bigger_max_value_substitution_error():
    with given:
        value = 42
        another_value = 51

    with given:
        sch = schema.int.max(value)

    with given:
        clarification_type = schema.int.max(another_value)

    with when, raises(Exception) as exception:
        substitute(sch, clarification_type)

    with then:
        assert exception.type is SubstitutionError
        assert sch == schema.int.max(value)


def test_schema_int_max_value_with_schema_int_with_smaller_exact_value_substitution():
    with given:
        value = 42
        another_value = 31

    with given:
        sch = schema.int.max(value)

    with given:
        clarification_type = schema.int(another_value)

    with when:
        res = substitute(sch, clarification_type)

    with then:
        assert res == clarification_type
        assert repr(res) == repr(clarification_type)
        assert id(res) != id(clarification_type)
        assert id(res) != id(sch)


def test_schema_int_max_value_with_schema_int_with_bigger_exact_value_substitution_error():
    with given:
        value = 42
        another_value = 51

    with given:
        sch = schema.int.max(value)

    with given:
        clarification_type = schema.int(another_value)

    with when, raises(Exception) as exception:
        substitute(sch, clarification_type)

    with then:
        assert exception.type is SubstitutionError
        assert sch == schema.int.max(value)
