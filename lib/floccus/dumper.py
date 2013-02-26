import json

import floccus.utils

def output(model, outfile):
    with open(outfile, 'w') as fp:
        json.dump(model, fp, indent=4)
