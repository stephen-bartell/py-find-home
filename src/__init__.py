import time
import datetime

THIRTY_HOURS_IN_SECONDS = 108000

class Visit:

    def __init__(self, latitude, longitude, arrival_time_local, departure_time_local):
        self.latitude = latitude
        self.longitude = longitude
        self.arrival_time_local = self._parse_time(arrival_time_local)
        self.departure_time_local = self._parse_time(departure_time_local)

    def _parse_time(self, stime):
        return datetime.datetime.fromtimestamp(time.mktime(time.strptime(stime, '%m/%d/%Y %H:%M:%S')))

    def _truncate_float(self, f, n):
        '''Truncates/pads a float f to n decimal places without rounding
        credit: http://stackoverflow.com/a/783927/448956
        '''
        s = '{}'.format(f)
        if 'e' in s or 'E' in s:
            return '{0:.{1}f}'.format(f, n)
        i, p, d = s.partition('.')
        return '.'.join([i, (d + '0' * n)[:n]])

    def get_applicable_duration(self):
        start = self.arrival_time_local
        if start.hour < 20:
            start = datetime.datetime(
                year=self.arrival_time_local.year,
                month=self.arrival_time_local.month,
                day=self.arrival_time_local.day,
                hour=20,
                minute=self.arrival_time_local.minute,
                second=self.arrival_time_local.second
            )

        end = self.departure_time_local
        if end.hour >= 8:
            end = datetime.datetime(
                year=self.arrival_time_local.year,
                month= self.arrival_time_local.month,
                day=self.arrival_time_local.day,
                hour=7,
                minute=59,
                second=self.arrival_time_local.second
            )
        return start - end

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
                'timedeltas': []
            }
        locations[vid]['timedeltas'].append(v.get_applicable_duration())

    for vid, meta in locations.items():
        total_duration = sum([td.total_seconds() for td in meta['timedeltas']], 0)
        if total_duration > THIRTY_HOURS_IN_SECONDS:
            return {'latitude': meta['latitude'], 'longitude': meta['longitude']}
