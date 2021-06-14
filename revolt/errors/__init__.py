from valera import ValidationResult

from .substitution_error import SubstitutionError

__all__ = ("SubstitutionError", "make_substitution_error",)


def make_substitution_error(result: ValidationResult) -> SubstitutionError:
    message = ",".join(map(str, result.get_errors()))
    return SubstitutionError(message)
