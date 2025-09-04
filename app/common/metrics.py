import time
from collections import defaultdict

# keep timestamps of requests per module
REQUEST_COUNTERS = defaultdict(list)

# how long to keep request timestamps
LIFE_TIME = 60  # 60 seconds window

def record_request(module: str):
    now = time.time()
    REQUEST_COUNTERS[module].append(now)
    _cleanup(module)

def get_rpm(module: str) -> int:
    """Requests per LIFE_TIME window"""
    _cleanup(module)
    return len(REQUEST_COUNTERS[module])

def _cleanup(module: str):
    """Remove old timestamps outside the window"""
    now = time.time()
    cutoff = now - LIFE_TIME
    REQUEST_COUNTERS[module] = [t for t in REQUEST_COUNTERS[module] if t >= cutoff]
