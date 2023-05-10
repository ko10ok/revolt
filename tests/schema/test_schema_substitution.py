import pytest
from baby_steps import then, when
from district42 import schema, GenericSchema

from revolt import substitute


# basic types

@pytest.mark.parametrize("basic_type,substitution_type", [
    *[(sch, sch) for sch in [
        schema.any,  # AnySchema,
        schema.bool,  # BoolSchema,
        schema.bytes,  # BytesSchema,
        schema.const,  # ConstSchema,
        schema.dict,  # DictSchema,
        schema.float,  # FloatSchema,
        schema.int,  # IntSchema,
        schema.list,  # ListSchema,
        schema.none,  # NoneSchema,
        schema.str,  # StrSchema,
    ]]  # all in same schema
])
def test_schema_with_same_schema_substitution(basic_type: GenericSchema,
                                              substitution_type: GenericSchema):
    with when:
        res = substitute(basic_type, substitution_type)

    with then:
        assert res == substitution_type
        assert id(res) != id(substitution_type) != id(basic_type)


@pytest.mark.parametrize("basic_type,substitution_type", [
    [schema.any, schema.any(
        schema.dict({'a': schema.int(1)}),
        schema.list([schema.int(1), schema.int(2), schema.int(4)]),
        schema.bool(True),
        schema.bytes(b'bytearray'),
        schema.float(2.427),
        schema.int(123),
        schema.none,
        schema.str('any str'),
    )],
    [schema.dict, schema.dict({'a': schema.int(1)})],
    [schema.list, schema.list([schema.int(1), schema.int(2), schema.int(4)])],
    [schema.bool, schema.bool(True)],
    [schema.bool, schema.bool(False)],
    [schema.bytes, schema.bytes(b'bytearray')],
    [schema.float, schema.float(2.427)],
    [schema.int, schema.int(123)],
    [schema.none, schema.none],
    [schema.str, schema.str('any str')],
])
def test_schema_with_same_schema_with_value_substitution(
    basic_type: GenericSchema,
    substitution_type: GenericSchema
):
    with when:
        res = substitute(basic_type, substitution_type)

    with then:
        assert res == substitution_type
        assert id(res) != id(substitution_type) != id(basic_type)


@pytest.mark.parametrize("basic_type,substitution_type", [
    [schema.any(
        schema.dict({'a': schema.int(1)}),
        schema.list([schema.int(1), schema.int(2), schema.int(4)]),
        schema.bool(True),
        schema.bool(False),
        schema.bytes(b'bytearray'),
        schema.float(2.427),
        schema.int(123),
        schema.none,
        schema.str('any str'),
    ), schema.any],
    [schema.dict({'a': schema.int(1)}), schema.dict],
    [schema.list([schema.int(1), schema.int(2), schema.int(4)]), schema.list],
    [schema.bool(True), schema.bool],
    [schema.bool(False), schema.bool],
    [schema.bytes(b'bytearray'), schema.bytes],
    [schema.float(2.427), schema.float],
    [schema.int(123), schema.int],
    [schema.none, schema.none],
    [schema.str('any str'), schema.str],
])
def test_schema_with_value_with_same_schema_without_value_substitution(
    basic_type: GenericSchema,
    substitution_type: GenericSchema
):
    # TODO substitution error, more detailed type already defined
    pass


@pytest.mark.parametrize("basic_and_substitution_type", [
    schema.any(
        schema.dict({'a': schema.int(1)}),
        schema.list([schema.int(1), schema.int(2), schema.int(4)]),
        schema.bool(True),
        schema.bytes(b'bytearray'),
        schema.float(2.427),
        schema.int(123),
        schema.none,
        schema.str('any str'),
    ),
    schema.dict({'a': schema.int(1)}),
    schema.list([schema.int(1), schema.int(2), schema.int(4)]),
    schema.bool(True),
    schema.bytes(b'bytearray'),
    schema.float(2.427),
    schema.int(123),
    schema.none,
    schema.str('any str'),
])
def test_schema_with_value_with_same_schema_with_same_value_substitution(
    basic_and_substitution_type: GenericSchema
):
    with when:
        res = substitute(basic_and_substitution_type, basic_and_substitution_type)

    with then:
        assert res == basic_and_substitution_type
        assert id(res) != id(basic_and_substitution_type)


