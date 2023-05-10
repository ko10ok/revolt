import pytest
from baby_steps import then, when, given
from district42 import schema, GenericSchema
from pytest import raises

from revolt import substitute
from revolt.errors import SubstitutionError


def test_schema_str_with_schema_str_substitution():
    with given:
        sch = schema.str

    with when:
        res = substitute(sch, sch)

    with then:
        assert res == sch
        assert id(res) != id(sch)


def test_schema_str_with_schema_str_with_value_substitution():
    with given:
        sch = schema.str

    with given:
        clarification_type = schema.str("banana")

    with when:
        res = substitute(sch, clarification_type)

    with then:
        assert sch == schema.str
        assert res == clarification_type
        assert id(res) != id(clarification_type)
        assert id(res) != id(sch)


def test_schema_str_with_value_with_schema_str_with_same_value_substitution():
    with given:
        value = "banana"

    with given:
        sch = schema.str(value)

    with given:
        clarification_type = schema.str(value)

    with when:
        res = substitute(sch, clarification_type)

    with then:
        assert res == clarification_type
        assert id(res) != id(clarification_type)
        assert id(res) != id(sch)


def test_schema_str_with_value_with_schema_str_with_different_value_substitution_error():
    with given:
        value = "banana"
        another_value = "cucumber"

    with given:
        sch = schema.str(value)

    with given:
        clarification_type = schema.str(another_value)

    with when, raises(Exception) as exception:
        substitute(sch, clarification_type)

    with then:
        assert exception.type is SubstitutionError
        assert sch == schema.str(value)


@pytest.mark.parametrize("clarification_type", [
    schema.any,
    schema.bool,
    schema.bytes,
    schema.const,
    schema.dict,
    schema.float,
    schema.int,
    schema.none,
    schema.str,
])
def test_schema_str_with_different_schema_substitution_error(
    clarification_type: GenericSchema
):
    with given:
        sch = schema.str

    with when, raises(Exception) as exception:
        substitute(sch, clarification_type)

    with then:
        assert exception.type is SubstitutionError
        assert sch == schema.str
