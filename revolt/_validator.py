from copy import deepcopy
from typing import Any

from district42.types import (
    DictSchema, ListSchema, IntSchema, FloatSchema, BoolSchema, BytesSchema
)
from district42.utils import is_ellipsis
from niltype import Nil, Nilable
from th import PathHolder
from valera import ValidationResult, Validator
from valera.errors import (
    ExtraKeyValidationError,
    LengthValidationError,
    MaxLengthValidationError,
    MinLengthValidationError, TypeValidationError, ValueValidationError, MinValueValidationError,
    MaxValueValidationError,
)

__all__ = ("SubstitutorValidator",)


class SubstitutorValidator(Validator):
    def visit_list(self, schema: ListSchema, *,
                   value: Any = Nil, path: Nilable[PathHolder] = Nil,
                   **kwargs: Any) -> ValidationResult:
        result = self._validation_result_factory()
        if path is Nil:
            path = self._path_holder_factory()

        if error := self._validate_type(path, value, list):
            return result.add_error(error)

        if schema.props.len is not Nil:
            if len(value) != schema.props.len:
                return result.add_error(LengthValidationError(path, value, schema.props.len))
        if schema.props.min_len is not Nil:
            if len(value) < schema.props.min_len:
                return result.add_error(
                    MinLengthValidationError(path, value, schema.props.min_len))
        if schema.props.max_len is not Nil:
            if len(value) > schema.props.max_len:
                return result.add_error(
                    MaxLengthValidationError(path, value, schema.props.max_len))

        if (schema.props.type is Nil) and (schema.props.elements is Nil):
            return result

        if schema.props.type is not Nil:
            type_schema = schema.props.type
            for index, elem in enumerate(value):
                if is_ellipsis(elem) and (index == 0 or index == len(value) - 1):
                    continue
                nested_path = deepcopy(path)[index]
                res = type_schema.__accept__(self, value=elem, path=nested_path, **kwargs)
                result.add_errors(res.get_errors())
            return result
        else:
            return super().visit_list(schema, value=value, path=path, **kwargs)

    def visit_dict(self, schema: DictSchema, *,
                   value: Any = Nil, path: Nilable[PathHolder] = Nil,
                   **kwargs: Any) -> ValidationResult:
        result = self._validation_result_factory()
        if path is Nil:
            path = self._path_holder_factory()

        if error := self._validate_type(path, value, dict):
            return result.add_error(error)

        if schema.props.keys is Nil:
            return result

        for key, (val, is_optional) in schema.props.keys.items():
            if is_ellipsis(key):
                continue
            if key in value:
                nested_path = deepcopy(path)[key]
                res = val.__accept__(self, value=value[key], path=nested_path, **kwargs)
                result.add_errors(res.get_errors())

        if (... not in schema.props.keys) and (set(schema.props.keys) != set(value)):
            for key, val in value.items():
                if key not in schema.props.keys:
                    result.add_error(ExtraKeyValidationError(path, value, key))

        return result

    def visit_int(self, schema: IntSchema, *,
                  value: Any = Nil, path: Nilable[PathHolder] = Nil,
                  **kwargs: Any) -> ValidationResult:
        if path == Nil:
            path = ''
        result = self._validation_result_factory()

        if error := self._validate_type(path, value, (int, IntSchema)):
            return result.add_error(error)

        if isinstance(value, IntSchema):
            if schema.props.value != Nil:
                if schema.props.value != Nil:
                    if schema.props.value != value.props.value:
                        return result.add_error(
                            ValueValidationError(path, value.props.value, schema.props.value))

            if schema.props.min != Nil:
                if value.props.min != Nil:
                    if value.props.min < schema.props.min:
                        # TODO new error MinMinValidationError
                        return result.add_error(
                            MinValueValidationError(path, value.props.min, schema.props.min))

                if value.props.max != Nil:
                    if value.props.max > schema.props.min:
                        # TODO new error MaxMinValidationError
                        return result.add_error(
                            MaxValueValidationError(path, value.props.min, schema.props.max))

                if value.props.value != Nil:
                    if value.props.value < schema.props.min:
                        return result.add_error(
                            MinValueValidationError(path, value.props.min, schema.props.min))

            if schema.props.max != Nil:
                if value.props.max != Nil:
                    if value.props.max > schema.props.max:
                        # TODO new error MaxMaxValidationError
                        return result.add_error(
                            MaxValueValidationError(path, value.props.max, schema.props.min))

                if value.props.min != Nil:
                    if value.props.min > schema.props.max:
                        # TODO new error MaxMinValidationError
                        return result.add_error(
                            MinValueValidationError(path, value.props.max, schema.props.max))

                if value.props.value != Nil:
                    if value.props.value > schema.props.max:
                        return result.add_error(
                            MaxValueValidationError(path, value.props.max, schema.props.min))

        elif isinstance(value, int):
            if schema.props.value != Nil:
                if schema.props.value != value:
                    return result.add_error(
                        ValueValidationError(path, value, schema.props.value))

            if schema.props.max != Nil:
                if value > schema.props.max:
                    return result.add_error(
                        MaxValueValidationError(path, value, schema.props.max))

            if schema.props.min != Nil:
                if value < schema.props.min:
                    return result.add_error(
                        MinValueValidationError(path, value, schema.props.min))
        else:
            return result.add_error(TypeValidationError(path, value, schema))

        return result


    def visit_float(self, schema: FloatSchema, *,
                  value: Any = Nil, path: Nilable[PathHolder] = Nil,
                  **kwargs: Any) -> ValidationResult:
        if path == Nil:
            path = ''
        result = self._validation_result_factory()

        if error := self._validate_type(path, value, (float, FloatSchema)):
            return result.add_error(error)

        if isinstance(value, FloatSchema):
            if schema.props.value != Nil:
                if schema.props.value != Nil:
                    if schema.props.value != value.props.value:
                        return result.add_error(
                            ValueValidationError(path, value.props.value, schema.props.value))

            if schema.props.min != Nil:
                if value.props.min != Nil:
                    if value.props.min < schema.props.min:
                        # TODO new error MinMinValidationError
                        return result.add_error(
                            MinValueValidationError(path, value.props.min, schema.props.min))

                if value.props.max != Nil:
                    if value.props.max > schema.props.min:
                        # TODO new error MaxMinValidationError
                        return result.add_error(
                            MaxValueValidationError(path, value.props.min, schema.props.max))

                if value.props.value != Nil:
                    if value.props.value < schema.props.min:
                        return result.add_error(
                            MinValueValidationError(path, value.props.min, schema.props.min))

            if schema.props.max != Nil:
                if value.props.max != Nil:
                    if value.props.max > schema.props.max:
                        # TODO new error MaxMaxValidationError
                        return result.add_error(
                            MaxValueValidationError(path, value.props.max, schema.props.min))

                if value.props.min != Nil:
                    if value.props.min > schema.props.max:
                        # TODO new error MaxMinValidationError
                        return result.add_error(
                            MinValueValidationError(path, value.props.max, schema.props.max))

                if value.props.value != Nil:
                    if value.props.value > schema.props.max:
                        return result.add_error(
                            MaxValueValidationError(path, value.props.max, schema.props.min))

        elif isinstance(value, float):
            if schema.props.value != Nil:
                if schema.props.value != value:
                    return result.add_error(
                        ValueValidationError(path, value, schema.props.value))

            if schema.props.max != Nil:
                if value > schema.props.max:
                    return result.add_error(
                        MaxValueValidationError(path, value, schema.props.max))

            if schema.props.min != Nil:
                if value < schema.props.min:
                    return result.add_error(
                        MinValueValidationError(path, value, schema.props.min))
        else:
            return result.add_error(TypeValidationError(path, value, schema))

        return result

    def visit_bool(self, schema: BoolSchema, *,
                  value: Any = Nil, path: Nilable[PathHolder] = Nil,
                  **kwargs: Any) -> ValidationResult:
        if path == Nil:
            path = ''
        result = self._validation_result_factory()

        if error := self._validate_type(path, value, (bool, BoolSchema)):
            return result.add_error(error)

        if isinstance(value, BoolSchema):
            if schema.props.value != Nil:
                if schema.props.value != Nil:
                    if schema.props.value != value.props.value:
                        return result.add_error(
                            ValueValidationError(path, value.props.value, schema.props.value))
        elif isinstance(value, bool):
            if schema.props.value != Nil:
                if schema.props.value != value:
                    return result.add_error(
                        ValueValidationError(path, value, schema.props.value))
        else:
            return result.add_error(TypeValidationError(path, value, schema))

        return result

    def visit_bytes(self, schema: BytesSchema, *,
                  value: Any = Nil, path: Nilable[PathHolder] = Nil,
                  **kwargs: Any) -> ValidationResult:
        if path == Nil:
            path = ''
        result = self._validation_result_factory()

        if error := self._validate_type(path, value, (bytes, BytesSchema)):
            return result.add_error(error)

        if isinstance(value, BytesSchema):
            if schema.props.value != Nil:
                if schema.props.value != Nil:
                    if schema.props.value != value.props.value:
                        return result.add_error(
                            ValueValidationError(path, value.props.value, schema.props.value))
        elif isinstance(value, bytes):
            if schema.props.value != Nil:
                if schema.props.value != value:
                    return result.add_error(
                        ValueValidationError(path, value, schema.props.value))
        else:
            return result.add_error(TypeValidationError(path, value, schema))

        return result
