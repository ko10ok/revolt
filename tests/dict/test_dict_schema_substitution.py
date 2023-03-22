import pytest
from baby_steps import then, when, given
from district42 import schema, GenericSchema
from pytest import raises

from revolt import substitute
from revolt.errors import SubstitutionError


def test_schema_dict_with_schema_dict_substitution():
    with given:
        sch = schema.dict

    with when:
        res = substitute(sch, sch)

    with then:
        assert res == sch
        assert id(res) != id(sch)


def test_schema_dict_with_schema_dict_with_value_substitution():
    with given:
        sch = schema.dict

    with given:
        clarification_type = schema.dict({})

    with when:
        res = substitute(sch, clarification_type)

    with then:
        assert sch == schema.dict
        assert res == clarification_type
        assert id(res) != id(clarification_type)
        assert id(res) != id(sch)


def test_schema_dict_with_value_with_schema_dict_with_same_value_substitution():
    with given:
        value = {}

    with given:
        sch = schema.dict(value)

    with given:
        clarification_type = schema.dict(value)

    with when:
        res = substitute(sch, clarification_type)

    with then:
        assert res == clarification_type
        assert id(res) != id(clarification_type)
        assert id(res) != id(sch)


def test_schema_dict_with_value_with_schema_dict_with_different_incomparable_value_substitution_error():
    with given:
        value = {'a': schema.int}
        another_value = {'b': schema.float}

    with given:
        sch = schema.dict(value)

    with given:
        clarification_type = schema.dict(another_value)

    with when, raises(Exception) as exception:
        substitute(sch, clarification_type)

    with then:
        assert exception.type is SubstitutionError
        assert sch == schema.dict(value)


def test_schema_dict_with_value_with_schema_dict_with_different_incomparable_value_on_subtype_substitution_error():
    with given:
        value = {'a': schema.int}
        another_value = {'a': schema.float}

    with given:
        sch = schema.dict(value)

    with given:
        clarification_type = schema.dict(another_value)

    with when, raises(Exception) as exception:
        substitute(sch, clarification_type)

    with then:
        assert exception.type is SubstitutionError
        assert sch == schema.dict(value)


def test_schema_dict_with_value_with_schema_dict_with_different_incomparable_value_on_subtype_value_substitution_error():
    with given:
        value = {'a': schema.int(1)}
        another_value = {'a': schema.int(2)}

    with given:
        sch = schema.dict(value)

    with given:
        clarification_type = schema.dict(another_value)

    with when, raises(Exception) as exception:
        substitute(sch, clarification_type)

    with then:
        assert exception.type is SubstitutionError
        assert sch == schema.dict(value)


@pytest.mark.parametrize("clarification_type", [
    schema.any,
    schema.bool,
    schema.bytes,
    schema.const,
    schema.float,
    schema.int,
    schema.list,
    schema.none,
    schema.str,
])
def test_schema_dict_with_different_schema_substitution_error(
    clarification_type: GenericSchema
):
    with given:
        sch = schema.dict

    with when, raises(Exception) as exception:
        substitute(sch, clarification_type)

    with then:
        assert exception.type is SubstitutionError
        assert sch == schema.dict
