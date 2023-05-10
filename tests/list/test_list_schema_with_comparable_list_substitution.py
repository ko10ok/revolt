from copy import deepcopy

import pytest
from baby_steps import then, when, given
from district42 import schema, GenericSchema
from pytest import raises

from revolt import substitute
from revolt.errors import SubstitutionError

"""
ListSchema ranging via one steps clarifying mutations tree
    
    schema.list == schema.list([...]) == schema.list(schema.any)
        
    schema.list([...]) > schema.list.len(3) == schema.list([schema.any] * 3)
    
    schema.list([...]) > 
        schema.list([..., schema.int, ...]) >
        schema.list([..., schema.int, schema.float, ...]) > 
        schema.list([..., schema.int, schema.float]) >
        schema.list([schema.int, schema.float])
    
    schema.list([..., schema.int, schema.float, ...]) >
        schema.list([schema.int, schema.float, ...]) >
        schema.list([schema.int, schema.float])
    
    schema.list([..., schema.int, ...]) > schema.list([..., schema.int, ...]).len(3) 
    
    schema.list > schema.list([])
    
    schema.list(schema.any) > schema.list([schema.any]) == schema.list(schema.any).len(1)
    
    schema.list(schema.any) > schema.list(schema.int)
"""


@pytest.mark.parametrize("basic_type,clarification_type", [
    (schema.list, schema.list([...])),
    (schema.list([...]), schema.list),
    (schema.list(schema.any), schema.list),  # ????
    (schema.list, schema.list(schema.any)),
    (schema.list([...]), schema.list.len(3)),
    (schema.list.len(3), schema.list([schema.any] * 3)),
    (schema.list([schema.any] * 3), schema.list.len(3)),
    (schema.list([...]), schema.list([..., schema.int, ...])),
    (
        schema.list([..., schema.int, ...]),
        schema.list([..., schema.int, schema.float, ...])
    ),
    (
        schema.list([..., schema.int, schema.float, ...]),
        schema.list([..., schema.int, schema.float])
    ),
    (
        schema.list([..., schema.int, schema.float]),
        schema.list([schema.int, schema.float])
    ),
    (
        schema.list([..., schema.int, schema.float, ...]),
        schema.list([schema.int, schema.float, ...])
    ),
    (
        schema.list([schema.int, schema.float, ...]),
        schema.list([schema.int, schema.float])
    ),
    (
        schema.list([..., schema.int, ...]),
        schema.list([..., schema.int, ...]).len(3)
    ),
    (
        schema.list([...]),
        schema.list([])
    ),
    (
        schema.list([...]),
        schema.list([])
    ),
    (
        schema.list([..., schema.str, schema.int, schema.str, ...]),
        schema.list([..., schema.str, schema.int, schema.str, ...]).len(3)
    ),
    (schema.list(schema.any), schema.list([schema.any])),  # ????
    (schema.list([schema.any]), schema.list(schema.any)),  # ????
    (schema.list(schema.any), schema.list(schema.int)),
    (schema.list(schema.any), schema.list(schema.int(1))),
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
    (schema.list.len(3), schema.list([...])),
    (schema.list([schema.any] * 3), schema.list.len(3)),
    (schema.list.len(3), schema.list([schema.any] * 3)),
    (schema.list([..., schema.int, ...]), schema.list([...])),
    (
        schema.list([..., schema.int, schema.float, ...]),
        schema.list([..., schema.int, ...])
    ),
    (
        schema.list([..., schema.int, schema.float]),
        schema.list([..., schema.int, schema.float, ...])
    ),
    (
        schema.list([schema.int, schema.float]),
        schema.list([..., schema.int, schema.float])
    ),
    (
        schema.list([schema.int, schema.float, ...]),
        schema.list([..., schema.int, schema.float, ...])
    ),
    (
        schema.list([schema.int, schema.float]),
        schema.list([schema.int, schema.float, ...])
    ),
    (
        schema.list([..., schema.int, ...]).len(3),
        schema.list([..., schema.int, ...])
    ),
    (
        schema.list([..., schema.str, schema.int, schema.str, ...]).len(3),
        schema.list([..., schema.str, schema.int, schema.str, ...]),
    ),
    (schema.list(schema.int), schema.list(schema.any),),
    (schema.list(schema.int(1)), schema.list(schema.any)),

    (
        schema.list([..., schema.float, schema.int, ...]),
        schema.list([..., schema.int]).len(2)
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
