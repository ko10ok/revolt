from copy import deepcopy

import pytest
from baby_steps import then, when, given
from district42 import schema, GenericSchema
from pytest import raises

from revolt import substitute
from revolt.errors import SubstitutionError

"""
DictSchema ranging via one steps clarifying mutations tree
    
    schema.dict ==
        schema.dict({...: ...}) >
        schema.dict({'a': schema.any, ...: ...}) >
        schema.dict({'a': schema.any, 'b': schema.any, ...: ...}) >
        schema.dict({'a': schema.any, 'b': schema.any})
    
    schema.dict < schema.dict({})
    schema.dict({'a': schema.any, ...: ...}) # split by any in any schema tests
    
    schema.dict({'a': schema.any, ...: ...}) >
        schema.dict({'a': schema.int, ...: ...})
    
    schema.dict({'a': schema.any}) >
        schema.dict({'a': schema.int})
    
    schema.dict({'a': schema.any, ...: ...}) >
        schema.dict({'a': schema.dict({'a': schema.int}), ...: ...})
    
    schema.dict({'a': schema.any, ...: ...}) >
        schema.dict({'a': schema.list([schema.int(1), schema.int(2), schema.int(3)])

"""


@pytest.mark.parametrize("basic_type,clarification_type", [
    (schema.dict, schema.dict({...: ...})),
    (schema.dict, schema.dict({'a': schema.any, ...: ...})),
    (schema.dict, schema.dict({'a': schema.any})),
    (schema.dict({...: ...}), schema.dict({...: ...})),
    (schema.dict({...: ...}), schema.dict({'a': schema.any, ...: ...})),
    (schema.dict({...: ...}), schema.dict({'a': schema.any})),
    (schema.dict({'a': schema.any, ...: ...}), schema.dict({'a': schema.any, ...: ...})),
    (
        schema.dict({'a': schema.any, ...: ...}),
        schema.dict({'a': schema.any, 'b': schema.any, ...: ...})
    ),
    (schema.dict({'a': schema.any, ...: ...}), schema.dict({'a': schema.any, 'b': schema.any})),
    (schema.dict, schema.dict({})),
    (schema.dict({'a': schema.any, ...: ...}), schema.dict({'a': schema.int, ...: ...})),
    (schema.dict({'a': schema.any}), schema.dict({'a': schema.int})),
    (
        schema.dict({'a': schema.any, ...: ...}),
        schema.dict({'a': schema.dict({'a': schema.int}), ...: ...})
    ),
    (
        schema.dict({'a': schema.any, ...: ...}),
        schema.dict({'a': schema.list([schema.int(1), schema.int(2), schema.int(3)])})
    ),
])
def test_dict_schema_clarification_with_dict_schema_with_subset_values_substitution(
    basic_type: GenericSchema,
    clarification_type: GenericSchema
):
    with given:
        sch = deepcopy(basic_type)

    with when:
        res = substitute(sch, clarification_type)

    with then:
        assert res == clarification_type
        assert sch == basic_type
        assert id(res) != id(clarification_type)
        assert id(res) != id(sch)


@pytest.mark.parametrize("basic_type,clarification_type", [
    # (schema.dict({...: ...}), schema.dict), ???
    (schema.dict({'a': schema.any, ...: ...}), schema.dict),
    (schema.dict({'a': schema.any}), schema.dict),
    (schema.dict({'a': schema.any, ...: ...}), schema.dict({...: ...})),
    (schema.dict({'a': schema.any}), schema.dict({...: ...})),
    (schema.dict({'a': schema.any, ...: ...}), schema.dict({'a': schema.any, ...: ...})),
    (
        schema.dict({'a': schema.any, 'b': schema.any, ...: ...}),
        schema.dict({'a': schema.any, ...: ...})
    ),
    (schema.dict({'a': schema.any, 'b': schema.any}), schema.dict({'a': schema.any, ...: ...})),
    (schema.dict({}), schema.dict),
    (schema.dict({'a': schema.int, ...: ...}), schema.dict({'a': schema.any, ...: ...})),
    (schema.dict({'a': schema.int}), schema.dict({'a': schema.any})),
    (
        schema.dict({'a': schema.dict({'a': schema.int}), ...: ...}),
        schema.dict({'a': schema.any, ...: ...})
    ),
    (
        schema.dict({'a': schema.list([schema.int(1), schema.int(2), schema.int(3)])}),
        schema.dict({'a': schema.any, ...: ...})
    ),
])
def test_schema_dict_clarification_with_dict_schema_with_superset_values_substitution_error(
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
