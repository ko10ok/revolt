from copy import deepcopy
from typing import Any

from district42.types import DictSchema
from district42.utils import is_ellipsis
from niltype import Nil, Nilable
from th import PathHolder
from valera import ValidationResult, Validator
from valera.errors import ExtraKeyValidationError

__all__ = ("SubstitutorValidator",)


class SubstitutorValidator(Validator):
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

        if (... not in schema.props.keys) and (len(schema.props.keys) != len(value)):
            for key, val in value.items():
                if key not in schema.props.keys:
                    result.add_error(ExtraKeyValidationError(path, value, key))

        return result
