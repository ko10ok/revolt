import pytest
from baby_steps import then, when, given
from district42 import schema, GenericSchema
from pytest import raises

from revolt import substitute
from revolt.errors import SubstitutionError


def test_schema_bytes_with_schema_bytes_substitution():
    with given:
        sch = schema.bytes

    with when:
        res = substitute(sch, sch)

    with then:
        assert res == sch
        assert id(res) != id(sch)


def test_schema_bytes_with_schema_bytes_with_value_substitution():
    with given:
        sch = schema.bytes

    with given:
        clarification_type = schema.bytes(b"banana")

    with when:
        res = substitute(sch, clarification_type)

    with then:
        assert sch == schema.bytes
        assert res == clarification_type
        assert id(res) != id(clarification_type)
        assert id(res) != id(sch)


def test_schema_bytes_with_value_with_schema_bytes_with_same_value_substitution():
    with given:
        value = b"banana"

    with given:
        sch = schema.bytes(value)

    with given:
        clarification_type = schema.bytes(value)

    with when:
        res = substitute(sch, clarification_type)

    with then:
        assert res == clarification_type
        assert id(res) != id(clarification_type)
        assert id(res) != id(sch)


def test_schema_bytes_with_value_with_schema_bytes_with_different_value_substitution_error():
    with given:
        value = b"banana"
        another_value = b"cucumber"

    with given:
        sch = schema.bytes(value)

    with given:
        clarification_type = schema.bytes(another_value)

    with when, raises(Exception) as exception:
        substitute(sch, clarification_type)

    with then:
        assert exception.type is SubstitutionError
        assert sch == schema.bytes(value)


@pytest.mark.parametrize("clarification_type", [
    schema.any,
    schema.bool,
    schema.const,
    schema.dict,
    schema.float,
    schema.int,
    schema.list,
    schema.none,
    schema.str,
])
def test_schema_bytes_with_different_schema_substitution_error(
    clarification_type: GenericSchema
):
    with given:
        sch = schema.bytes

    with when, raises(Exception) as exception:
        substitute(sch, clarification_type)

    with then:
        assert exception.type is SubstitutionError
        assert sch == schema.bytes
