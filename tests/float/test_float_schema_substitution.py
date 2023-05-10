import pytest
from baby_steps import then, when, given
from district42 import schema, GenericSchema
from pytest import raises

from revolt import substitute
from revolt.errors import SubstitutionError


def test_schema_float_with_schema_float_substitution():
    with given:
        sch = schema.float

    with when:
        res = substitute(sch, sch)

    with then:
        assert res == sch
        assert id(res) != id(sch)


def test_schema_float_with_schema_float_with_value_substitution():
    with given:
        sch = schema.float

    with given:
        clarification_type = schema.float(42.0)

    with when:
        res = substitute(sch, clarification_type)

    with then:
        assert sch == schema.float
        assert res == clarification_type
        assert id(res) != id(clarification_type)
        assert id(res) != id(sch)


def test_schema_float_with_value_with_schema_float_with_same_value_substitution():
    with given:
        value = 42.0

    with given:
        sch = schema.float(value)

    with given:
        clarification_type = schema.float(value)

    with when:
        res = substitute(sch, clarification_type)

    with then:
        assert res == clarification_type
        assert id(res) != id(clarification_type)
        assert id(res) != id(sch)


def test_schema_float_with_value_with_schema_float_with_different_value_substitution_error():
    with given:
        value = 42.0
        another_value = 51.0

    with given:
        sch = schema.float(value)

    with given:
        clarification_type = schema.float(another_value)

    with when, raises(Exception) as exception:
        substitute(sch, clarification_type)

    with then:
        assert exception.type is SubstitutionError
        assert sch == schema.float(value)


@pytest.mark.parametrize("clarification_type", [
    schema.any,
    schema.bool,
    schema.bytes,
    schema.const,
    schema.dict,
    schema.int,
    schema.list,
    schema.none,
    schema.str,
])
def test_schema_float_with_different_schema_substitution_error(
    clarification_type: GenericSchema
):
    with given:
        sch = schema.float

    with when, raises(Exception) as exception:
        substitute(sch, clarification_type)

    with then:
        assert exception.type is SubstitutionError
        assert sch == schema.float
