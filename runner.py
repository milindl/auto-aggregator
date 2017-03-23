#/bin/env python3

import aggregator
import time
from config import main


while True:
    try:
        aggregator.Main()
    except KeyError:
        pass
    time.sleep(main['SLEEP_TIME'])
