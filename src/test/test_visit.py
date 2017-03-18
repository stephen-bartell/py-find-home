from unittest import TestCase
from src import Visit
import datetime


class VisitTestCase(TestCase):

    def test_get_duration_when_in_full_window(self):
        pass

    def test_get_duration_when_in_partial_window(self):
        pass

    def test_get_duration_when_not_in_window(self):
        pass

    def test_parse_timestring(self):
        visit = Visit(None, None, '3/17/2017 20:42:43', '3/17/2017 20:42:43')
        self.assertEqual(
            visit._parse_time('3/17/2017 20:42:43'),
            datetime.datetime(2017, 3, 17, 20, 42, 43)
        )
        pass
