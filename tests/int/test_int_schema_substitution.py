import pytest
from baby_steps import then, when, given
from district42 import schema, GenericSchema
from pytest import raises

from revolt import substitute
from revolt.errors import SubstitutionError


def test_schema_int_with_schema_int_substitution():
    with given:
        sch = schema.int

    with when:
        res = substitute(sch, sch)

    with then:
        assert res == sch
        assert repr(res) == repr(sch)
        assert id(res) != id(sch)


def test_schema_int_with_schema_int_with_value_substitution():
    with given:
        sch = schema.int

    with given:
        clarification_type = schema.int(42)

    with when:
        res = substitute(sch, clarification_type)

    with then:
        assert sch == schema.int
        assert res == clarification_type
        assert repr(res) == repr(clarification_type)
        assert id(res) != id(clarification_type)
        assert id(res) != id(sch)


def test_schema_int_with_value_with_schema_int_with_same_value_substitution():
    with given:
        value = 42

    with given:
        sch = schema.int(value)

    with given:
        clarification_type = schema.int(value)

    with when:
        res = substitute(sch, clarification_type)

    with then:
        assert res == clarification_type
        assert repr(res) == repr(clarification_type)
        assert id(res) != id(clarification_type)
        assert id(res) != id(sch)


def test_schema_int_with_value_with_schema_int_with_different_value_substitution_error():
    with given:
        value = 42
        another_value = 51

    with given:
        sch = schema.int(value)

    with given:
        clarification_type = schema.int(another_value)

    with when, raises(Exception) as exception:
        substitute(sch, clarification_type)

    with then:
        assert exception.type is SubstitutionError
        assert sch == schema.int(value)


@pytest.mark.parametrize("clarification_type", [
    schema.any,
    schema.bool,
    schema.bytes,
    schema.const,
    schema.dict,
    schema.float,
    schema.list,
    schema.none,
    schema.str,
])
def test_schema_int_with_different_schema_substitution_error(
    clarification_type: GenericSchema
):
    with given:
        sch = schema.int

    with when, raises(Exception) as exception:
        substitute(sch, clarification_type)

    with then:
        assert exception.type is SubstitutionError
        assert sch == schema.int
