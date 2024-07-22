#
# Imports
#

import re

#
# Utility Functions
#

def get_basename(name: str) -> str:
    return re.sub(r"\.\d+$", "", name)