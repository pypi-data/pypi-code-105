from datetime import date
from collections import namedtuple


def getOverlaps(startdate,enddate,stardate1,enddate1) -> date:
    Range = namedtuple('Range', ['start', 'end'])
    r1 = Range(start = date(startdate), end = date(enddate))
    r2 = Range(start = stardate1, end = enddate1)
    latest_start = max(r1.start, r2.start)
    earliest_end = min(r1.end, r2.end)
    delta = (earliest_end - latest_start).days + 1
    overlap = max(0, delta)
    if overlap != 0:
        return "Overlaps"