@pytest.mark.parametrize("basic_type,substitution_type", [
    [schema.any(schema.dict({'b': schema.int(2)}),
                schema.list([schema.int(1), schema.int(3), schema.int(4)]),
                schema.bool(False),
                schema.bytes(b'bytearray'),
                schema.float(2.427),
                schema.int(123),
                schema.none,
                schema.str('any str'),
                ),
     schema.any(schema.dict({'a': schema.int(1)}),
                schema.list([schema.int(1), schema.int(2), schema.int(4)]),
                schema.bool(True),
                schema.bytes(b'bitlist'),
                schema.float(9.427),
                schema.int(321),
                schema.str('any another str'),
                )],
    [schema.dict({'a': schema.int(1)}), schema.dict({'b': schema.int(1)})],
    [schema.list([schema.int(1), schema.int(4), schema.int(4)]), schema.list([schema.int(1), schema.int(2), schema.int(4)])],
    [schema.bool(True), schema.bool(False)],
    [schema.bool(False), schema.bool(True)],
    [schema.bytes(b'bytearray'), schema.bytes(b'bitlist')],
    [schema.float(2.527), schema.float(1.427)],
    [schema.int(123), schema.int(321)],
    [schema.str('any str'), schema.str('any other str')],
])
def test_schema_with_value_with_same_schema_with_different_value_substitution(
    basic_type: GenericSchema,
    substitution_type: GenericSchema
):
    # TODO substitution error, mismatched detailed type already defined
    pass


# schema mismatch schema.dict % schema.str

# composite types
# dict
@pytest.mark.parametrize("basic_type,substitution_type", [
    (schema.dict({'a': schema.int}), schema.dict({'a': schema.int})),
    (schema.dict({'a': schema.int}), schema.dict({'a': schema.int(1)})),
    (schema.dict({'a': schema.dict}), schema.dict({'a': schema.dict({'a': schema.int(1)})})),
    (schema.dict({'a': schema.list}), schema.dict({'a': schema.list})),
    (schema.dict({'a': schema.list}),
     schema.dict({'a': schema.list([schema.int(1), schema.int(2), schema.int(3)])})),
])
def test_dict_schema_clarification_with_dict_with_values_schema_substitution(
    basic_type: GenericSchema,
    substitution_type: GenericSchema
):
    with when:
        res = substitute(basic_type, substitution_type)

    with then:
        assert res == substitution_type
        assert id(res) != id(substitution_type) != id(basic_type)


# dict partial
@pytest.mark.parametrize("basic_type,substitution_type", [
    (
        schema.dict({...: ...}),
        schema.dict({'a': schema.int})
    ),
    (
        schema.dict({'a': schema.int, ...: ...}),
        schema.dict({'a': schema.int})
    ),
    (
        schema.dict({'a': schema.int, ...: ...}),
        schema.dict({'a': schema.int, 'b': schema.str})
    ),
    (
        schema.dict({'a': schema.int, ...: ...}),
        schema.dict({'a': schema.int, ...: ...})
    ),
    (
        schema.dict({...: ...}),
        schema.dict({'a': schema.int, ...: ...})
    ),
    (
        schema.dict({'a': schema.int, ...: ...}),
        schema.dict({'a': schema.int, 'b': schema.str, ...: ...})
    ),
    (
        schema.dict({'a': schema.int, ...: ...}),
        schema.dict({'a': schema.int, 'b': schema.str})
    ),
])
def test_partial_dict_schema_clarification_with_partial_dict_schema_substitution(
    basic_type: GenericSchema,
    substitution_type: GenericSchema
):
    with when:
        res = substitute(basic_type, substitution_type)

    with then:
        assert res == substitution_type
        assert id(res) != id(substitution_type) != id(basic_type)


