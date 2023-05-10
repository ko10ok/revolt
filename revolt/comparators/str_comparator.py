from district42.types import StrSchema

from .comparable import Comparable


def str_sub_schema_comparator(schema: StrSchema, subschema: StrSchema):
    base = Comparable(schema)
    sub = Comparable(subschema)

    # TODO extract each with error message
    stops = [
        base.has('len') and any([
            not sub.has('len'),
            sub.has('substr') and len(sub.prop('substr').get()) > base.prop('len').get(),
            sub.has('len') and sub.prop('len').get() != base.prop('len').get(),
        ]),
        base.has('min_len') and any([
            not (sub.has('min_len') or sub.has('len')),
            sub.has('min_len') and base.prop('min_len').get() > sub.prop('min_len').get(),
            sub.has('max_len') and base.prop('min_len').get() > sub.prop('max_len').get(),
            sub.has('len') and sub.prop('len').get() < base.prop('min_len').get(),
        ]),
        base.has('max_len') and any([
            not (sub.has('max_len') or sub.has('len')),
            sub.has('max_len') and base.prop('max_len').get() < sub.prop('max_len').get(),
            sub.has('min_len') and base.prop('max_len').get() < sub.prop('min_len').get(),
            sub.has('len') and sub.prop('len').get() > base.prop('max_len').get(),
        ]),
        base.has('substr') and any([
            sub.has('substr') and sub.prop('substr').get() not in base.prop('substr').get(),
            sub.has('value') and base.prop('substr').get() not in sub.prop('value').get(),
            sub.has('len') and len(base.prop('substr').get()) > sub.prop('len').get(),
        ]),
        base.has('regex') and not sub.has('regex'),
        base.has('value') and any([
            not sub.has('value'),
            sub.has('value') and base.prop('value').get() != sub.prop('value').get(),
            sub.has('len') and len(base.prop('value').get()) != sub.prop('len').get(),
            sub.has('min_len') and len(base.prop('value').get()) < sub.prop('min_len').get(),
            sub.has('max_len') and len(base.prop('value').get()) > sub.prop('max_len').get(),
            sub.has('contains')
        ]),
    ]
    return not any(stops)
