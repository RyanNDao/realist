import logging
import copy

LOGGER = logging.getLogger(__name__)

def recursive_lookup(key, obj, path=None):
    if path is None:
        path = []

    if key in obj:
        return obj[key], path + [key]

    for k, val in obj.items():
        if isinstance(val, dict):
            result, found_path = recursive_lookup(key, val, path + [k])
            if result is not None:
                return result, found_path

    return None, []

def editQueryVariables(key, newValue, obj):
    _, path = recursive_lookup(key, obj)
    if not path:
        LOGGER.warning(f'Did not find attribute "{key}" in query options')
    nodeToEdit = obj
    for node in path:
        if node == key:
            nodeToEdit[node] = newValue
        else: 
            nodeToEdit = nodeToEdit[node]


def returnedObjectWithPoppedAttributes(object, attributesToPop: list):
    objectToReturn = copy.deepcopy(object)
    for attribute in attributesToPop:
        objectToReturn.pop(attribute, None)
    return objectToReturn

def safeParseInt(value):
    try:
        return int(value)
    except (ValueError, TypeError):
        return None