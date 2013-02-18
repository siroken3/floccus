import json

import floccus.utils

def output(model):
    return json.dumps(model, indent=4, sort_keys=True)
