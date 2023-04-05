from typing import Dict

from niltype import Nil


def nil_dict_to_empty(dict_: Dict):
    if dict_ is Nil:
        return {}

    return dict_
