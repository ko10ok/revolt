import pytest
from baby_steps import then, when, given
from district42 import schema, GenericSchema
from pytest import raises

from revolt import substitute
from revolt.errors import SubstitutionError


@pytest.mark.parametrize("substitution_type", [
    schema.any,
    schema.bool,
    schema.bytes,
    schema.const,
    schema.dict,
    schema.float,
    schema.int,
    schema.list,
    schema.none,
    schema.str,
])
def test_schema_any_with_different_schemas_substitution(
    substitution_type: GenericSchema,
):
    with given:
        sch = schema.any

    with when:
        res = substitute(sch, substitution_type)

    with then:
        assert res == substitution_type
        assert sch == schema.any
        assert id(res) != id(substitution_type)
        assert id(res) != id(sch)


def test_schema_any_with_schema_any_with_value_substitution():
    with given:
        sch = schema.any

    with given:
        clarification_type = schema.any(schema.int, schema.float)

    with when:
        res = substitute(sch, clarification_type)

    with then:
        assert res == clarification_type
        assert sch == schema.any
        assert id(res) != id(clarification_type)
        assert id(res) != id(sch)


def test_schema_any_with_value_with_schema_any_with_same_value_substitution():
    with given:
        sch = schema.any(schema.int, schema.float)

    with given:
        clarification_type = schema.any(schema.int, schema.float)

    with when:
        res = substitute(sch, clarification_type)

    with then:
        assert res == clarification_type
        assert id(res) != id(clarification_type)
        assert id(res) != id(sch)


def test_schema_any_with_value_with_different_incomparable_schema_substitution_error():
    with given:
        sch = schema.any(schema.int, schema.str)

    with given:
        clarification_type = schema.float

    with when, raises(Exception) as exception:
        substitute(sch, clarification_type)

    with then:
        assert exception.type is SubstitutionError
        assert sch == schema.any(schema.int, schema.str)


def test_schema_any_with_value_with_schema_any_with_different_incomparable_value_substitution_error():
    with given:
        sch = schema.any(schema.int, schema.str)

    with given:
        clarification_type = schema.any(schema.float, schema.str)

    with when, raises(Exception) as exception:
        substitute(sch, clarification_type)

    with then:
        assert exception.type is SubstitutionError
        assert sch == schema.any(schema.int, schema.str)


def test_schema_any_with_value_with_schema_any_with_different_incomparable_value_on_subtype_substitution_error():
    with given:
        sch = schema.any(schema.dict({'a': schema.int}), schema.str)

    with given:
        clarification_type = schema.any(schema.dict({'a': schema.float}), schema.str)

    with when, raises(Exception) as exception:
        substitute(sch, clarification_type)

    with then:
        assert exception.type is SubstitutionError
        assert sch == schema.any(schema.dict({'a': schema.int}), schema.str)


def test_schema_any_with_value_with_schema_any_with_different_incomparable_value_on_subtype_value_substitution_error():
    with given:
        sch = schema.any(schema.dict({'a': schema.int(1)}), schema.str)

    with given:
        clarification_type = schema.any(schema.dict({'a': schema.int(2)}), schema.str)

    with when, raises(Exception) as exception:
        substitute(sch, clarification_type)

    with then:
        assert exception.type is SubstitutionError
        assert sch == schema.any(schema.dict({'a': schema.int(1)}), schema.str)
