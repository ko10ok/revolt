import pytest
from baby_steps import given, then, when
from district42 import schema, GenericSchema
from pytest import raises

from revolt import substitute
from revolt.errors import SubstitutionError


def test_none_schema_substitution():
    with given:
        sch = schema.none

    with given:
        clarification_type = schema.none

    with when:
        res = substitute(sch, clarification_type)

    with then:
        assert res == sch == schema.none
        assert id(res) != id(sch)


@pytest.mark.parametrize("clarification_type", [
    schema.any,
    schema.bool,
    schema.bytes,
    schema.const,
    schema.dict,
    schema.float,
    schema.int,
    schema.list,
    schema.str,
])
def test_none_substitution_with_another_schema_substitution__error(
    clarification_type: GenericSchema
):
    with given:
        sch = schema.none

    with when, raises(Exception) as exception:
        substitute(sch, clarification_type)

    with then:
        assert exception.type is SubstitutionError
        assert sch == schema.none
