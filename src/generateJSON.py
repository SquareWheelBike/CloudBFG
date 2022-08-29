import zsoc
import json
import numpy

# generate Vo curve
k = [-4.4813,30.3625,-5.4895,0.6087,-0.0285,-16.9776,38.2121,-0.1162]
batt = zsoc.OCV_curve(k)
# json doesnt like numpy arrays
batt = {k: list(v) if type(v) is numpy.ndarray else v for k, v in batt.items()}

# print to stdout (json)
print(json.dumps(batt, indent=2))