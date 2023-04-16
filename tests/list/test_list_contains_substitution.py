from typing import Any, List

import pytest
from baby_steps import given, then, when
from district42 import schema
from pytest import raises

from revolt import substitute
from revolt.errors import SubstitutionError


def test_list_contains_empty_substitution():
    with given:
        sch = schema.list([...])

    with when:
        res = substitute(sch, [])

    with then:
        assert res == schema.list([])
        assert res != sch


def test_list_contains_elements_substitution():
    with given:
        sch = schema.list([...])

    with when:
        res = substitute(sch, [1, 2])

    with then:
        assert res == schema.list([schema.int(1), schema.int(2)])
        assert res != sch


@pytest.mark.parametrize("value", [
    [1, 2],
    [1, 2, 3],
])
def test_list_contains_head_elements_substitution(value: List[Any]):
    with given:
        sch = schema.list([schema.int(1), schema.int(2), ...])

    with when:
        res = substitute(sch, value)

    with then:
        assert res == schema.list([substitute(schema.int, x) for x in value])
        assert res != sch


def test_list_contains_head_less_elements_substitution_error():
    with given:
        sch = schema.list([schema.int(1), schema.int(2), ...])

    with when, raises(Exception) as exception:
        substitute(sch, [1])

    with then:
        assert exception.type is SubstitutionError


@pytest.mark.parametrize("value", [
    [1, 2],
    [0, 1, 2],
])
def test_list_contains_tail_elements_substitution(value: List[Any]):
    with given:
        sch = schema.list([..., schema.int(1), schema.int(2)])

    with when:
        res = substitute(sch, value)

    with then:
        assert res == schema.list([substitute(schema.int, x) for x in value])
        assert res != sch


def test_list_contains_tail_less_elements_substitution_error():
    with given:
        sch = schema.list([..., schema.int(1), schema.int(2)])

    with when, raises(Exception) as exception:
        substitute(sch, [1])

    with then:
        assert exception.type is SubstitutionError


@pytest.mark.parametrize("value", [
    [1, 2],
    [0, 1, 2, 3],
    [0, 1, 2],
    [1, 2, 3],
])
def test_list_contains_body_elements_substitution(value: List[Any]):
    with given:
        sch = schema.list([..., schema.int(1), schema.int(2), ...])

    with when:
        res = substitute(sch, value)

    with then:
        assert res == schema.list([substitute(schema.int, x) for x in value])
        assert res != sch


def test_list_contains_body_less_elements_substitution_error():
    with given:
        sch = schema.list([..., schema.int(1), schema.int(2), ...])

    with when, raises(Exception) as exception:
        substitute(sch, [1])

    with then:
        assert exception.type is SubstitutionError


def test_list_contains_body_empty_elements_substitution_error():
    with given:
        sch = schema.list([..., schema.int, ...])

    with when, raises(Exception) as exception:
        substitute(sch, [])

    with then:
        assert exception.type is SubstitutionError


def test_list_contains_body_elements_with_len_substitution():
    with given:
        sch = schema.list([..., schema.int(1), schema.int(2), ...]).len(2)

    with when:
        res = substitute(sch, [1, 2])

    with then:
        assert res == schema.list([schema.int(1), schema.int(2)]).len(2)
        assert res != sch


@pytest.mark.parametrize("value", [
    [1, 2, 3],
    [0, 1, 2],
    [0, 1, 2, 3],
])
def test_list_contains_body_elements_with_len_substitution_error(value: List[Any]):
    with given:
        sch = schema.list([..., schema.int(1), schema.int(2), ...]).len(2)

    with when, raises(Exception) as exception:
        substitute(sch, value)

    with then:
        assert exception.type is SubstitutionError


def test_list_contains_some_substitution_error():
    with given:
        sch = schema.list([...])

    with when, raises(Exception) as exception:
        substitute(sch, [...])

    with then:
        assert exception.type is SubstitutionError


def test_list_contains_ellipsis_substitution_error():
    with given:
        sch = schema.list

    with when, raises(Exception) as exception:
        substitute(sch, [...])

    with then:
        assert exception.type is SubstitutionError


def test_list_contains_all_ellipsis_substitution_error():
    with given:
        sch = schema.list

    with when, raises(Exception) as exception:
        substitute(sch, [..., ...])

    with then:
        assert exception.type is SubstitutionError


