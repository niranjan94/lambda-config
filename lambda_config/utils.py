import collections
from copy import deepcopy
from typing import Dict, List


def dict_merge(destination: Dict, changes_list: List[Dict]):
    for changes in changes_list:
        for k, v in changes.items():
            if k in destination and isinstance(destination[k], dict) and isinstance(changes[k], collections.Mapping):
                dict_merge(destination[k], changes[k])
            else:
                destination[k] = deepcopy(changes[k])
    return destination