# dict extensions entropy up failed
@pytest.mark.parametrize("basic_type,substitution_type", [
    (
        schema.dict({'a': schema.int, 'b': schema.str}),
        schema.dict({'a': schema.int, ...: ...}),
    ),
    (
        schema.dict({'a': schema.int, 'b': schema.str}),
        schema.dict({'a': schema.int, 'c': schema.str}),
    ),
    (
        schema.dict({'a': schema.int, ...: ...}),
        schema.dict({'c': schema.int}),
    ),
])
def test_dict_schema_extension_with_partial_dict_schema_substitution_forbidden(
    basic_type: GenericSchema,
    substitution_type: GenericSchema
):
    # TODO substitution error, missmatched detailed type already defined
    pass


# list
@pytest.mark.parametrize("basic_type,substitution_type", [
    (schema.list(schema.int), schema.list(schema.int)),
    (schema.list(schema.int), schema.list(schema.int(1))),
    (schema.list(schema.list), schema.list(schema.list)),
    (schema.list(schema.list), schema.list(schema.list(schema.int(1)))),
    (schema.list(schema.dict), schema.list(schema.dict)),
    (schema.list(schema.dict), schema.list(schema.dict({'a': schema.int(1)}))),
])
def test_list_schema_clarification_with_list_with_values_schema_substitution(
    basic_type: GenericSchema,
    substitution_type: GenericSchema
):
    with when:
        res = substitute(basic_type, substitution_type)

    with then:
        assert res == substitution_type
        assert id(res) != id(substitution_type) != id(basic_type)


# list partial
@pytest.mark.parametrize("basic_type,substitution_type", [
    (schema.list([schema.int, ...]), schema.list([schema.int])),
    (schema.list([schema.int, ...]), schema.list([schema.int, schema.str])),
    (schema.list([..., schema.int]), schema.list([schema.int])),
    (schema.list([..., schema.int]), schema.list([schema.str, schema.int])),
    (schema.list([..., schema.int, ...]), schema.list([schema.int])),
    (schema.list([..., schema.int, ...]), schema.list([schema.str, schema.int, schema.str])),
    (schema.list([..., schema.int, ...]), schema.list([schema.str, schema.str, schema.int])),
])
def test_list_schema_clarification_with_list_with_values_schema_substitution(
    basic_type: GenericSchema,
    substitution_type: GenericSchema
):
    with when:
        res = substitute(basic_type, substitution_type)

    with then:
        assert res == substitution_type
        assert id(res) != id(substitution_type) != id(basic_type)


# list extensions entropy up failed
@pytest.mark.parametrize("basic_type,substitution_type", [
    (schema.list([schema.int]), schema.list([schema.int, ...])),
    (schema.list([schema.int]), schema.list([..., schema.int])),
    (schema.list([schema.int]), schema.list([..., schema.int, ...])),
    (schema.list([schema.int, ...]), schema.list([schema.str, schema.int, schema.str])),
    (schema.list([..., schema.int]), schema.list([schema.str, schema.int, schema.str])),
    (schema.list([..., schema.int, ...]), schema.list([schema.str])),
    (schema.list([..., schema.int, ...]), schema.list([schema.str, schema.str])),
    (schema.list([..., schema.int, ...]), schema.list([schema.str, schema.str, schema.str])),
])
def test_list_schema_extension_with_list_with_values_schema_substitution_forbidden(
    basic_type: GenericSchema,
    substitution_type: GenericSchema
):
    with when:
        res = substitute(basic_type, substitution_type)

    with then:
        assert res == substitution_type
        assert id(res) != id(substitution_type) != id(basic_type)


