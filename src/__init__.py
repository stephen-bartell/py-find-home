from time import mktime, strptime
from datetime import datetime, timedelta
from dateutil.rrule import rrule, rruleset, SECONDLY

THIRTY_HOURS_IN_SECONDS = 108000


class Visit:

    def __init__(self, latitude, longitude, arrival_time_local, departure_time_local):
        self.latitude = latitude
        self.longitude = longitude
        self.arrival_time_local = self._parse_time(arrival_time_local)
        self.departure_time_local = self._parse_time(departure_time_local)

    def _parse_time(self, stime):
        return datetime.fromtimestamp(mktime(strptime(stime, '%m/%d/%Y %H:%M:%S')))

    @staticmethod
    def _truncate_float(f, n):
        """Truncates/pads a float f to n decimal places without rounding
        credit: http://stackoverflow.com/a/783927/448956
        """
        s = '{}'.format(f)
        if 'e' in s or 'E' in s:
            return '{0:.{1}f}'.format(f, n)
        i, p, d = s.partition('.')
        return '.'.join([i, (d + '0' * n)[:n]])

    def get_applicable_duration(self):
        # create a new rule set
        valid_times = rruleset()

        # include the full range of seconds for the stay duration
        valid_times.rrule(rrule(SECONDLY, dtstart=self.arrival_time_local, until=self.departure_time_local))

        # exclude the range of invalid seconds from the set
        valid_times.exrule(rrule(SECONDLY, dtstart=self.arrival_time_local, until=self.departure_time_local,
                                 byhour=range(8, 20)))

        return valid_times.count()

    def get_visit_id(self):
        return '{}..{}'.format(
            self._truncate_float(self.latitude, 3),
            self._truncate_float(self.longitude, 3)
        )


def find_home(jsonvisits):
    locations = {}
    visits = [Visit(**jv) for jv in jsonvisits]
    for v in visits:
        vid = v.get_visit_id()
        if vid not in locations:
            locations[vid] = {
                'latitude': v.latitude,
                'longitude': v.longitude,
                'deltas': []
            }
        locations[vid]['deltas'].append(v.get_applicable_duration())

    for vid, meta in locations.items():
        total_duration = sum([seconds for seconds in meta['deltas']], 0)
        if total_duration >= THIRTY_HOURS_IN_SECONDS:
            return {'latitude': meta['latitude'], 'longitude': meta['longitude']}
