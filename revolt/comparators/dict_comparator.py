from typing import Dict

from district42.types import DictSchema

from .comparable import Comparable


def is_subset(set_: Dict, subset: Dict):
    # all keys from base should be contained in sub
    # if ... in base, sub can contain any extra key
    # TODO add optional keys check

    base = set(set_)
    sub = set(subset)

    extra_in_base = base - sub

    if base == sub:
        return True

    if extra_in_base == {...} or extra_in_base == set():
        return True

    return False


def dict_sub_schema_comparator(schema: DictSchema, subschema: DictSchema):
    base = Comparable(schema)
    sub = Comparable(subschema)

    # TODO extract each with error message
    stops = [
        base.has('keys') and not sub.has('keys'),
        base.has('keys') and sub.has('keys') and (
            not is_subset(
                base.prop('keys').get(),
                sub.prop('keys').get()
            )
        )
    ]
    return not any(stops)
