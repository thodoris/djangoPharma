import json

from suds.sudsobject import asdict


def __recursive_dict(d):
    out = {}
    for k, v in asdict(d).items():
        if hasattr(v, '__keylist__'):
            out[k] = __recursive_dict(v)
        elif isinstance(v, list):
            out[k] = []
            for item in v:
                if hasattr(item, '__keylist__'):
                    out[k].append(__recursive_dict(item))
                else:
                    out[k].append(item)
        else:
            out[k] = v
    return out


# converts XML to JSON
def xml2json(d):
    return json.dumps(__recursive_dict(d))
