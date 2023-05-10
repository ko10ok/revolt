from copy import deepcopy

import pytest
from baby_steps import then, when, given
from district42 import schema, GenericSchema
from pytest import raises

from revolt import substitute
from revolt.errors import SubstitutionError


def test_schema_list_with_schema_list_substitution():
    with given:
        sch = schema.list

    with when:
        res = substitute(sch, sch)

    with then:
        assert res == sch
        assert id(res) != id(sch)


def test_schema_list_with_schema_list_with_value_substitution():
    with given:
        sch = schema.list

    with given:
        clarification_type = schema.list([])

    with when:
        res = substitute(sch, clarification_type)

    with then:
        assert sch == schema.list
        assert res == clarification_type
        assert id(res) != id(clarification_type)
        assert id(res) != id(sch)


def test_schema_list_with_value_with_schema_list_with_same_value_substitution():
    with given:
        value = []

    with given:
        sch = schema.list(value)

    with given:
        clarification_type = schema.list(value)

    with when:
        res = substitute(sch, clarification_type)

    with then:
        assert res == clarification_type
        assert id(res) != id(clarification_type)
        assert id(res) != id(sch)


def test_schema_list_with_value_with_schema_list_with_exact_same_value_substitution():
    with given:
        value = [schema.int(1), schema.int(2), schema.int(3)]
        another_value = [schema.int(1), schema.int(2), schema.int(3)]

    with given:
        sch = schema.list(value)

    with given:
        clarification_type = schema.list(another_value)

    with when:
        res = substitute(sch, clarification_type)

    with then:
        assert res == schema.list(value)


def test_schema_list_with_value_with_l_ellipsis_with_schema_list_with_sub_value_substitution():
    with given:
        value = [..., schema.int(1), schema.int(2), schema.int(3)]
        another_value = [schema.int(1), schema.int(2), schema.int(3)]

    with given:
        sch = schema.list(value)

    with given:
        clarification_type = schema.list(another_value)

    with when:
        res = substitute(sch, clarification_type)

    with then:
        assert res == schema.list(another_value)


def test_schema_list_with_value_with_r_ellipsis_with_schema_list_with_sub_value_substitution():
    with given:
        value = [schema.int(1), schema.int(2), schema.int(3), ...]
        another_value = [schema.int(1), schema.int(2), schema.int(3)]

    with given:
        sch = schema.list(value)

    with given:
        clarification_type = schema.list(another_value)

    with when:
        res = substitute(sch, clarification_type)

    with then:
        assert res == schema.list(another_value)


def test_schema_list_with_value_with_in_middle_ellipsis_with_schema_list_with_sub_value_substitution():
    with given:
        value = [schema.int(1), schema.int(2), ..., schema.int(3)]
        another_value = [schema.int(1), schema.int(2), schema.int(3)]

    with given:
        sch = schema.list(value)

    with given:
        clarification_type = schema.list(another_value)

    with when:
        res = substitute(sch, clarification_type)

    with then:
        assert res == schema.list(another_value)

def test_schema_list_with_value_with_ellipsis_with_schema_list_with_sub_2_possible_combinations_value_substitution():
    with given:
        value = [..., schema.int(1), schema.int(1), ...]
        another_value = [..., schema.int(1), schema.int(1), schema.int(1), ...]

    with given:
        sch = schema.list(value)

    with given:
        clarification_type = schema.list(another_value)

    with when:
        res = substitute(sch, clarification_type)

    with then:
        assert res == schema.list([..., schema.int(1), schema.int(1), schema.int(1), ...])


def test_schema_list_with_value_with_lr_ellipsis_with_schema_list_with_sub_value_substitution():
    with given:
        value = [..., schema.int(1), schema.int(2), schema.int(3), ...]
        another_value = [schema.int(1), schema.int(2), schema.int(3)]

    with given:
        sch = schema.list(value)

    with given:
        clarification_type = schema.list(another_value)

    with when:
        res = substitute(sch, clarification_type)

    with then:
        assert res == schema.list(another_value)


def test_schema_list_with_value_with_mlr_ellipsis_with_schema_list_with_sub_value_substitution():
    with given:
        value = [..., schema.int(1), schema.int(2), schema.int(3), ...]
        another_value = [schema.int(1), schema.int(2), schema.int(3)]

    with given:
        sch = schema.list(value)

    with given:
        clarification_type = schema.list(another_value)

    with when:
        res = substitute(sch, clarification_type)

    with then:
        assert res == schema.list(another_value)


def test_schema_list_with_value_with_schema_list_with_different_incomparable_value_substitution_error():
    with given:
        value = [schema.int(1), schema.int(2), schema.int(3)]
        another_value = [schema.int(3), schema.int(2), schema.int(1)]

    with given:
        sch = schema.list(value)

    with given:
        clarification_type = schema.list(another_value)

    with when, raises(Exception) as exception:
        substitute(sch, clarification_type)

    with then:
        assert exception.type is SubstitutionError
        assert sch == schema.list(value)


def test_schema_list_with_value_with_schema_list_with_different_incomparable_value_over_subtype_substitution_error():
    with given:
        value = [schema.int]
        another_value = [schema.float]

    with given:
        sch = schema.list(value)

    with given:
        clarification_type = schema.list(another_value)

    with when, raises(Exception) as exception:
        substitute(sch, clarification_type)

    with then:
        assert exception.type is SubstitutionError
        assert sch == schema.list(value)


def test_schema_list_with_value_with_schema_list_with_different_incomparable_value_on_subtype_value_substitution_error():
    with given:
        value = [schema.int(1)]
        another_value = [schema.int(2)]

    with given:
        sch = schema.list(value)

    with given:
        clarification_type = schema.list(another_value)

    with when, raises(Exception) as exception:
        substitute(sch, clarification_type)

    with then:
        assert exception.type is SubstitutionError
        assert sch == schema.list(value)


@pytest.mark.parametrize("basic_type,clarification_type", [
    (
        schema.list([..., schema.int, ...]),
        schema.list([..., schema.float, ...])
    ),
    (
        schema.list([..., schema.float, schema.int, ...]),
        schema.list([..., schema.int, schema.float, ...])
    ),
    (
        schema.list([..., schema.float, schema.int, ...]),
        schema.list([..., schema.int, ...]).len(1)
    ),
])
def test_schema_list_with_value_with_schema_list_with_different_incomparable_value_on_partial_value_substitution_error(
    basic_type: GenericSchema,
    clarification_type: GenericSchema
):
    with given:
        sch = deepcopy(basic_type)

    with when, raises(Exception) as exception:
        substitute(sch, clarification_type)

    with then:
        assert exception.type is SubstitutionError
        assert sch == basic_type


@pytest.mark.parametrize("clarification_type", [
    schema.any,
    schema.bool,
    schema.bytes,
    schema.const,
    schema.float,
    schema.int,
    schema.dict,
    schema.none,
    schema.str,
])
def test_schema_list_with_different_schema_substitution_error(
    clarification_type: GenericSchema
):
    with given:
        sch = schema.list

    with when, raises(Exception) as exception:
        substitute(sch, clarification_type)

    with then:
        assert exception.type is SubstitutionError
        assert sch == schema.list