# any % basic
@pytest.mark.parametrize("basic_type,substitution_type,result", [
    *[(schema.any, sch, sch) for sch in [
        schema.any,  # AnySchema,
        schema.bool,  # BoolSchema,
        schema.bytes,  # BytesSchema,
        schema.const,  # ConstSchema,
        schema.dict,  # DictSchema,
        schema.float,  # FloatSchema,
        schema.int,  # IntSchema,
        schema.list,  # ListSchema,
        schema.none,  # NoneSchema,
        schema.str,  # StrSchema,
    ]],
    (
        schema.any(schema.int, schema.str),
        schema.int,
        schema.int,
    ),
    (
        schema.any(schema.int, schema.str),
        schema.str,
        schema.str,
    ),
])
def test_any_schema_clarification_with_one_basic_schema_substitution(
    basic_type: GenericSchema,
    substitution_type: GenericSchema,
    result: GenericSchema,
):
    with when:
        res = substitute(basic_type, substitution_type)

    with then:
        assert res == result
        assert id(res) != id(substitution_type) != id(basic_type)


@pytest.mark.parametrize("basic_type,substitution_type", [
    (
        schema.any(schema.int, schema.str),
        schema.float,
    ),
])
def test_any_of_some_schemas_extension_with_different_case_schema_substitution_forbidden(
    basic_type: GenericSchema,
    substitution_type: GenericSchema,
):
    # TODO substitution error, missmatched detailed type already defined
    pass


# cross composite

# any % any
@pytest.mark.parametrize("basic_type,substitution_type,result", [

    (
        schema.any(
            schema.dict({'a': schema.int, 'b': schema.str}),
            schema.dict({'b': schema.str})
        ),
        schema.any(
            schema.dict({'a': schema.int, 'b': schema.str}),
            schema.dict({'b': schema.str})
        ),
        schema.any(
            schema.dict({'a': schema.int, 'b': schema.str}),
            schema.dict({'b': schema.str})
        ),
    ),
])
def test_any_of_some_schemas_clarification_with_any_of_same_schemas_substitution(
    basic_type: GenericSchema,
    substitution_type: GenericSchema,
    result: GenericSchema,
):
    with when:
        res = substitute(basic_type, substitution_type)

    with then:
        assert res == result
        assert id(res) != id(substitution_type) != id(basic_type)


@pytest.mark.parametrize("basic_type,substitution_type", [
    (
        schema.any(
            schema.dict({'a': schema.int}),
            schema.dict({'b': schema.str})
        ),
        schema.any(
            schema.dict({'a': schema.int}),
            schema.dict({'c': schema.str})
        ),
    ),
])
def test_any_of_some_schemas_clarification_with_any_of_another_schemas_substitution_forbidden(
    basic_type: GenericSchema,
    substitution_type: GenericSchema,
):
    # TODO substitution error, missmatched detailed type already defined
    pass


# any dict
@pytest.mark.parametrize("basic_type,substitution_type,result", [
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
            schema.dict({'a': schema.int, 'b': schema.str, ...: ...}),
            schema.dict({'b': schema.str, 'c': schema.float})
        ),
        schema.dict({'b': schema.str, ...: ...}),
        schema.any(
            schema.dict({'a': schema.int, 'b': schema.str, ...: ...}),
            schema.dict({'b': schema.str, 'c': schema.str})  # mby should exclude?
        ),
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
            schema.dict({'b': schema.str, ...: ...}),
            schema.dict({'b': schema.str, 'c': schema.float})
        ),
        schema.dict({'b': schema.str, 'c': schema.float}),
        schema.dict({'b': schema.str, 'c': schema.float}),
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
def test_any_with_dict_cases_schema_clarification_with_one_of_sub_dicts_schema_substitution(
    basic_type: GenericSchema,
    substitution_type: GenericSchema,
    result: GenericSchema,
):
    with when:
        res = substitute(basic_type, substitution_type)

    with then:
        assert res == result
        assert id(res) != id(substitution_type) != id(basic_type)