def test_list_contains_substitution_head():
    with given:
        sch = schema.list

    with when:
        res = substitute(sch, [1, 2, ...])

    with then:
        assert res == schema.list([schema.int(1), schema.int(2), ...])
        assert res != sch


def test_list_contains_substitution_tail():
    with given:
        sch = schema.list

    with when:
        res = substitute(sch, [..., 1, 2])

    with then:
        assert res == schema.list([..., schema.int(1), schema.int(2)])
        assert res != sch


def test_list_contains_substitution_body():
    with given:
        sch = schema.list

    with when:
        res = substitute(sch, [..., 1, 2, ...])

    with then:
        assert res == schema.list([..., schema.int(1), schema.int(2), ...])
        assert res != sch


def test_list_contains_substitution_with_exect_values():
    with given:
        sch = schema.list([..., schema.int, schema.float, ...])

    with when:
        res = substitute(sch, [1, 2.0])

    with then:
        assert res == schema.list([schema.int(1), schema.float(2.0)])
        assert res != sch


def test_list_contains_substitution_with_contains_values():
    with given:
        sch = schema.list([..., schema.int, schema.float, ...])

    with when:
        res = substitute(sch, [..., 1, 2.0, ...])  # TODO should we?

    with then:
        assert res == schema.list([schema.int(1), schema.float(2.0)])
        assert res != sch


def test_list_contains_substitution_with_schema_contains_values():
    with given:
        sch = schema.list([..., schema.int, schema.float, ...])

    with when:
        res = substitute(sch, schema.list([..., schema.int(1), schema.float(2.0), ...]))

    with then:
        assert res == schema.list([..., schema.int(1), schema.float(2.0), ...])
        assert res != sch


def test_list_contains_substitution_with_constant_count_values():
    with given:
        sch = schema.list([..., schema.int, schema.float, ...])

    with when:
        res = substitute(sch, schema.list([schema.int(1), schema.float(2.0)]))

    with then:
        assert res == schema.list([schema.int(1), schema.float(2.0)])
        assert res != sch

# TODO error should be, check case
# def test_list_contains_substitution_with_multiple_cases_contains_values():
#     with given:
#         sch = schema.list([..., schema.int, schema.int, schema.float, ...])
#
#     with when:
#         res = substitute(sch, schema.list([..., schema.int(1), schema.float(2.0), ...]))
#
#     with then:
#         assert res == schema.any(
#             schema.list([..., schema.int(1), schema.int, schema.float(2.0), ...]),
#             schema.list([..., schema.int, schema.int(1), schema.float(2.0), ...]),
#             schema.list([
#                 ..., schema.int(1), schema.float(2.0), schema.int, schema.int, schema.float, ...
#             ]),
#             schema.list([
#                 ..., schema.int(1), schema.float(2.0), ..., schema.int, schema.int,
#                 schema.float, ...
#             ]),
#             schema.list([
#                 schema.int(1), schema.float(2.0), ..., schema.int, schema.int, schema.float, ...
#             ]),
#             schema.list([
#                 ..., schema.int, schema.int, schema.float, ..., schema.int(1), schema.float(
#                 2.0), ...
#             ]),
#             schema.list([
#                 ..., schema.int, schema.int, schema.float, ..., schema.int(1), schema.float(2.0)
#             ]),
#         )
#         assert res != sch

# TODO error should be, check case
# def test_list_contains_substitution_with_one_extra_with_multiple_cases_contains_values():
#     with given:
#         sch = schema.list([..., schema.int, schema.int, schema.float, ...])
#
#     with when:
#         res = substitute(sch, schema.list([..., schema.float(2.0), schema.int(1), ...]))
#
#     with then:
#         assert res == schema.any(
#             schema.list([..., schema.int, schema.int, schema.float(2.0), schema.int(1), ...]),
#             schema.list([
#                 ..., schema.int, schema.int, schema.float, schema.float(2.0), schema.int(1), ...
#             ]),
#             schema.list([..., schema.float(2.0), schema.int(1), schema.int, schema.float, ...]),
#             schema.list([
#                 ..., schema.float(2.0), schema.int(1), schema.int, schema.int, schema.float, ...
#             ]),
#         )
#         assert res != sch
