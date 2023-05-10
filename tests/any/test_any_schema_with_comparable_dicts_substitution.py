from copy import deepcopy

import pytest
from baby_steps import then, when, given
from district42 import schema, GenericSchema
from pytest import raises

from revolt import substitute
from revolt.errors import SubstitutionError


@pytest.mark.parametrize("basic_type,clarification_type,result", [
    (
        schema.any(
            schema.dict({'a': schema.int}),
            schema.dict({'b': schema.str})
        ),
        schema.dict({'a': schema.int}),
        schema.dict({'a': schema.int}),
    ),
    (
        schema.any(
            schema.dict({'a': schema.int}),
            schema.dict({'b': schema.str})
        ),
        schema.dict({'b': schema.str}),
        schema.dict({'b': schema.str}),
    ),
    (
        schema.any(
            schema.dict({'a': schema.int, 'b': schema.str}),
            schema.dict({'b': schema.str})
        ),
        schema.dict({'b': schema.str}),
        schema.dict({'b': schema.str}),
    ),
    (
        schema.any(
            schema.dict({'a': schema.int, 'b': schema.str}),
            schema.dict({'b': schema.str})
        ),
        schema.dict({'a': schema.int, 'b': schema.str}),
        schema.dict({'a': schema.int, 'b': schema.str}),
    ),
    (
        schema.any(
            schema.dict({'b': schema.str, ...: ...}),
            schema.dict({'b': schema.str, 'c': schema.float})
        ),
        schema.dict({'b': schema.str, 'c': schema.float}),
        schema.dict({'b': schema.str, 'c': schema.float}),  # should relax/reduce into 1?
    ),
    (
        schema.any(
            schema.dict({...: ...}),
            schema.dict({'a': schema.str})
        ),
        schema.dict({'a': schema.str}),
        schema.dict({'a': schema.str}),
    ),
    (
        schema.any(
            schema.dict({...: ...}),
            schema.dict({'a': schema.str})
        ),
        schema.dict({'b': schema.str}),
        schema.dict({'b': schema.str}),
    ),
    (
        schema.any(
            schema.dict({'a': schema.int, 'b': schema.str}),
            schema.dict({'b': schema.str, ...: ...})
        ),
        schema.dict({'b': schema.str}),
        schema.any(
            schema.dict({'a': schema.int, 'b': schema.str}),
            schema.dict({'b': schema.str})
        ),
    ),
])
def test_any_schema_clarification_with_dict_schema_with_subset_values_substitution(
    basic_type: GenericSchema,
    clarification_type: GenericSchema,
    result: GenericSchema,
):
    with given:
        sch = deepcopy(basic_type)

    with when:
        res = substitute(sch, clarification_type)

    with then:
        assert res == result
        assert sch == basic_type
        assert id(res) != id(clarification_type)
        assert id(res) != id(sch)


@pytest.mark.parametrize("basic_type,clarification_type", [
    (
        schema.dict({'a': schema.int}),
        schema.any(
            schema.dict({'a': schema.int}),
            schema.dict({'b': schema.str})
        ),
    ),
    (
        schema.dict({'b': schema.str}),
        schema.any(
            schema.dict({'a': schema.int}),
            schema.dict({'b': schema.str})
        ),
    ),
    (
        schema.dict({'b': schema.str}),
        schema.any(
            schema.dict({'a': schema.int, 'b': schema.str}),
            schema.dict({'b': schema.str})
        ),
    ),
    (
        schema.dict({'a': schema.int, 'b': schema.str}),
        schema.any(
            schema.dict({'a': schema.int, 'b': schema.str}),
            schema.dict({'b': schema.str})
        ),
    ),
    (
        schema.dict({'b': schema.str, ...: ...}),
        schema.any(
            schema.dict({'a': schema.int, 'b': schema.str, ...: ...}),
            schema.dict({'b': schema.str, 'c': schema.float})
        ),
    ),
    (
        schema.dict({'b': schema.str, 'c': schema.float}),
        schema.any(
            schema.dict({'b': schema.str, ...: ...}),
            schema.dict({'b': schema.str, 'c': schema.float})
        ),
    ),
    (
        schema.dict({'b': schema.str, 'c': schema.float}),
        schema.any(
            schema.dict({'b': schema.str, ...: ...}),
            schema.dict({'b': schema.str, 'c': schema.float})
        ),
    ),
    (
        schema.dict({'a': schema.str}),
        schema.any(
            schema.dict({...: ...}),
            schema.dict({'a': schema.str})
        ),
    ),
    (
        schema.dict({'b': schema.str}),
        schema.any(
            schema.dict({...: ...}),
            schema.dict({'a': schema.str})
        ),
    ),
    (
        schema.dict({'b': schema.str}),
        schema.any(
            schema.dict({'a': schema.int, 'b': schema.str}),
            schema.dict({'b': schema.str, ...: ...})
        ),
    ),
    (
        schema.any(
            schema.dict({'a': schema.int, 'b': schema.str}),
            schema.dict({'c': schema.float, 'b': schema.str})
        ),
        schema.dict({'b': schema.str})
    ),
    (
        schema.any(
            schema.dict({'a': schema.int, 'b': schema.str, ...: ...}),
            schema.dict({'b': schema.str, 'c': schema.float})
        ),
        schema.dict({'b': schema.str, ...: ...}),
    ),
    (
        schema.any(
            schema.dict({'a': schema.int, 'b': schema.str}),
            schema.dict({'b': schema.str, ...: ...})
        ),
        schema.dict({'b': schema.str}),
    ),
    (
        schema.any(
            schema.dict({'a': schema.int, 'b': schema.str}),
            schema.dict({'b': schema.str, 'c': schema.float})
        ),
        schema.dict({'b': schema.str, ...: ...}),
    ),
])
def test_schema_any_clarification_with_dict_schema_with_superset_values_substitution_error(
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