# any dict failed
@pytest.mark.parametrize("basic_type,substitution_type", [
    (
        schema.any(
            schema.dict({'a': schema.int, 'b': schema.str}),
            schema.dict({'c': schema.float, 'b': schema.str})
        ),
        schema.dict({'b': schema.str})
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
def test_any_with_some_dict_cases_schema_clarification_with_another_sub_dict_schema_substitution(
    basic_type: GenericSchema,
    substitution_type: GenericSchema,
    result: GenericSchema,
):
    # TODO substitution error, missmatched detailed type already defined
    pass


# any list
@pytest.mark.parametrize("basic_type,substitution_type,result", [
    (
        schema.any(
            schema.list(schema.int),
            schema.list(schema.str)
        ),
        schema.list(schema.int),
        schema.dict({'a': schema.int}),
    ),
    (
        schema.any(
            schema.list([schema.int, schema.str]),
            schema.list([schema.int])
        ),
        schema.list([schema.int]),
        schema.list([schema.int]),
    ),
    (
        schema.any(
            schema.list([schema.int, schema.str]),
            schema.list([schema.int])
        ),
        schema.list([schema.int, schema.str]),
        schema.list([schema.int, schema.str]),
    ),
    (
        schema.any(
            schema.list([schema.int, ...]),
            schema.list([schema.int])
        ),
        schema.list([schema.int, ...]),
        schema.list([schema.int, ...]),
    ),
    (
        schema.any(
            schema.list([schema.int, ...]),
            schema.list([schema.str])
        ),
        schema.list([schema.int]),
        schema.list([schema.int]),
    ),
    (
        schema.any(
            schema.list([..., schema.int]),
            schema.list([schema.int])
        ),
        schema.list([..., schema.int]),
        schema.list([..., schema.int]),
    ),
    (
        schema.any(
            schema.list([..., schema.int, ...]),
            schema.list([schema.int])
        ),
        schema.list([..., schema.int, ...]),
        schema.list([..., schema.int, ...]),
    ),

    (
        schema.any(
            schema.list([..., schema.int, ...]),
            schema.list([schema.str, schema.int, schema.str])
        ),
        schema.list([..., schema.int, ...]),
        schema.list([..., schema.int, ...]),
    ),
    # ( # fail
    #     schema.any(
    #         schema.list([schema.int]),
    #         schema.list([schema.str, schema.int, schema.str])
    #     ),
    #     schema.list([..., schema.int, ...]),
    #     schema.list([..., schema.int, ...]),
    # ),
    (
        schema.any(
            schema.list([schema.int, ...]),
            schema.list([schema.int, schema.str])
        ),
        schema.list([schema.int, schema.str]),
        schema.list([schema.int, schema.str]),
    ),
    (
        schema.any(
            schema.list([...]),
            schema.list([schema.int, schema.str])
        ),
        schema.list([schema.int]),
        schema.list([schema.int]),
    ),
    (
        schema.any(
            schema.list,
            schema.list([schema.int, schema.str])
        ),
        schema.list(schema.int),
        schema.list(schema.int),
    ),
])
def test_any_with_list_schema_clarification_with_one_of_sub_list_schema_substitution(
    basic_type: GenericSchema,
    substitution_type: GenericSchema,
    result: GenericSchema,
):
    with when:
        res = substitute(basic_type, substitution_type)

    with then:
        assert res == result
        assert id(res) != id(substitution_type) != id(basic_type)


# any any-dict
@pytest.mark.parametrize("basic_type,substitution_type,result", [
    (
        schema.any(
            schema.dict({'a': schema.int}),
            schema.dict({'b': schema.str})
        ),
        schema.any(
            schema.dict({'b': schema.str}),
            schema.dict({'a': schema.int})
        ),
        schema.any(
            schema.dict({'a': schema.int}),
            schema.dict({'b': schema.str})
        ),
    ),
    (
        schema.any(
            schema.dict({'a': schema.int, 'b': schema.str}),
            schema.dict({'a': schema.int, 'b': schema.str, 'c': schema.float}),
            schema.dict({'a': schema.int, 'b': schema.str, 'd': schema.float}),
        ),
        schema.any(
            schema.dict({'a': schema.int, 'b': schema.str}),
            schema.dict({'a': schema.int, 'b': schema.str, 'd': schema.float}),
        ),
        schema.any(
            schema.dict({'a': schema.int, 'b': schema.str}),
            schema.dict({'a': schema.int, 'b': schema.str, 'd': schema.float}),
        ),
    ),
    (
        schema.any(
            schema.dict({'a': schema.int, 'b': schema.str}),
            schema.dict({'a': schema.int, 'b': schema.str, 'c': schema.float}),
            schema.dict({'a': schema.int, 'b': schema.str, 'd': schema.float}),
        ),
        schema.any(
            schema.dict({'a': schema.int, 'b': schema.str}),
        ),
        schema.dict({'a': schema.int, 'b': schema.str}),
    ),
    (
        schema.any(
            schema.dict({'a': schema.int, ...: ...}),
            schema.dict({'a': schema.int, 'b': schema.str, 'c': schema.float}),
            schema.dict({'a': schema.int, 'b': schema.str, 'd': schema.float}),
        ),
        schema.any(
            schema.dict({'a': schema.int, ...: ...}),
        ),
        schema.dict({'a': schema.int, ...: ...}),
    ),
    (
        schema.any(
            schema.dict({'a': schema.int, ...: ...}),
            schema.dict({'a': schema.int, 'b': schema.str, ...: ...}),
            schema.dict({'a': schema.int, 'b': schema.str, 'd': schema.float}),
        ),
        schema.any(
            schema.dict({'a': schema.int, ...: ...}),
            schema.dict({'a': schema.int, 'b': schema.str, ...: ...}),
        ),
        schema.any(
            schema.dict({'a': schema.int, ...: ...}),
            schema.dict({'a': schema.int, 'b': schema.str, ...: ...}),
        ),
    ),
])
def test_any_with_dict_schemas_clarification_with_any_with_sub_dicts_schema_substitution(
    basic_type: GenericSchema,
    substitution_type: GenericSchema,
    result: GenericSchema,
):
    with when:
        res = substitute(basic_type, substitution_type)

    with then:
        assert res == result
        assert id(res) != id(substitution_type) != id(basic_type)


# fails
@pytest.mark.parametrize("basic_type,substitution_type", [
    (
        schema.any(
            schema.dict({'a': schema.int}),
            schema.dict({'b': schema.str})
        ),
        schema.any(
            schema.dict({'b': schema.str}),
            schema.dict({'c': schema.int})
        ),
    ),
])
def test_any_with_dict_schemas_clarification_with_any_with_sub_dicts_schema_substitution_failed(
    basic_type: GenericSchema,
    substitution_type: GenericSchema,
    result: GenericSchema,
):
    # TODO substitution error, missmatched detailed type already defined
    pass


# any any-list
@pytest.mark.parametrize("basic_type,substitution_type,result", [
    (
        schema.any(
            schema.list(schema.int),
            schema.list(schema.float)
        ),
        schema.any(
            schema.list(schema.int),
            schema.list(schema.float)
        ),
        schema.any(
            schema.list(schema.int),
            schema.list(schema.float)
        ),
    ),
    (
        schema.any(
            schema.list(schema.int),
            schema.list(schema.float),
            schema.list(schema.str)
        ),
        schema.any(
            schema.list(schema.int),
            schema.list(schema.float)
        ),
        schema.any(
            schema.list(schema.int),
            schema.list(schema.float)
        ),
    ),
])
def test_any_with_dict_schemas_clarification_with_any_with_sub_dicts_schema_substitution(
    basic_type: GenericSchema,
    substitution_type: GenericSchema,
    result: GenericSchema,
):
    with when:
        res = substitute(basic_type, substitution_type)

    with then:
        assert res == result
        assert id(res) != id(substitution_type) != id(basic_type)


# fails
@pytest.mark.parametrize("basic_type,substitution_type", [
    (
        schema.any(
            schema.list(schema.int),
            schema.list(schema.float)
        ),
        schema.any(
            schema.list(schema.str),
            schema.list(schema.int)
        ),
    ),
])
def test_any_with_dict_schemas_clarification_with_any_with_sub_dicts_schema_substitution_failed(
    basic_type: GenericSchema,
    substitution_type: GenericSchema,
    result: GenericSchema,
):
    # TODO substitution error, missmatched detailed type already defined
    pass
