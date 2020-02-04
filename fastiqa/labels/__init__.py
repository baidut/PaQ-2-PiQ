from ..label import *
from .TID2013 import *
from .CLIVE import *
from .KonIQ import *
from .FLIVE import *
from .TestImages import *

# test on the whole database
# e.valid(All(CLIVE))
def All(label):
    name = f'{label.__name__}_all'
    return type(name, (label,), {"valid_pct": 1})
