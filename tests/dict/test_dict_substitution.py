from unittest.mock import sentinel

from baby_steps import given, then, when
from district42 import schema
from pytest import raises

from revolt import substitute
from revolt.errors import SubstitutionError


def test_dict_no_keys_substitution():
    with given:
        sch = schema.dict

    with when:
        res = substitute(sch, {})

    with then:
        assert res == schema.dict({})
        assert res != sch


def test_dict_invalid_value_substitution_error():
    with given:
        sch = schema.dict

    with when, raises(Exception) as exception:
        substitute(sch, [])

    with then:
        assert exception.type is SubstitutionError


def test_dict_keys_substitution():
    with given:
        sch = schema.dict

    with when:
        res = substitute(sch, {
            "result": {
                "id": 1,
                "name": "Bob"
            },
        })

    with then:
        # from_native
        assert res == schema.dict({
            "result": schema.dict({
                "id": schema.int(1),
                "name": schema.str("Bob"),
            }),
        })
        assert res != sch


def test_dict_value_substitution_error():
    with given:
        sch = schema.dict

    with when, raises(Exception) as exception:
        substitute(sch, {"val": sentinel})

    with then:
        assert exception.type is SubstitutionError


def test_dict_values_substitution():
    with given:
        sch = schema.dict({
            "result": schema.dict({
                "id": schema.int,
                "name": schema.str,
            }),
        })

    with when:
        res = substitute(sch, {
            "result": {
                "id": 1,
                "name": "Bob",
            },
        })

    with then:
        assert res == schema.dict({
            "result": schema.dict({
                "id": schema.int(1),
                "name": schema.str("Bob"),
            }),
        })
        assert res != sch


def test_dict_incorrect_value_substitution_error():
    with given:
        sch = schema.dict({
            "id": schema.int,
        })

    with when, raises(Exception) as exception:
        substitute(sch, {"id": "1"})

    with then:
        assert exception.type is SubstitutionError


def test_dict_more_keys_substitution_error():
    with given:
        sch = schema.dict({
            "id": schema.int,
        })

    with when, raises(Exception) as exception:
        substitute(sch, {
            "id": 1,
            "name": "Bob",
        })

    with then:
        assert exception.type is SubstitutionError


def test_dict_less_keys_substitution():
    with given:
        sch = schema.dict({
            "result": schema.dict({
                "id": schema.int,
                "name": schema.str,
            }),
        })

    with when:
        res = substitute(sch, {
            "result": {
                "id": 1,
            },
        })

    with then:
        assert res == schema.dict({
            "result": schema.dict({
                "id": schema.int(1),
                "name": schema.str,
            }),
        })
        assert res != sch
