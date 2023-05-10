from copy import deepcopy

import pytest
from baby_steps import then, when, given
from district42 import schema, GenericSchema
from pytest import raises

from revolt import substitute
from revolt.errors import SubstitutionError

"""
AnySchema ranging via one steps clarifying mutations tree
    
    schema.any > 
        schema.any(schema.str, schema.float, schema.int) >
        schema.any(schema.str, schema.float)
    
    schema.any(schema.str, schema.float, schema.int) > 
        schema.any(schema.str, schema.float(42), schema.int) > 
        schema.any(schema.str, schema.int)
"""


@pytest.mark.parametrize("basic_type,clarification_type", [
    (schema.any, schema.any(schema.str, schema.float, schema.int)),
    (
        schema.any(schema.str, schema.float, schema.int),
        schema.any(schema.str, schema.float)
    ),
    (
        schema.any(schema.str, schema.float, schema.int),
        schema.any(schema.str, schema.float(42.0), schema.int)
    ),
    (
        schema.any(schema.str, schema.float(42.0), schema.int),
        schema.any(schema.str, schema.int)
    ),
])
def test_any_schema_clarification_with_any_schema_with_subset_values_substitution(
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
    (schema.any(schema.str, schema.float, schema.int), schema.any),
    (
        schema.any(schema.str, schema.float),
        schema.any(schema.str, schema.float, schema.int)
    ),
    (
        schema.any(schema.str, schema.float(42.0), schema.int),
        schema.any(schema.str, schema.float, schema.int)
    ),
    (
        schema.any(schema.str, schema.int),
        schema.any(schema.str, schema.float(42.0), schema.int)
    ),
])
def test_schema_any_clarification_with_any_schema_with_superset_values_substitution_error(
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
