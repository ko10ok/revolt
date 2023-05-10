import pytest
from baby_steps import then, when, given
from district42 import schema, GenericSchema
from pytest import raises

from revolt import substitute
from revolt.errors import SubstitutionError


def test_schema_bool_with_schema_bool_substitution():
    with given:
        sch = schema.bool

    with when:
        res = substitute(sch, sch)

    with then:
        assert res == sch
        assert id(res) != id(sch)


@pytest.mark.parametrize("value", [True, False])
def test_schema_bool_with_schema_bool_with_value_substitution(value: bool):
    with given:
        sch = schema.bool

    with given:
        clarification_type = schema.bool(value)

    with when:
        res = substitute(sch, clarification_type)

    with then:
        assert sch == schema.bool
        assert res == clarification_type
        assert id(res) != id(clarification_type)
        assert id(res) != id(sch)


@pytest.mark.parametrize("value", [True, False])
def test_schema_bool_with_value_with_schema_bool_with_same_value_substitution(value: bool):
    with given:
        sch = schema.bool(value)

    with given:
        clarification_type = schema.bool(value)

    with when:
        res = substitute(sch, clarification_type)

    with then:
        assert res == clarification_type
        assert id(res) != id(clarification_type)
        assert id(res) != id(sch)


@pytest.mark.parametrize("value", [True, False])
def test_schema_bool_with_value_with_schema_bool_with_different_value_substitution_error(
    value: bool
):
    with given:
        sch = schema.bool(value)

    with given:
        clarification_type = schema.bool(not value)

    with when, raises(Exception) as exception:
        substitute(sch, clarification_type)

    with then:
        assert exception.type is SubstitutionError
        assert sch == schema.bool(value)


@pytest.mark.parametrize("clarification_type", [
    schema.any,
    schema.bytes,
    schema.const,
    schema.dict,
    schema.float,
    schema.int,
    schema.list,
    schema.none,
    schema.str,
])
def test_schema_bool_with_different_schema_substitution_error(
    clarification_type: GenericSchema
):
    with given:
        sch = schema.bool

    with when, raises(Exception) as exception:
        substitute(sch, clarification_type)

    with then:
        assert exception.type is SubstitutionError
        assert sch == schema.bool
